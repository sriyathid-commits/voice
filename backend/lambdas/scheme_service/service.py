"""
Scheme Service - Business logic for scheme management, eligibility checking, and recommendations.
"""
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Import shared models and utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.models import Scheme, EligibilityCriteria, UserProfile
from shared.utils import (
    get_dynamodb_resource, get_bedrock_client, get_table_name,
    get_multilingual_text, calculate_profile_strength
)
from shared.constants import SUPPORTED_LANGUAGES, BEDROCK_MODELS


class SchemeService:
    """Service for managing government welfare schemes"""
    
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.bedrock = get_bedrock_client()
        self.schemes_table = self.dynamodb.Table(get_table_name("schemes"))
        self.users_table = self.dynamodb.Table(get_table_name("users"))
        self.user_profile_table = self.dynamodb.Table(get_table_name("user_profile"))
        
        # Initialize Redis cache if available
        self.cache = None
        try:
            import redis
            redis_host = os.getenv("REDIS_HOST")
            if redis_host:
                self.cache = redis.Redis(
                    host=redis_host,
                    port=int(os.getenv("REDIS_PORT", "6379")),
                    db=0,
                    decode_responses=True
                )
        except Exception as e:
            print(f"Redis cache not available: {e}")
    
    def search_schemes(
        self,
        state: Optional[str] = None,
        category: Optional[str] = None,
        is_active: bool = True,
        user_id: Optional[str] = None,
        language: str = "en",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search schemes with filters
        
        Args:
            state: State code filter (e.g., "KA", "MH")
            category: Scheme category filter
            is_active: Filter for active schemes only
            user_id: User ID for personalized results
            language: Language for multilingual content
            limit: Maximum number of results
        
        Returns:
            List of scheme dictionaries
        """
        # Try cache first
        cache_key = f"schemes:{state}:{category}:{is_active}:{language}"
        if self.cache:
            try:
                cached = self.cache.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception as e:
                print(f"Cache read error: {e}")
        
        # Build query
        filter_expression = None
        
        if is_active:
            filter_expression = Attr("is_active").eq(True)
        
        # Query by state and category using GSI
        if state and category:
            response = self.schemes_table.query(
                IndexName="state-category-index",
                KeyConditionExpression=Key("state").eq(state.upper()) & Key("category").eq(category.lower()),
                FilterExpression=filter_expression,
                Limit=limit
            )
        elif state:
            response = self.schemes_table.query(
                IndexName="state-category-index",
                KeyConditionExpression=Key("state").eq(state.upper()),
                FilterExpression=filter_expression,
                Limit=limit
            )
        else:
            # Scan if no state specified (less efficient)
            scan_params = {"Limit": limit}
            if filter_expression:
                scan_params["FilterExpression"] = filter_expression
            response = self.schemes_table.scan(**scan_params)
        
        schemes = response.get("Items", [])
        
        # Convert DynamoDB Decimal to float
        schemes = self._convert_decimals(schemes)
        
        # Get user profile for eligibility scoring if user_id provided
        user_profile = None
        if user_id:
            user_profile = self._get_user_profile(user_id)
        
        # Format schemes with multilingual content and eligibility scores
        formatted_schemes = []
        for scheme in schemes:
            formatted = self._format_scheme(scheme, language, user_profile)
            formatted_schemes.append(formatted)
        
        # Sort by eligibility score if available
        if user_profile:
            formatted_schemes.sort(key=lambda x: x.get("eligibility_score", 0), reverse=True)
        
        # Cache results
        if self.cache:
            try:
                self.cache.setex(cache_key, 3600, json.dumps(formatted_schemes))
            except Exception as e:
                print(f"Cache write error: {e}")
        
        return formatted_schemes
    
    def get_scheme_by_id(
        self,
        scheme_id: str,
        language: str = "en",
        user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get scheme details by ID
        
        Args:
            scheme_id: Scheme identifier
            language: Language for multilingual content
            user_id: User ID for eligibility calculation
        
        Returns:
            Scheme dictionary or None if not found
        """
        # Try cache first
        cache_key = f"scheme:{scheme_id}:{language}"
        if self.cache:
            try:
                cached = self.cache.get(cache_key)
                if cached:
                    scheme = json.loads(cached)
                    # Calculate eligibility if user_id provided
                    if user_id:
                        user_profile = self._get_user_profile(user_id)
                        if user_profile:
                            eligibility = self.check_eligibility(scheme_id, user_profile)
                            scheme["eligibility_score"] = eligibility["score"]
                            scheme["match_reasons"] = eligibility["match_reasons"]
                            scheme["missing_info"] = eligibility["missing_info"]
                    return scheme
            except Exception as e:
                print(f"Cache read error: {e}")
        
        # Query DynamoDB
        response = self.schemes_table.get_item(Key={"scheme_id": scheme_id})
        
        if "Item" not in response:
            return None
        
        scheme = self._convert_decimals(response["Item"])
        
        # Get user profile for eligibility
        user_profile = None
        if user_id:
            user_profile = self._get_user_profile(user_id)
        
        formatted = self._format_scheme(scheme, language, user_profile)
        
        # Cache result
        if self.cache:
            try:
                self.cache.setex(cache_key, 3600, json.dumps(formatted))
            except Exception as e:
                print(f"Cache write error: {e}")
        
        return formatted
    
    def check_eligibility(
        self,
        scheme_id: str,
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check user eligibility for a scheme
        
        Args:
            scheme_id: Scheme identifier
            user_profile: User profile data
        
        Returns:
            Dictionary with score (0-100), match_reasons, and missing_info
        """
        # Get scheme
        response = self.schemes_table.get_item(Key={"scheme_id": scheme_id})
        if "Item" not in response:
            return {
                "score": 0,
                "match_reasons": [],
                "missing_info": ["Scheme not found"]
            }
        
        scheme = self._convert_decimals(response["Item"])
        criteria = scheme.get("eligibility_criteria", {})
        
        score = 0
        max_score = 0
        match_reasons = []
        missing_info = []
        
        # Check age (20 points)
        max_score += 20
        user_age = self._calculate_age(user_profile.get("date_of_birth"))
        min_age = criteria.get("min_age")
        max_age = criteria.get("max_age")
        
        if user_age is None:
            missing_info.append("Date of birth not provided")
        elif min_age is not None or max_age is not None:
            if (min_age is None or user_age >= min_age) and (max_age is None or user_age <= max_age):
                score += 20
                age_range = f"{min_age or 0}-{max_age or '∞'}"
                match_reasons.append(f"Age {user_age} is within eligible range ({age_range})")
            else:
                age_range = f"{min_age or 0}-{max_age or '∞'}"
                missing_info.append(f"Age {user_age} is outside eligible range ({age_range})")
        else:
            score += 20  # No age restriction
        
        # Check gender (15 points)
        max_score += 15
        user_gender = user_profile.get("gender")
        eligible_genders = criteria.get("gender", [])
        
        if not user_gender:
            missing_info.append("Gender not provided")
        elif not eligible_genders or "ALL" in eligible_genders:
            score += 15
        elif user_gender.upper() in [g.upper() for g in eligible_genders]:
            score += 15
            match_reasons.append(f"Gender {user_gender} is eligible")
        else:
            missing_info.append(f"Gender {user_gender} is not eligible (required: {', '.join(eligible_genders)})")
        
        # Check income (25 points)
        max_score += 25
        user_income = user_profile.get("income")
        income_limit = criteria.get("income_limit")
        
        if income_limit is not None:
            if user_income is None:
                missing_info.append("Income information not provided")
            elif user_income <= income_limit:
                score += 25
                match_reasons.append(f"Income ₹{user_income:,.0f} is below limit of ₹{income_limit:,.0f}")
            else:
                missing_info.append(f"Income ₹{user_income:,.0f} exceeds limit of ₹{income_limit:,.0f}")
        else:
            score += 25  # No income restriction
        
        # Check category (20 points)
        max_score += 20
        user_category = user_profile.get("category")
        eligible_categories = criteria.get("categories", [])
        
        if not user_category:
            missing_info.append("Social category not provided")
        elif not eligible_categories or "ALL" in eligible_categories:
            score += 20
        elif user_category.upper() in [c.upper() for c in eligible_categories]:
            score += 20
            match_reasons.append(f"Category {user_category} is eligible")
        else:
            missing_info.append(f"Category {user_category} is not eligible (required: {', '.join(eligible_categories)})")
        
        # Check state (20 points)
        max_score += 20
        user_state = user_profile.get("state")
        scheme_state = scheme.get("state")
        eligible_states = criteria.get("states", [])
        
        if not user_state:
            missing_info.append("State not provided")
        elif scheme_state == "ALL_INDIA" or "ALL_INDIA" in eligible_states:
            score += 20
            match_reasons.append("Scheme is available nationwide")
        elif user_state.upper() == scheme_state.upper() or user_state.upper() in [s.upper() for s in eligible_states]:
            score += 20
            match_reasons.append(f"Scheme is available in {user_state}")
        else:
            missing_info.append(f"Scheme not available in {user_state}")
        
        # Evaluate custom rules (bonus points, not counted in max_score)
        custom_rules = criteria.get("custom_rules", [])
        for rule in custom_rules:
            rule_result = self._evaluate_rule(rule, user_profile)
            if rule_result["matched"]:
                score += 5  # Bonus points for matching custom rules
                match_reasons.append(rule_result["reason"])
        
        # Calculate final score as percentage
        final_score = int((score / max_score) * 100) if max_score > 0 else 0
        
        return {
            "score": final_score,
            "match_reasons": match_reasons,
            "missing_info": missing_info
        }
    
    def get_recommendations(
        self,
        user_id: str,
        state: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get personalized scheme recommendations using Bedrock embeddings
        
        Args:
            user_id: User identifier
            state: Optional state filter
            limit: Maximum number of recommendations
        
        Returns:
            List of recommended schemes
        """
        # Get user profile
        user_profile = self._get_user_profile(user_id)
        if not user_profile:
            return []
        
        # Use state from profile if not provided
        if not state:
            state = user_profile.get("state")
        
        # Get all schemes for the state
        schemes = self.search_schemes(
            state=state,
            is_active=True,
            user_id=user_id,
            limit=100
        )
        
        # Filter schemes with eligibility score > 50
        eligible_schemes = [s for s in schemes if s.get("eligibility_score", 0) >= 50]
        
        # Sort by eligibility score
        eligible_schemes.sort(key=lambda x: x.get("eligibility_score", 0), reverse=True)
        
        return eligible_schemes[:limit]
    
    def sync_scheme_data(self, source_url: str) -> Dict[str, Any]:
        """
        Sync scheme data from government API
        
        Args:
            source_url: Government API URL
        
        Returns:
            Dictionary with sync statistics
        """
        # This is a placeholder for government API integration
        # In production, this would fetch data from external APIs
        
        return {
            "status": "success",
            "message": "Scheme sync not yet implemented",
            "schemes_added": 0,
            "schemes_updated": 0,
            "schemes_deactivated": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from DynamoDB"""
        try:
            # Try user_profile table first
            response = self.user_profile_table.get_item(Key={"user_id": user_id})
            if "Item" in response:
                return self._convert_decimals(response["Item"])
            
            # Fallback to users table
            response = self.users_table.get_item(Key={"user_id": user_id})
            if "Item" in response:
                user = self._convert_decimals(response["Item"])
                return user.get("profile", {})
            
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def _format_scheme(
        self,
        scheme: Dict[str, Any],
        language: str,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Format scheme with multilingual content and eligibility score"""
        formatted = {
            "scheme_id": scheme.get("scheme_id"),
            "name": get_multilingual_text(scheme.get("name", {}), language),
            "description": get_multilingual_text(scheme.get("description", {}), language),
            "state": scheme.get("state"),
            "category": scheme.get("category"),
            "benefits": get_multilingual_text(scheme.get("benefits", {}), language),
            "application_process": scheme.get("application_process", {}).get(language, []),
            "required_documents": scheme.get("required_documents", []),
            "portal_url": scheme.get("portal_url"),
            "portal_status": scheme.get("portal_status"),
            "is_active": scheme.get("is_active", True),
            "last_synced_at": scheme.get("last_synced_at")
        }
        
        # Add eligibility information if user profile provided
        if user_profile:
            eligibility = self.check_eligibility(scheme.get("scheme_id"), user_profile)
            formatted["eligibility_score"] = eligibility["score"]
            formatted["match_reasons"] = eligibility["match_reasons"]
            formatted["missing_info"] = eligibility["missing_info"]
        
        return formatted
    
    def _calculate_age(self, date_of_birth: Any) -> Optional[int]:
        """Calculate age from date of birth"""
        if not date_of_birth:
            return None
        
        try:
            # Handle different date formats
            if isinstance(date_of_birth, str):
                dob = datetime.fromisoformat(date_of_birth.replace('Z', '+00:00')).date()
            elif isinstance(date_of_birth, datetime):
                dob = date_of_birth.date()
            elif isinstance(date_of_birth, date):
                dob = date_of_birth
            else:
                return None
            
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return age
        except Exception as e:
            print(f"Error calculating age: {e}")
            return None
    
    def _evaluate_rule(self, rule: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a custom eligibility rule"""
        field = rule.get("field")
        operator = rule.get("operator")
        value = rule.get("value")
        
        user_value = user_profile.get(field)
        
        if user_value is None:
            return {"matched": False, "reason": f"Missing field: {field}"}
        
        matched = False
        reason = ""
        
        try:
            if operator == "eq":
                matched = user_value == value
                reason = f"{field} equals {value}"
            elif operator == "ne":
                matched = user_value != value
                reason = f"{field} does not equal {value}"
            elif operator == "gt":
                matched = float(user_value) > float(value)
                reason = f"{field} ({user_value}) is greater than {value}"
            elif operator == "lt":
                matched = float(user_value) < float(value)
                reason = f"{field} ({user_value}) is less than {value}"
            elif operator == "gte":
                matched = float(user_value) >= float(value)
                reason = f"{field} ({user_value}) is greater than or equal to {value}"
            elif operator == "lte":
                matched = float(user_value) <= float(value)
                reason = f"{field} ({user_value}) is less than or equal to {value}"
            elif operator == "in":
                matched = user_value in value if isinstance(value, list) else False
                reason = f"{field} ({user_value}) is in allowed values"
            elif operator == "not_in":
                matched = user_value not in value if isinstance(value, list) else True
                reason = f"{field} ({user_value}) is not in excluded values"
            elif operator == "contains":
                matched = value in str(user_value)
                reason = f"{field} contains {value}"
            elif operator == "not_contains":
                matched = value not in str(user_value)
                reason = f"{field} does not contain {value}"
        except Exception as e:
            print(f"Error evaluating rule: {e}")
            return {"matched": False, "reason": f"Error evaluating rule for {field}"}
        
        return {"matched": matched, "reason": reason}
    
    def _convert_decimals(self, obj: Any) -> Any:
        """Convert DynamoDB Decimal types to float/int"""
        if isinstance(obj, list):
            return [self._convert_decimals(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._convert_decimals(value) for key, value in obj.items()}
        elif isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        else:
            return obj
