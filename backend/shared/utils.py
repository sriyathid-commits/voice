"""
Shared utility functions for Voice for Bharat backend services.
"""
import os
import boto3
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json


def get_dynamodb_client():
    """Get DynamoDB client"""
    return boto3.client("dynamodb", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_dynamodb_resource():
    """Get DynamoDB resource"""
    return boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_s3_client():
    """Get S3 client"""
    return boto3.client("s3", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_bedrock_client():
    """Get Bedrock client"""
    return boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_cognito_client():
    """Get Cognito client"""
    return boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_sns_client():
    """Get SNS client"""
    return boto3.client("sns", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def get_eventbridge_client():
    """Get EventBridge client"""
    return boto3.client("events", region_name=os.getenv("AWS_REGION", "ap-south-1"))


def generate_presigned_url(bucket: str, key: str, expiration: int = 900) -> str:
    """
    Generate presigned URL for S3 object
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
        expiration: URL expiration time in seconds (default: 15 minutes)
    
    Returns:
        Presigned URL string
    """
    s3_client = get_s3_client()
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration
    )
    return url


def generate_presigned_post(bucket: str, key: str, expiration: int = 900, 
                           max_size: int = 5242880) -> Dict[str, Any]:
    """
    Generate presigned POST for direct browser upload to S3
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
        expiration: URL expiration time in seconds (default: 15 minutes)
        max_size: Maximum file size in bytes (default: 5MB)
    
    Returns:
        Dictionary with url and fields for POST request
    """
    s3_client = get_s3_client()
    response = s3_client.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        ExpiresIn=expiration,
        Conditions=[
            ["content-length-range", 0, max_size]
        ]
    )
    return response


def get_document_s3_key(user_id: str, document_type: str, document_id: str, 
                       extension: str = "pdf") -> str:
    """
    Generate S3 key for user document
    
    Args:
        user_id: User ID
        document_type: Document type (aadhaar, pan, income-certificate, etc.)
        document_id: Unique document ID
        extension: File extension (default: pdf)
    
    Returns:
        S3 key string
    """
    return f"users/{user_id}/{document_type}/{document_id}.{extension}"


def get_application_document_s3_key(application_id: str, document_type: str, 
                                   document_id: str, extension: str = "pdf") -> str:
    """
    Generate S3 key for application document
    
    Args:
        application_id: Application ID
        document_type: Document type
        document_id: Unique document ID
        extension: File extension (default: pdf)
    
    Returns:
        S3 key string
    """
    return f"applications/{application_id}/{document_type}/{document_id}.{extension}"


def get_audio_s3_key(session_id: str, role: str, message_id: str, 
                    extension: str = "wav") -> str:
    """
    Generate S3 key for conversation audio
    
    Args:
        session_id: Conversation session ID
        role: Message role (user or assistant)
        message_id: Unique message ID
        extension: File extension (wav for user, mp3 for assistant)
    
    Returns:
        S3 key string
    """
    return f"conversations/{session_id}/{role}/{message_id}.{extension}"


def get_tts_cache_s3_key(language: str, text_hash: str) -> str:
    """
    Generate S3 key for TTS cache
    
    Args:
        language: Language code (en, hi, mr, etc.)
        text_hash: SHA256 hash of text
    
    Returns:
        S3 key string
    """
    return f"tts-cache/{language}/{text_hash}.mp3"


def get_stt_recording_s3_key(user_id: str, timestamp: str) -> str:
    """
    Generate S3 key for STT recording
    
    Args:
        user_id: User ID
        timestamp: ISO 8601 timestamp
    
    Returns:
        S3 key string
    """
    return f"stt-recordings/{user_id}/{timestamp}.wav"


def upload_to_s3(bucket: str, key: str, data: bytes, 
                content_type: str = "application/octet-stream",
                metadata: Optional[Dict[str, str]] = None) -> bool:
    """
    Upload data to S3
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
        data: Binary data to upload
        content_type: Content type (default: application/octet-stream)
        metadata: Optional metadata dictionary
    
    Returns:
        True if successful, False otherwise
    """
    try:
        s3_client = get_s3_client()
        params = {
            "Bucket": bucket,
            "Key": key,
            "Body": data,
            "ContentType": content_type
        }
        if metadata:
            params["Metadata"] = metadata
        
        s3_client.put_object(**params)
        return True
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False


def download_from_s3(bucket: str, key: str) -> Optional[bytes]:
    """
    Download data from S3
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
    
    Returns:
        Binary data if successful, None otherwise
    """
    try:
        s3_client = get_s3_client()
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()
    except Exception as e:
        print(f"Error downloading from S3: {e}")
        return None


def delete_from_s3(bucket: str, key: str) -> bool:
    """
    Delete object from S3
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
    
    Returns:
        True if successful, False otherwise
    """
    try:
        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=bucket, Key=key)
        return True
    except Exception as e:
        print(f"Error deleting from S3: {e}")
        return False


def check_s3_object_exists(bucket: str, key: str) -> bool:
    """
    Check if S3 object exists
    
    Args:
        bucket: S3 bucket name
        key: S3 object key
    
    Returns:
        True if exists, False otherwise
    """
    try:
        s3_client = get_s3_client()
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except Exception:
        return False


def calculate_profile_strength(profile: Dict[str, Any]) -> int:
    """
    Calculate user profile strength percentage (0-100)
    
    Args:
        profile: User profile dictionary
    
    Returns:
        Profile strength percentage
    """
    required_fields = [
        "name", "date_of_birth", "gender", "state", 
        "district", "income", "category"
    ]
    document_fields = ["aadhaar_number", "pan_number", "bank_account"]
    
    # Check required fields (70% weight)
    filled_required = sum(1 for field in required_fields if profile.get(field))
    required_score = (filled_required / len(required_fields)) * 70
    
    # Check document fields (30% weight)
    filled_documents = sum(1 for field in document_fields if profile.get(field))
    document_score = (filled_documents / len(document_fields)) * 30
    
    return int(required_score + document_score)


def get_table_name(base_name: str) -> str:
    """
    Get full DynamoDB table name with environment prefix
    
    Args:
        base_name: Base table name (e.g., "users", "schemes")
    
    Returns:
        Full table name with prefix
    """
    prefix = os.getenv("DYNAMODB_TABLE_PREFIX", "voice-for-bharat")
    return f"{prefix}-{base_name}"


def hash_text(text: str) -> str:
    """
    Generate hash for text (used for TTS cache keys)
    
    Args:
        text: Text to hash
    
    Returns:
        SHA256 hash string
    """
    return hashlib.sha256(text.encode()).hexdigest()


def get_multilingual_text(text_dict: Dict[str, str], language: str = "en") -> str:
    """
    Get text in specified language with fallback to English
    
    Args:
        text_dict: Dictionary with language codes as keys
        language: Desired language code
    
    Returns:
        Text in specified language or English fallback
    """
    return text_dict.get(language, text_dict.get("en", ""))


def validate_indian_phone(phone: str) -> bool:
    """
    Validate Indian phone number format
    
    Args:
        phone: Phone number string
    
    Returns:
        True if valid, False otherwise
    """
    import re
    return bool(re.match(r"^[6-9]\d{9}$", phone))


def validate_aadhaar(aadhaar: str) -> bool:
    """
    Validate Aadhaar number format
    
    Args:
        aadhaar: Aadhaar number string
    
    Returns:
        True if valid, False otherwise
    """
    import re
    return bool(re.match(r"^\d{12}$", aadhaar))


def validate_pan(pan: str) -> bool:
    """
    Validate PAN number format
    
    Args:
        pan: PAN number string
    
    Returns:
        True if valid, False otherwise
    """
    import re
    return bool(re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", pan.upper()))


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime to ISO 8601 string
    
    Args:
        dt: Datetime object
    
    Returns:
        ISO 8601 formatted string
    """
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO 8601 timestamp string
    
    Args:
        timestamp_str: ISO 8601 formatted string
    
    Returns:
        Datetime object
    """
    return datetime.fromisoformat(timestamp_str)
