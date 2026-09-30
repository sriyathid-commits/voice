"""
User Service Lambda Handler
Handles user registration, authentication, and profile management.
"""
import os
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel, Field
import boto3
from botocore.exceptions import ClientError

# Import shared models and utilities
import sys
sys.path.append('/opt/python')  # Lambda layer path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from models import User, UserProfile, UserPreferences
from utils import (
    get_dynamodb_resource,
    get_cognito_client,
    get_table_name,
    calculate_profile_strength
)

# Initialize FastAPI app
app = FastAPI(
    title="User Service",
    description="User registration, authentication, and profile management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID", "")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

# Validate required environment variables
if not COGNITO_USER_POOL_ID:
    print("WARNING: COGNITO_USER_POOL_ID not set")
if not COGNITO_CLIENT_ID:
    print("WARNING: COGNITO_CLIENT_ID not set")

# Initialize AWS clients
dynamodb = get_dynamodb_resource()
cognito_client = get_cognito_client()


# Request/Response models
class RegisterRequest(BaseModel):
    """User registration request"""
    phone_number: str = Field(..., description="10-digit Indian mobile number")
    language: str = Field(default="en", description="Preferred language code")


class RegisterResponse(BaseModel):
    """User registration response"""
    user_id: str
    phone_number: str
    message: str


class VerifyOTPRequest(BaseModel):
    """OTP verification request"""
    phone_number: str = Field(..., description="10-digit Indian mobile number")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")


class VerifyOTPResponse(BaseModel):
    """OTP verification response"""
    user_id: str
    access_token: str
    refresh_token: str
    id_token: str
    message: str


class UpdateProfileRequest(BaseModel):
    """Profile update request"""
    profile: UserProfile


class ProfileResponse(BaseModel):
    """Profile response"""
    user_id: str
    phone_number: str
    language: str
    profile: Optional[UserProfile]
    preferences: UserPreferences
    profile_strength: int
    created_at: str
    updated_at: str
    last_login_at: Optional[str]


# Helper functions
def get_user_by_phone(phone_number: str) -> Optional[Dict[str, Any]]:
    """Get user by phone number from DynamoDB"""
    table = dynamodb.Table(get_table_name("users"))
    
    try:
        # Query using GSI on phone_number
        response = table.query(
            IndexName="phoneNumber-index",
            KeyConditionExpression="phoneNumber = :phone",
            ExpressionAttributeValues={":phone": phone_number}
        )
        
        if response.get("Items"):
            return response["Items"][0]
        return None
    except ClientError as e:
        print(f"Error querying user by phone: {e}")
        return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by user_id from DynamoDB"""
    table = dynamodb.Table(get_table_name("users"))
    
    try:
        response = table.get_item(Key={"userId": user_id})
        return response.get("Item")
    except ClientError as e:
        print(f"Error getting user by ID: {e}")
        return None


def create_user_in_db(user_id: str, phone_number: str, language: str, cognito_id: str) -> bool:
    """Create user in DynamoDB"""
    table = dynamodb.Table(get_table_name("users"))
    
    now = datetime.utcnow().isoformat()
    
    user_item = {
        "userId": user_id,
        "phoneNumber": phone_number,
        "language": language,
        "cognitoId": cognito_id,
        "profile": {},
        "preferences": {
            "notificationChannels": ["sms"],
            "preferredLanguage": language,
            "voiceSpeed": 1.0,
            "autoPlayAudio": True
        },
        "profileStrength": 0,
        "savedSchemes": [],
        "createdAt": now,
        "updatedAt": now,
        "lastLoginAt": None
    }
    
    try:
        table.put_item(Item=user_item)
        return True
    except ClientError as e:
        print(f"Error creating user in DB: {e}")
        return False


def update_user_profile_in_db(user_id: str, profile_data: Dict[str, Any]) -> bool:
    """Update user profile in DynamoDB"""
    table = dynamodb.Table(get_table_name("users"))
    
    # Calculate profile strength
    profile_strength = calculate_profile_strength(profile_data)
    
    now = datetime.utcnow().isoformat()
    
    try:
        table.update_item(
            Key={"userId": user_id},
            UpdateExpression="SET profile = :profile, profileStrength = :strength, updatedAt = :updated",
            ExpressionAttributeValues={
                ":profile": profile_data,
                ":strength": profile_strength,
                ":updated": now
            }
        )
        return True
    except ClientError as e:
        print(f"Error updating user profile: {e}")
        return False


def update_last_login(user_id: str) -> bool:
    """Update user's last login timestamp"""
    table = dynamodb.Table(get_table_name("users"))
    
    now = datetime.utcnow().isoformat()
    
    try:
        table.update_item(
            Key={"userId": user_id},
            UpdateExpression="SET lastLoginAt = :login_time",
            ExpressionAttributeValues={":login_time": now}
        )
        return True
    except ClientError as e:
        print(f"Error updating last login: {e}")
        return False


# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "user-service"}


@app.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterRequest):
    """
    Register a new user with phone number
    Sends OTP via AWS Cognito
    """
    # Validate phone number format
    phone_number = request.phone_number.strip()
    if not phone_number.startswith("+91"):
        phone_number = f"+91{phone_number}"
    
    # Check if user already exists
    existing_user = get_user_by_phone(phone_number.replace("+91", ""))
    if existing_user:
        # User exists, initiate OTP for login
        try:
            cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow="CUSTOM_AUTH",
                AuthParameters={
                    "USERNAME": phone_number
                }
            )
            
            return RegisterResponse(
                user_id=existing_user["userId"],
                phone_number=existing_user["phoneNumber"],
                message="OTP sent to your phone number. User already exists."
            )
        except ClientError as e:
            print(f"Cognito error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP"
            )
    
    # Create new user in Cognito
    try:
        # Sign up user in Cognito
        cognito_response = cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=phone_number,
            Password=str(uuid.uuid4()),  # Random password (not used for phone auth)
            UserAttributes=[
                {"Name": "phone_number", "Value": phone_number}
            ]
        )
        
        cognito_user_sub = cognito_response["UserSub"]
        
        # Generate user ID
        user_id = str(uuid.uuid4())
        
        # Create user in DynamoDB
        success = create_user_in_db(
            user_id=user_id,
            phone_number=phone_number.replace("+91", ""),
            language=request.language,
            cognito_id=cognito_user_sub
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user in database"
            )
        
        # Initiate OTP authentication
        cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="CUSTOM_AUTH",
            AuthParameters={
                "USERNAME": phone_number
            }
        )
        
        return RegisterResponse(
            user_id=user_id,
            phone_number=phone_number.replace("+91", ""),
            message="OTP sent to your phone number"
        )
        
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        error_message = e.response.get("Error", {}).get("Message", "")
        
        print(f"Cognito error: {error_code} - {error_message}")
        
        if error_code == "UsernameExistsException":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {error_message}"
        )


@app.post("/verify-otp", response_model=VerifyOTPResponse)
async def verify_otp(request: VerifyOTPRequest):
    """
    Verify OTP and authenticate user
    Returns JWT tokens for authenticated session
    """
    phone_number = request.phone_number.strip()
    if not phone_number.startswith("+91"):
        phone_number = f"+91{phone_number}"
    
    try:
        # Verify OTP with Cognito
        auth_response = cognito_client.respond_to_auth_challenge(
            ClientId=COGNITO_CLIENT_ID,
            ChallengeName="CUSTOM_CHALLENGE",
            ChallengeResponses={
                "USERNAME": phone_number,
                "ANSWER": request.otp
            }
        )
        
        # Get authentication result
        auth_result = auth_response.get("AuthenticationResult")
        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP"
            )
        
        # Get user from database
        user = get_user_by_phone(phone_number.replace("+91", ""))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update last login timestamp
        update_last_login(user["userId"])
        
        return VerifyOTPResponse(
            user_id=user["userId"],
            access_token=auth_result["AccessToken"],
            refresh_token=auth_result.get("RefreshToken", ""),
            id_token=auth_result["IdToken"],
            message="Authentication successful"
        )
        
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        error_message = e.response.get("Error", {}).get("Message", "")
        
        print(f"Cognito error: {error_code} - {error_message}")
        
        if error_code == "NotAuthorizedException":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP or expired session"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OTP verification failed: {error_message}"
        )


@app.get("/profile", response_model=ProfileResponse)
async def get_profile(user_id: str):
    """
    Get user profile by user ID (passed as query parameter)
    """
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Parse profile data
    profile_data = user.get("profile", {})
    profile = UserProfile(**profile_data) if profile_data else None
    
    preferences_data = user.get("preferences", {})
    preferences = UserPreferences(**preferences_data) if preferences_data else UserPreferences()
    
    return ProfileResponse(
        user_id=user["userId"],
        phone_number=user["phoneNumber"],
        language=user.get("language", "en"),
        profile=profile,
        preferences=preferences,
        profile_strength=user.get("profileStrength", 0),
        created_at=user["createdAt"],
        updated_at=user["updatedAt"],
        last_login_at=user.get("lastLoginAt")
    )


@app.put("/profile", response_model=ProfileResponse)
async def update_profile(user_id: str, request: UpdateProfileRequest):
    """
    Update user profile (user_id passed as query parameter)
    """
    # Check if user exists
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Convert profile to dict
    profile_dict = request.profile.model_dump(exclude_none=True)
    
    # Update profile in database
    success = update_user_profile_in_db(user_id, profile_dict)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
    
    # Get updated user data
    updated_user = get_user_by_id(user_id)
    
    profile_data = updated_user.get("profile", {})
    profile = UserProfile(**profile_data) if profile_data else None
    
    preferences_data = updated_user.get("preferences", {})
    preferences = UserPreferences(**preferences_data) if preferences_data else UserPreferences()
    
    return ProfileResponse(
        user_id=updated_user["userId"],
        phone_number=updated_user["phoneNumber"],
        language=updated_user.get("language", "en"),
        profile=profile,
        preferences=preferences,
        profile_strength=updated_user.get("profileStrength", 0),
        created_at=updated_user["createdAt"],
        updated_at=updated_user["updatedAt"],
        last_login_at=updated_user.get("lastLoginAt")
    )


@app.get("/activity")
async def get_user_activity(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(20, ge=1, le=100, description="Number of activities to return"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type")
):
    """Get user activity log with optional filtering."""
    table = dynamodb.Table(get_table_name("activity_log"))
    
    try:
        if activity_type:
            # Query with type filter
            resp = table.query(
                IndexName="userId-type-index",
                KeyConditionExpression="userId = :uid AND #t = :type",
                ExpressionAttributeNames={"#t": "type"},
                ExpressionAttributeValues={":uid": user_id, ":type": activity_type},
                ScanIndexForward=False,  # Most recent first
                Limit=limit
            )
        else:
            # Query all activities for user
            resp = table.query(
                IndexName="userId-timestamp-index", 
                KeyConditionExpression="userId = :uid",
                ExpressionAttributeValues={":uid": user_id},
                ScanIndexForward=False,  # Most recent first
                Limit=limit
            )
    except Exception:
        # Fallback to scan if GSI doesn't exist
        resp = table.scan(
            FilterExpression="userId = :uid",
            ExpressionAttributeValues={":uid": user_id},
            Limit=limit
        )
        
    items = resp.get("Items", [])
    # Sort by timestamp desc if using scan fallback
    items.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return {
        "activities": items[:limit],
        "count": len(items)
    }


# Lambda handler
handler = Mangum(app, lifespan="off")
