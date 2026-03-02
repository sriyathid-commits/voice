"""
Voice Service specific models
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


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
