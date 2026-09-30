"""
Scheme Service Lambda Handler - FastAPI endpoints for scheme management.
"""
import os
import sys
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from service import SchemeService

# Initialize FastAPI app
app = FastAPI(
    title="Scheme Service API",
    description="API for government welfare scheme management, eligibility checking, and recommendations",
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

# Initialize service
scheme_service = SchemeService()


# Request/Response models
class EligibilityCheckRequest(BaseModel):
    """Request model for eligibility check"""
    user_profile: dict


class EligibilityCheckResponse(BaseModel):
    """Response model for eligibility check"""
    scheme_id: str
    score: int
    match_reasons: List[str]
    missing_info: List[str]


class SaveSchemeRequest(BaseModel):
    """Request model for saving a scheme"""
    user_id: str


class SyncSchemeDataRequest(BaseModel):
    """Request model for syncing scheme data"""
    source_url: str


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "scheme-service"}


# GET /schemes - Search schemes with filters
@app.get("/schemes")
def get_schemes(
    state: Optional[str] = Query(None, description="State code (e.g., KA, MH)"),
    category: Optional[str] = Query(None, description="Scheme category"),
    is_active: bool = Query(True, description="Filter for active schemes only"),
    user_id: Optional[str] = Query(None, description="User ID for personalized results"),
    language: str = Query("en", description="Language code (en, hi, mr, kn, ta, te)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results")
):
    """
    Search schemes with filters
    
    Query Parameters:
    - state: State code filter (e.g., "KA", "MH", "ALL_INDIA")
    - category: Scheme category (education, health, agriculture, etc.)
    - is_active: Filter for active schemes only (default: true)
    - user_id: User ID for eligibility scoring
    - language: Language for multilingual content (default: en)
    - limit: Maximum number of results (1-100, default: 50)
    
    Returns:
    - List of schemes with multilingual content and eligibility scores
    """
    try:
        schemes = scheme_service.search_schemes(
            state=state,
            category=category,
            is_active=is_active,
            user_id=user_id,
            language=language,
            limit=limit
        )
        
        return {
            "success": True,
            "count": len(schemes),
            "schemes": schemes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching schemes: {str(e)}")


# GET /schemes/{scheme_id} - Get scheme details
@app.get("/schemes/{scheme_id}")
def get_scheme(
    scheme_id: str,
    language: str = Query("en", description="Language code (en, hi, mr, kn, ta, te)"),
    user_id: Optional[str] = Query(None, description="User ID for eligibility calculation")
):
    """
    Get scheme details by ID
    
    Path Parameters:
    - scheme_id: Unique scheme identifier
    
    Query Parameters:
    - language: Language for multilingual content (default: en)
    - user_id: User ID for eligibility calculation
    
    Returns:
    - Scheme details with multilingual content and eligibility score
    """
    try:
        scheme = scheme_service.get_scheme_by_id(
            scheme_id=scheme_id,
            language=language,
            user_id=user_id
        )
        
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        
        return {
            "success": True,
            "scheme": scheme
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scheme: {str(e)}")


# POST /schemes/{scheme_id}/check-eligibility - Check eligibility
@app.post("/schemes/{scheme_id}/check-eligibility", response_model=EligibilityCheckResponse)
def check_eligibility(
    scheme_id: str,
    request: EligibilityCheckRequest
):
    """
    Check user eligibility for a scheme
    
    Path Parameters:
    - scheme_id: Unique scheme identifier
    
    Request Body:
    - user_profile: User profile data (age, gender, income, category, state, etc.)
    
    Returns:
    - Eligibility score (0-100)
    - Match reasons (why user is eligible)
    - Missing information (what's needed for full eligibility)
    """
    try:
        eligibility = scheme_service.check_eligibility(
            scheme_id=scheme_id,
            user_profile=request.user_profile
        )
        
        return EligibilityCheckResponse(
            scheme_id=scheme_id,
            score=eligibility["score"],
            match_reasons=eligibility["match_reasons"],
            missing_info=eligibility["missing_info"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking eligibility: {str(e)}")


# POST /schemes/{scheme_id}/save - Save scheme to user's saved list
@app.post("/schemes/{scheme_id}/save")
def save_scheme(
    scheme_id: str,
    request: SaveSchemeRequest
):
    """
    Save scheme to user's saved list
    
    Path Parameters:
    - scheme_id: Unique scheme identifier
    
    Request Body:
    - user_id: User identifier
    
    Returns:
    - Success status
    """
    try:
        # Get user profile
        user_profile = scheme_service._get_user_profile(request.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current saved schemes
        saved_schemes = user_profile.get("saved_schemes", [])
        
        # Add scheme if not already saved
        if scheme_id not in saved_schemes:
            saved_schemes.append(scheme_id)

            # Update user profile — partition key is userId (camelCase per DynamoDB schema)
            scheme_service.user_profile_table.update_item(
                Key={"userId": request.user_id},
                UpdateExpression="SET saved_schemes = :schemes",
                ExpressionAttributeValues={":schemes": saved_schemes}
            )
        
        return {
            "success": True,
            "message": "Scheme saved successfully",
            "scheme_id": scheme_id,
            "saved_schemes_count": len(saved_schemes)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving scheme: {str(e)}")


# GET /schemes/recommendations - Get personalized recommendations
@app.get("/schemes/recommendations")
def get_recommendations(
    user_id: str = Query(..., description="User identifier"),
    state: Optional[str] = Query(None, description="State code filter"),
    language: str = Query("en", description="Language code"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations")
):
    """
    Get personalized scheme recommendations
    
    Query Parameters:
    - user_id: User identifier (required)
    - state: Optional state filter (uses user's state if not provided)
    - language: Language for multilingual content (default: en)
    - limit: Maximum number of recommendations (1-50, default: 10)
    
    Returns:
    - List of recommended schemes sorted by eligibility score
    """
    try:
        recommendations = scheme_service.get_recommendations(
            user_id=user_id,
            state=state,
            limit=limit
        )
        
        return {
            "success": True,
            "count": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")


# POST /schemes/sync - Sync scheme data from government APIs
@app.post("/schemes/sync")
def sync_scheme_data(request: SyncSchemeDataRequest):
    """
    Sync scheme data from government APIs
    
    Request Body:
    - source_url: Government API URL
    
    Returns:
    - Sync statistics (schemes added, updated, deactivated)
    
    Note: This endpoint should be protected and only accessible to admin users
    """
    try:
        result = scheme_service.sync_scheme_data(source_url=request.source_url)
        
        return {
            "success": True,
            "sync_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing scheme data: {str(e)}")


# POST /schemes/{scheme_id}/eligibility-explanation - Get detailed eligibility explanation
@app.post("/schemes/{scheme_id}/eligibility-explanation")
def get_eligibility_explanation(
    scheme_id: str,
    request: EligibilityCheckRequest,
    language: str = Query("en", description="Language code")
):
    """
    Get detailed eligibility explanation with status determination
    
    Path Parameters:
    - scheme_id: Unique scheme identifier
    
    Request Body:
    - user_profile: User profile data
    
    Query Parameters:
    - language: Language for multilingual content (default: en)
    
    Returns:
    - Structured eligibility explanation with status (ELIGIBLE, LIKELY_ELIGIBLE, NEEDS_VERIFICATION, NOT_ELIGIBLE)
    - Matched conditions
    - Match reasons
    - Missing information
    - Verification required items
    - Eligibility criteria summary
    """
    try:
        # Get scheme
        scheme = scheme_service.get_scheme_by_id(scheme_id, language=language)
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        
        # Check eligibility
        eligibility = scheme_service.check_eligibility(
            scheme_id=scheme_id,
            user_profile=request.user_profile
        )
        
        # Determine status from score
        score = eligibility["score"]
        if score >= 80:
            status = "ELIGIBLE"
        elif score >= 60:
            status = "LIKELY_ELIGIBLE"
        elif score >= 40:
            status = "NEEDS_VERIFICATION"
        else:
            status = "NOT_ELIGIBLE"
        
        # Build matched conditions list
        matched_conditions = []
        if eligibility["match_reasons"]:
            matched_conditions = eligibility["match_reasons"]
        
        # Build verification required list (items in missing_info that are critical)
        verification_required = []
        for item in eligibility["missing_info"]:
            if "not provided" in item.lower():
                verification_required.append(item)
        
        # Get eligibility criteria summary
        criteria = scheme.get("eligibility_criteria", {})
        criteria_summary = {
            "age_range": f"{criteria.get('min_age', 0)}-{criteria.get('max_age', '∞')}",
            "eligible_genders": criteria.get("gender", ["ALL"]),
            "income_limit": criteria.get("income_limit"),
            "eligible_categories": criteria.get("categories", ["ALL"]),
            "eligible_states": criteria.get("states", ["ALL"])
        }
        
        return {
            "success": True,
            "explanation": {
                "scheme_id": scheme_id,
                "scheme_name": scheme.get("name", {}),
                "status": status,
                "score": score,
                "matched_conditions": matched_conditions,
                "match_reasons": eligibility["match_reasons"],
                "missing_information": eligibility["missing_info"],
                "verification_required": verification_required,
                "eligibility_criteria_summary": criteria_summary
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating eligibility explanation: {str(e)}")


# POST /schemes/{scheme_id}/action-plan - Generate citizen action plan

class ActionPlanRequest(BaseModel):
    """Request body for action plan generation"""
    user_profile: dict
    available_documents: Optional[List[str]] = []
    language: str = "en"


@app.post("/schemes/{scheme_id}/action-plan")
def generate_action_plan(
    scheme_id: str,
    request: ActionPlanRequest,
):
    """
    Generate actionable citizen plan for scheme application
    
    Path Parameters:
    - scheme_id: Unique scheme identifier
    
    Query Parameters:
    - available_documents: List of documents user currently has
    - language: Language for multilingual content (default: en)
    
    Request Body:
    - User profile data for eligibility check
    
    Returns:
    - Complete action plan with:
      - Eligibility status
      - Required vs available documents
      - Missing documents
      - Step-by-step action items
      - Application method
      - Portal URL
      - Estimated time
      - Helpful notes
    """
    try:
        from action_plan_generator import ActionPlanGenerator
        
        # Get scheme
        scheme = scheme_service.get_scheme_by_id(scheme_id, language=request.language)
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        
        # Check eligibility
        eligibility = scheme_service.check_eligibility(
            scheme_id=scheme_id,
            user_profile=request.user_profile
        )
        
        # Generate action plan
        action_plan_gen = ActionPlanGenerator()
        action_plan = action_plan_gen.generate_action_plan(
            scheme=scheme,
            eligibility=eligibility,
            available_documents=request.available_documents,
            language=request.language
        )
        
        return {
            "success": True,
            "action_plan": action_plan
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating action plan: {str(e)}")


# Lambda handler
handler = Mangum(app, lifespan="off")
