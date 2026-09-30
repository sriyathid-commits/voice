"""
Application Service Lambda Handler
Manages the complete application lifecycle from draft to submission.
"""
import os
import sys
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.utils import get_dynamodb_resource, get_table_name, get_eventbridge_client

app = FastAPI(title="Application Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = get_dynamodb_resource()


def get_applications_table():
    return dynamodb.Table(get_table_name("applications"))


def get_activity_table():
    return dynamodb.Table(get_table_name("activity_log"))


def log_activity(user_id: str, activity_type: str, metadata: dict = None):
    """Write an entry to the activity_log table."""
    try:
        now = datetime.utcnow().isoformat()
        ttl = int((datetime.utcnow().timestamp()) + (90 * 24 * 3600))  # 90-day TTL
        get_activity_table().put_item(Item={
            "activityId": str(uuid.uuid4()),
            "userId": user_id,
            "type": activity_type,
            "timestamp": now,
            "metadata": metadata or {},
            "ttl": ttl,
        })
    except Exception as e:
        print(f"[activity_log] non-fatal error: {e}")


# ── Request / Response models ──────────────────────────────────────────────

class ApplicantDetails(BaseModel):
    applicantName: str
    fatherName: Optional[str] = None
    motherName: Optional[str] = None
    contactNumber: str
    email: Optional[str] = None
    address: Optional[str] = None
    purpose: Optional[str] = None
    additionalInfo: Optional[str] = None


class CreateApplicationRequest(BaseModel):
    schemeId: str
    userId: str
    applicantDetails: ApplicantDetails
    documents: Optional[List[str]] = []
    status: Optional[str] = "DRAFT"


class UpdateApplicationRequest(BaseModel):
    applicantDetails: Optional[ApplicantDetails] = None
    documents: Optional[List[str]] = None


class ApplicationResponse(BaseModel):
    applicationId: str
    userId: str
    schemeId: str
    schemeName: Optional[str] = None
    status: str
    applicantDetails: Dict[str, Any]
    documents: List[str]
    submittedAt: Optional[str] = None
    createdAt: str
    updatedAt: str
    statusHistory: List[Dict[str, Any]]


# ── Helpers ────────────────────────────────────────────────────────────────

def _fetch_application(application_id: str) -> dict:
    resp = get_applications_table().get_item(Key={"applicationId": application_id})
    item = resp.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Application not found")
    return item


def _to_response(item: dict) -> dict:
    return {
        "applicationId": item["applicationId"],
        "userId": item["userId"],
        "schemeId": item["schemeId"],
        "schemeName": item.get("schemeName", ""),
        "status": item["status"],
        "applicantDetails": item.get("applicantDetails", {}),
        "documents": item.get("documents", []),
        "submittedAt": item.get("submittedAt"),
        "createdAt": item["createdAt"],
        "updatedAt": item["updatedAt"],
        "statusHistory": item.get("statusHistory", []),
    }


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "application_service"}


@app.post("/applications", status_code=status.HTTP_201_CREATED)
async def create_application(request: CreateApplicationRequest):
    """Create a new application (DRAFT or immediately SUBMITTED)."""
    now = datetime.utcnow().isoformat()
    application_id = str(uuid.uuid4())
    app_status = request.status if request.status in ("DRAFT", "SUBMITTED") else "DRAFT"

    item = {
        "applicationId": application_id,
        "userId": request.userId,
        "schemeId": request.schemeId,
        "status": app_status,
        "applicantDetails": request.applicantDetails.model_dump(exclude_none=True),
        "documents": request.documents or [],
        "createdAt": now,
        "updatedAt": now,
        "statusHistory": [{"status": app_status, "timestamp": now, "remarks": "Application created"}],
    }
    if app_status == "SUBMITTED":
        item["submittedAt"] = now

    get_applications_table().put_item(Item=item)
    log_activity(request.userId, "APPLICATION_CREATED", {"applicationId": application_id, "schemeId": request.schemeId})

    return {"applicationId": application_id, "application": _to_response(item)}


@app.get("/applications")
async def list_applications(
    user_id: str = Query(..., description="User ID"),
    application_status: Optional[str] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
):
    """List applications for a user, optionally filtered by status."""
    table = get_applications_table()

    # Use the userId-status GSI when filtering by status, otherwise scan by userId
    try:
        if application_status:
            resp = table.query(
                IndexName="userId-status-index",
                KeyConditionExpression="userId = :uid AND #s = :status",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":uid": user_id, ":status": application_status},
                Limit=limit,
            )
        else:
            resp = table.query(
                IndexName="userId-status-index",
                KeyConditionExpression="userId = :uid",
                ExpressionAttributeValues={":uid": user_id},
                Limit=limit,
            )
    except Exception:
        # Fallback: scan (table might not have GSI yet in some envs)
        resp = table.scan(
            FilterExpression="userId = :uid",
            ExpressionAttributeValues={":uid": user_id},
            Limit=limit,
        )

    items = resp.get("Items", [])
    items.sort(key=lambda x: x.get("updatedAt", ""), reverse=True)

    return {
        "applications": [_to_response(i) for i in items],
        "count": len(items),
    }


@app.get("/applications/{application_id}")
async def get_application(application_id: str):
    """Get a single application by ID."""
    return {"application": _to_response(_fetch_application(application_id))}


@app.put("/applications/{application_id}")
async def update_application(application_id: str, request: UpdateApplicationRequest):
    """Update an application that is still in DRAFT status."""
    item = _fetch_application(application_id)

    if item["status"] != "DRAFT":
        raise HTTPException(status_code=400, detail="Only DRAFT applications can be updated")

    now = datetime.utcnow().isoformat()
    update_expr_parts = ["updatedAt = :now"]
    expr_values: Dict[str, Any] = {":now": now}

    if request.applicantDetails is not None:
        update_expr_parts.append("applicantDetails = :details")
        expr_values[":details"] = request.applicantDetails.model_dump(exclude_none=True)

    if request.documents is not None:
        update_expr_parts.append("documents = :docs")
        expr_values[":docs"] = request.documents

    get_applications_table().update_item(
        Key={"applicationId": application_id},
        UpdateExpression="SET " + ", ".join(update_expr_parts),
        ExpressionAttributeValues=expr_values,
    )

    updated = _fetch_application(application_id)
    log_activity(item["userId"], "APPLICATION_UPDATED", {"applicationId": application_id})
    return {"application": _to_response(updated)}


@app.post("/applications/{application_id}/submit")
async def submit_application(application_id: str):
    """Submit a DRAFT application."""
    item = _fetch_application(application_id)

    if item["status"] == "SUBMITTED":
        return {"message": "Application already submitted", "application": _to_response(item)}

    if item["status"] not in ("DRAFT",):
        raise HTTPException(status_code=400, detail=f"Cannot submit application in {item['status']} status")

    now = datetime.utcnow().isoformat()
    history = item.get("statusHistory", [])
    history.append({"status": "SUBMITTED", "timestamp": now, "remarks": "Application submitted by user"})

    get_applications_table().update_item(
        Key={"applicationId": application_id},
        UpdateExpression="SET #s = :s, submittedAt = :t, updatedAt = :t, statusHistory = :h",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "SUBMITTED", ":t": now, ":h": history},
    )

    log_activity(item["userId"], "APPLICATION_SUBMITTED", {"applicationId": application_id, "schemeId": item.get("schemeId")})

    # Fire EventBridge event
    try:
        eb = get_eventbridge_client()
        eb.put_events(Entries=[{
            "Source": "voice-for-bharat.application",
            "DetailType": "ApplicationSubmitted",
            "Detail": f'{{"applicationId":"{application_id}","userId":"{item["userId"]}","schemeId":"{item.get("schemeId","")}","submittedAt":"{now}"}}',
            "EventBusName": os.getenv("EVENT_BUS_NAME", "default"),
        }])
    except Exception as e:
        print(f"[eventbridge] non-fatal: {e}")

    updated = _fetch_application(application_id)
    return {"message": "Application submitted successfully", "application": _to_response(updated)}


# Lambda handler
handler = Mangum(app, lifespan="off")
