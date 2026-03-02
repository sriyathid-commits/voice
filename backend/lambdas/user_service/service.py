"""
User Service Business Logic
Contains core functions for user management operations.
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError

import sys
import os
sys.path.append('/opt/python')
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from utils import (
    get_dynamodb_resource,
    get_cognito_client,
    get_table_name,
    calculate_profile_strength
)


class UserService:
    """User service for managing user operations"""
    
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.cognito_client = get_cognito_client()
        self.users_table = self.dynamodb.Table(get_table_name("users"))
    
    def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Get user by phone number from DynamoDB
        
        Args:
            phone_number: 10-digit phone number (without +91)
        
        Returns:
            User dict if found, None otherwise
        """
        try:
            response = self.users_table.query(
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
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by user_id from DynamoDB
        
        Args:
            user_id: User UUID
        
        Returns:
            User dict if found, None otherwise
        """
        try:
            response = self.users_table.get_item(Key={"userId": user_id})
            return response.get("Item")
        except ClientError as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def create_user(
        self,
        user_id: str,
        phone_number: str,
        language: str,
        cognito_id: str
    ) -> bool:
        """
        Create user in DynamoDB
        
        Args:
            user_id: Generated UUID for user
            phone_number: 10-digit phone number (without +91)
            language: Preferred language code
            cognito_id: Cognito user sub
        
        Returns:
            True if successful, False otherwise
        """
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
            self.users_table.put_item(Item=user_item)
            return True
        except ClientError as e:
            print(f"Error creating user in DB: {e}")
            return False
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Update user profile in DynamoDB
        
        Args:
            user_id: User UUID
            profile_data: Profile data dictionary
        
        Returns:
            True if successful, False otherwise
        """
        # Calculate profile strength
        profile_strength = calculate_profile_strength(profile_data)
        
        now = datetime.utcnow().isoformat()
        
        try:
            self.users_table.update_item(
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
    
    def update_last_login(self, user_id: str) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User UUID
        
        Returns:
            True if successful, False otherwise
        """
        now = datetime.utcnow().isoformat()
        
        try:
            self.users_table.update_item(
                Key={"userId": user_id},
                UpdateExpression="SET lastLoginAt = :login_time",
                ExpressionAttributeValues={":login_time": now}
            )
            return True
        except ClientError as e:
            print(f"Error updating last login: {e}")
            return False
    
    def register_with_cognito(
        self,
        phone_number: str,
        client_id: str
    ) -> Dict[str, Any]:
        """
        Register user with AWS Cognito
        
        Args:
            phone_number: Phone number with +91 prefix
            client_id: Cognito client ID
        
        Returns:
            Dict with UserSub and other Cognito response data
        
        Raises:
            ClientError: If Cognito operation fails
        """
        response = self.cognito_client.sign_up(
            ClientId=client_id,
            Username=phone_number,
            Password=str(uuid.uuid4()),  # Random password (not used for phone auth)
            UserAttributes=[
                {"Name": "phone_number", "Value": phone_number}
            ]
        )
        return response
    
    def initiate_otp(self, phone_number: str, client_id: str) -> Dict[str, Any]:
        """
        Initiate OTP authentication with Cognito
        
        Args:
            phone_number: Phone number with +91 prefix
            client_id: Cognito client ID
        
        Returns:
            Cognito auth response
        
        Raises:
            ClientError: If Cognito operation fails
        """
        response = self.cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow="CUSTOM_AUTH",
            AuthParameters={
                "USERNAME": phone_number
            }
        )
        return response
    
    def verify_otp(
        self,
        phone_number: str,
        otp: str,
        client_id: str
    ) -> Dict[str, Any]:
        """
        Verify OTP with Cognito
        
        Args:
            phone_number: Phone number with +91 prefix
            otp: 6-digit OTP code
            client_id: Cognito client ID
        
        Returns:
            Cognito auth response with tokens
        
        Raises:
            ClientError: If OTP verification fails
        """
        response = self.cognito_client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName="CUSTOM_CHALLENGE",
            ChallengeResponses={
                "USERNAME": phone_number,
                "ANSWER": otp
            }
        )
        return response
