"""
Document Service Lambda Handler
Handles document upload, validation, S3 storage, and OCR extraction.
"""
import os
import sys
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.utils import (
    get_dynamodb_resource, get_s3_client, get_table_name,
    upload_to_s3, generate_presigned_url, get_document_s3_key,
)

app = FastAPI(title="Document Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCUMENTS_BUCKET = os.getenv("S3_DOCUMENTS_BUCKET", "voice-for-bharat-documents")

# Allowed MIME types → extension map
ALLOWED_TYPES: dict[str, str] = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
}

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

dynamodb = get_dynamodb_resource()


def get_docs_table():
    return dynamodb.Table(get_table_name("applications"))  # documents metadata stored in applications table


def get_activity_table():
    return dynamodb.Table(get_table_name("activity_log"))


def _log_activity(user_id: str, activity_type: str, metadata: dict = None):
    try:
        ttl = int(datetime.utcnow().timestamp()) + (90 * 24 * 3600)
        get_activity_table().put_item(Item={
            "activityId": str(uuid.uuid4()),
            "userId": user_id,
            "type": activity_type,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "ttl": ttl,
        })
    except Exception as e:
        print(f"[activity_log] non-fatal: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "document_service"}


@app.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    documentType: str = Form(...),
    userId: str = Form(...),
    schemeId: Optional[str] = Form(default=None),
):
    """Upload a document to S3 and return metadata."""
    # --- Validate MIME type ---
    content_type = file.content_type or ""
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{content_type}'. Allowed: PDF, JPG, PNG.",
        )

    # --- Read and size-check ---
    data = await file.read()
    if len(data) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File exceeds 5 MB size limit.")

    # --- Build S3 key ---
    ext = ALLOWED_TYPES[content_type]
    document_id = str(uuid.uuid4())
    s3_key = f"users/{userId}/{documentType}/{document_id}.{ext}"

    # --- Upload ---
    success = upload_to_s3(
        bucket=DOCUMENTS_BUCKET,
        key=s3_key,
        data=data,
        content_type=content_type,
        metadata={
            "documentId": document_id,
            "documentType": documentType,
            "userId": userId,
            "originalFilename": file.filename or "",
        },
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload document to S3.")

    now = datetime.utcnow().isoformat()

    # --- Generate short-lived presigned URL (1 hour) ---
    presigned_url = generate_presigned_url(DOCUMENTS_BUCKET, s3_key, expiration=3600)

    doc_meta = {
        "id": document_id,
        "documentId": document_id,
        "type": documentType,
        "name": file.filename or f"{documentType}.{ext}",
        "s3Key": s3_key,
        "url": presigned_url or "",
        "uploadedAt": now,
        "verified": False,
        "userId": userId,
        "schemeId": schemeId,
    }

    _log_activity(userId, "DOCUMENT_UPLOADED", {"documentId": document_id, "documentType": documentType})

    return JSONResponse(content={"document": doc_meta}, status_code=201)


@app.get("/documents/{document_id}")
async def get_document(document_id: str, userId: str):
    """Return a fresh presigned URL for the document."""
    # We can't easily look up by documentId without a GSI on S3 metadata,
    # so we reconstruct the key from the document_id if it's stored.
    # For now, require the caller to pass userId so we can scan user prefix.
    s3 = get_s3_client()
    prefix = f"users/{userId}/"

    try:
        resp = s3.list_objects_v2(Bucket=DOCUMENTS_BUCKET, Prefix=prefix)
        objects = resp.get("Contents", [])
        matched_key = next(
            (o["Key"] for o in objects if document_id in o["Key"]),
            None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

    if not matched_key:
        raise HTTPException(status_code=404, detail="Document not found")

    presigned_url = generate_presigned_url(DOCUMENTS_BUCKET, matched_key, expiration=3600)

    head = s3.head_object(Bucket=DOCUMENTS_BUCKET, Key=matched_key)
    meta = head.get("Metadata", {})

    return {
        "document": {
            "id": document_id,
            "documentId": document_id,
            "type": meta.get("documenttype", ""),
            "name": meta.get("originalfilename", document_id),
            "s3Key": matched_key,
            "url": presigned_url,
            "userId": userId,
        }
    }


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str, userId: str):
    """Delete a document from S3."""
    s3 = get_s3_client()
    prefix = f"users/{userId}/"

    try:
        resp = s3.list_objects_v2(Bucket=DOCUMENTS_BUCKET, Prefix=prefix)
        objects = resp.get("Contents", [])
        matched_key = next(
            (o["Key"] for o in objects if document_id in o["Key"]),
            None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

    if not matched_key:
        raise HTTPException(status_code=404, detail="Document not found")

    s3.delete_object(Bucket=DOCUMENTS_BUCKET, Key=matched_key)
    _log_activity(userId, "DOCUMENT_DELETED", {"documentId": document_id})

    return {"success": True, "message": "Document deleted successfully"}


# Lambda handler
handler = Mangum(app, lifespan="off")
