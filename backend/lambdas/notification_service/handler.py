"""
Notification Service Lambda Handler
Handles multi-channel notifications (SMS, Email, Push, WhatsApp).
"""
import os
import sys
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel, Field

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.utils import get_dynamodb_resource, get_sns_client, get_table_name

app = FastAPI(title="Notification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")

dynamodb = get_dynamodb_resource()
sns_client = get_sns_client()


def get_notifications_table():
    """Get the activity_log table for notification history"""
    return dynamodb.Table(get_table_name("activity_log"))


def log_notification(user_id: str, channel: str, message: str, status: str, metadata: dict = None):
    """Log notification to activity table"""
    try:
        ttl = int(datetime.utcnow().timestamp()) + (90 * 24 * 3600)  # 90-day TTL
        get_notifications_table().put_item(Item={
            "activityId": str(uuid.uuid4()),
            "userId": user_id,
            "type": "NOTIFICATION_SENT",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "channel": channel,
                "message": message[:100],  # Truncate long messages
                "status": status,
                **(metadata or {})
            },
            "ttl": ttl,
        })
    except Exception as e:
        print(f"[notification_log] non-fatal: {e}")


# ── Request Models ────────────────────────────────────────────────────────

class NotificationRequest(BaseModel):
    userId: str
    channels: List[str] = Field(..., description="Channels: sms, email, push, whatsapp")
    message: str
    subject: Optional[str] = None
    templateData: Optional[Dict[str, Any]] = None
    priority: str = Field(default="normal", description="Priority: low, normal, high, urgent")


class BulkNotificationRequest(BaseModel):
    userIds: List[str]
    channels: List[str]
    message: str
    subject: Optional[str] = None
    templateData: Optional[Dict[str, Any]] = None
    priority: str = "normal"


class NotificationResponse(BaseModel):
    notificationId: str
    status: str
    channels: Dict[str, str]  # channel -> status
    message: str


# ── Helper Functions ──────────────────────────────────────────────────────

def send_sms(phone_number: str, message: str) -> bool:
    """Send SMS via AWS SNS"""
    try:
        if not phone_number.startswith("+"):
            phone_number = f"+91{phone_number}"
            
        response = sns_client.publish(
            PhoneNumber=phone_number,
            Message=message[:140],  # SMS character limit
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'VoiceBharat'
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            }
        )
        return response.get("MessageId") is not None
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False


def send_email(email: str, subject: str, message: str) -> bool:
    """Send email via AWS SNS (requires email topic subscription)"""
    try:
        if not SNS_TOPIC_ARN:
            print("SNS_TOPIC_ARN not configured")
            return False
            
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject or "Voice for Bharat Notification",
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': email
                },
                'channel': {
                    'DataType': 'String',
                    'StringValue': 'email'
                }
            }
        )
        return response.get("MessageId") is not None
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def send_push(user_id: str, title: str, message: str) -> bool:
    """Send push notification (placeholder - requires FCM/APNS setup)"""
    # In production, integrate with AWS SNS Mobile Push or Firebase
    print(f"[PUSH] Would send to {user_id}: {title} - {message}")
    return True  # Simulate success


def send_whatsapp(phone_number: str, message: str) -> bool:
    """Send WhatsApp message via Business API"""
    try:
        if not WHATSAPP_API_KEY:
            print("WhatsApp API key not configured")
            return False
            
        # Placeholder for WhatsApp Business API integration
        # In production, use Twilio, Meta Business API, or similar
        print(f"[WhatsApp] Would send to {phone_number}: {message}")
        return True  # Simulate success
    except Exception as e:
        print(f"WhatsApp sending failed: {e}")
        return False


def get_user_contact_info(user_id: str) -> Dict[str, str]:
    """Fetch user contact info from users table"""
    try:
        users_table = dynamodb.Table(get_table_name("users"))
        response = users_table.get_item(Key={"userId": user_id})
        
        if "Item" not in response:
            return {}
            
        user = response["Item"]
        return {
            "phoneNumber": user.get("phoneNumber", ""),
            "email": user.get("profile", {}).get("email", ""),
        }
    except Exception as e:
        print(f"Failed to get user contact info: {e}")
        return {}


# ── API Endpoints ─────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notification_service"}


@app.post("/notifications/send", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest):
    """Send notification to a single user via multiple channels"""
    notification_id = str(uuid.uuid4())
    
    # Get user contact info
    contact_info = get_user_contact_info(request.userId)
    if not contact_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    channel_results = {}
    
    for channel in request.channels:
        success = False
        
        if channel == "sms" and contact_info.get("phoneNumber"):
            success = send_sms(contact_info["phoneNumber"], request.message)
        elif channel == "email" and contact_info.get("email"):
            success = send_email(contact_info["email"], request.subject or "Notification", request.message)
        elif channel == "push":
            success = send_push(request.userId, request.subject or "Update", request.message)
        elif channel == "whatsapp" and contact_info.get("phoneNumber"):
            success = send_whatsapp(contact_info["phoneNumber"], request.message)
        else:
            channel_results[channel] = "unsupported_or_missing_contact"
            continue
            
        channel_results[channel] = "sent" if success else "failed"
        
        # Log the notification attempt
        log_notification(
            user_id=request.userId,
            channel=channel,
            message=request.message,
            status="sent" if success else "failed",
            metadata={
                "notificationId": notification_id,
                "priority": request.priority,
                "subject": request.subject,
            }
        )
    
    overall_status = "sent" if any(status == "sent" for status in channel_results.values()) else "failed"
    
    return NotificationResponse(
        notificationId=notification_id,
        status=overall_status,
        channels=channel_results,
        message=request.message
    )


@app.post("/notifications/bulk")
async def send_bulk_notification(request: BulkNotificationRequest):
    """Send notifications to multiple users"""
    results = []
    
    for user_id in request.userIds:
        try:
            # Create individual notification request
            individual_request = NotificationRequest(
                userId=user_id,
                channels=request.channels,
                message=request.message,
                subject=request.subject,
                templateData=request.templateData,
                priority=request.priority
            )
            
            # Send notification
            result = await send_notification(individual_request)
            results.append({
                "userId": user_id,
                "notificationId": result.notificationId,
                "status": result.status,
                "channels": result.channels
            })
            
        except Exception as e:
            results.append({
                "userId": user_id,
                "status": "failed",
                "error": str(e)
            })
    
    successful = len([r for r in results if r.get("status") == "sent"])
    
    return {
        "totalUsers": len(request.userIds),
        "successful": successful,
        "failed": len(request.userIds) - successful,
        "results": results
    }


@app.get("/notifications/history")
async def get_notification_history(
    user_id: str,
    limit: int = 50,
    channel: Optional[str] = None
):
    """Get notification history for a user"""
    try:
        table = get_notifications_table()
        
        # Query activity log for notifications
        response = table.query(
            IndexName="userId-timestamp-index",
            KeyConditionExpression="userId = :uid",
            FilterExpression="#t = :type" + (
                " AND #metadata.#channel = :channel" if channel else ""
            ),
            ExpressionAttributeNames={
                "#t": "type",
                "#metadata": "metadata",
                **({"#channel": "channel"} if channel else {})
            },
            ExpressionAttributeValues={
                ":uid": user_id,
                ":type": "NOTIFICATION_SENT",
                **({"channel": channel} if channel else {})
            },
            ScanIndexForward=False,  # Most recent first
            Limit=limit
        )
        
        notifications = response.get("Items", [])
        
        return {
            "userId": user_id,
            "notifications": [
                {
                    "notificationId": n.get("metadata", {}).get("notificationId"),
                    "timestamp": n.get("timestamp"),
                    "channel": n.get("metadata", {}).get("channel"),
                    "message": n.get("metadata", {}).get("message"),
                    "status": n.get("metadata", {}).get("status"),
                    "priority": n.get("metadata", {}).get("priority"),
                }
                for n in notifications
            ],
            "count": len(notifications)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notification history: {str(e)}")


# ── EventBridge Event Handler ────────────────────────────────────────────

async def handle_eventbridge_event(event: dict):
    """Handle EventBridge events (ApplicationSubmitted, etc.)"""
    try:
        detail_type = event.get("detail-type", "")
        detail = json.loads(event.get("detail", "{}"))
        
        if detail_type == "ApplicationSubmitted":
            user_id = detail.get("userId")
            application_id = detail.get("applicationId")
            
            if user_id:
                await send_notification(NotificationRequest(
                    userId=user_id,
                    channels=["sms", "push"],
                    message=f"Your application {application_id[:8]} has been submitted successfully. You will receive updates on the status.",
                    subject="Application Submitted",
                    priority="normal"
                ))
                
        elif detail_type == "ApplicationStatusChanged":
            user_id = detail.get("userId")
            status = detail.get("status")
            application_id = detail.get("applicationId")
            
            if user_id and status:
                message = f"Your application {application_id[:8]} status has been updated to: {status}"
                if status == "APPROVED":
                    message += ". Congratulations! Check your dashboard for next steps."
                elif status == "REJECTED":
                    message += ". Please review the feedback and consider reapplying."
                
                await send_notification(NotificationRequest(
                    userId=user_id,
                    channels=["sms", "push", "email"],
                    message=message,
                    subject=f"Application Status Update: {status}",
                    priority="high" if status in ["APPROVED", "REJECTED"] else "normal"
                ))
        
        elif detail_type == "DocumentVerified":
            user_id = detail.get("userId")
            document_type = detail.get("documentType")
            
            if user_id:
                await send_notification(NotificationRequest(
                    userId=user_id,
                    channels=["push"],
                    message=f"Your {document_type} document has been verified successfully.",
                    subject="Document Verified",
                    priority="low"
                ))
        
        print(f"Processed EventBridge event: {detail_type}")
        
    except Exception as e:
        print(f"Failed to handle EventBridge event: {e}")


# Lambda handler
handler = Mangum(app, lifespan="off")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler - handles both API Gateway and EventBridge events
    """
    # Check if this is an EventBridge event
    if event.get("source") == "voice-for-bharat.application":
        import asyncio
        asyncio.run(handle_eventbridge_event(event))
        return {"statusCode": 200, "body": "Event processed"}
    
    # Otherwise, handle as API Gateway event via Mangum
    return handler(event, context)