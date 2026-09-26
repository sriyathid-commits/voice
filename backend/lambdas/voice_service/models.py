"""
Voice Service Models - Conversational Context & Citizen Profile
Enhanced for PS6: AI for Bharat in Indian Languages
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class CitizenProfile(BaseModel):
    """Temporary citizen profile built during conversation"""
    user_id: Optional[str] = None
    language: str = "en"
    state: Optional[str] = None
    district: Optional[str] = None
    age: Optional[int] = None
    occupation: Optional[str] = None
    income_range: Optional[str] = None
    gender: Optional[str] = None
    is_farmer: Optional[bool] = None
    is_student: Optional[bool] = None
    has_land: Optional[bool] = None
    has_disability: Optional[bool] = None
    available_documents: List[str] = Field(default_factory=list)
    current_scheme_context: Optional[str] = None
    current_application_context: Optional[str] = None


class ConversationMessage(BaseModel):
    """Single message in conversation"""
    message_id: str
    role: str  # USER, ASSISTANT, SYSTEM
    content: str
    audio_url: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    intent: Optional[str] = None
    entities: Dict[str, Any] = Field(default_factory=dict)


class ConversationSession(BaseModel):
    """Conversation session with context"""
    session_id: str
    user_id: str
    language: str = "en"
    citizen_profile: CitizenProfile = Field(default_factory=CitizenProfile)
    messages: List[ConversationMessage] = Field(default_factory=list)
    current_intent: Optional[str] = None
    conversation_state: str = "READY"  # READY, SEARCHING_SCHEMES, CHECKING_ELIGIBILITY, etc.
    matched_schemes: List[str] = Field(default_factory=list)
    started_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_activity_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_active: bool = True


# Legacy models kept for backward compatibility
class VoiceQueryRequest(BaseModel):
    """Voice query request model"""
    session_id: str = Field(..., description="Conversation session ID")
    user_id: str = Field(..., description="User ID")
    language: str = Field(default="en", description="Language code")


class VoiceQueryResponse(BaseModel):
    """Voice query response model"""
    text: str = Field(..., description="Response text")
    audio_url: Optional[str] = Field(None, description="Audio file URL")
    context: Dict[str, Any] = Field(default_factory=dict, description="Conversation context")
    schemes: List[Dict[str, Any]] = Field(default_factory=list, description="Matching schemes")


class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str = Field(..., description="Message type (start, audio, stop, ping)")
    session_id: Optional[str] = Field(None, description="Session ID")
    user_id: Optional[str] = Field(None, description="User ID")
    language: Optional[str] = Field(None, description="Language code")
    data: Optional[str] = Field(None, description="Base64 encoded audio data")


class TranscriptionResult(BaseModel):
    """Transcription result model"""
    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class NLPResult(BaseModel):
    """NLP processing result model"""
    intent: str = Field(..., description="Detected intent")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")


class EligibilityResult(BaseModel):
    """Eligibility check result model"""
    eligible: bool = Field(..., description="Whether user is eligible")
    score: int = Field(..., ge=0, le=100, description="Eligibility score (0-100)")
    reasons: List[str] = Field(default_factory=list, description="Eligibility reasons")
    scheme_name: Optional[Dict[str, str]] = Field(None, description="Scheme name (multilingual)")


# New models for PS6 enhancements
class EligibilityExplanation(BaseModel):
    """Structured eligibility explanation"""
    scheme_id: str
    scheme_name: Dict[str, str]
    status: str  # ELIGIBLE, LIKELY_ELIGIBLE, NEEDS_VERIFICATION, NOT_ELIGIBLE
    score: int  # 0-100
    matched_conditions: List[str] = Field(default_factory=list)
    match_reasons: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    verification_required: List[str] = Field(default_factory=list)
    eligibility_criteria_summary: Dict[str, Any] = Field(default_factory=dict)


class ActionPlanStep(BaseModel):
    """Single step in citizen action plan"""
    step_number: int
    action: str
    description: str
    status: str  # COMPLETED, REQUIRED, OPTIONAL
    documents_needed: List[str] = Field(default_factory=list)


class CitizenActionPlan(BaseModel):
    """Complete action plan for scheme application"""
    scheme_id: str
    scheme_name: Dict[str, str]
    eligibility_status: str
    required_documents: List[str] = Field(default_factory=list)
    available_documents: List[str] = Field(default_factory=list)
    missing_documents: List[str] = Field(default_factory=list)
    next_steps: List[ActionPlanStep] = Field(default_factory=list)
    application_method: Optional[str] = None
    portal_url: Optional[str] = None
    estimated_time: Optional[str] = None
    notes: List[str] = Field(default_factory=list)
