"""
Shared Pydantic models for Voice for Bharat backend services.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator, field_validator, model_validator
import re


class BankDetails(BaseModel):
    """Bank account details"""
    account_number: str = Field(..., min_length=9, max_length=18, description="Bank account number")
    ifsc_code: str = Field(..., min_length=11, max_length=11, description="IFSC code (11 characters)")
    bank_name: str = Field(..., min_length=1, max_length=100, description="Bank name")
    verified: bool = False

    @validator("ifsc_code")
    def validate_ifsc_code(cls, v):
        """Validate IFSC code format (e.g., SBIN0001234)"""
        if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", v):
            raise ValueError("Invalid IFSC code format. Must be 11 characters (e.g., SBIN0001234)")
        return v.upper()

    @validator("account_number")
    def validate_account_number(cls, v):
        """Validate account number contains only digits"""
        if not re.match(r"^\d{9,18}$", v):
            raise ValueError("Account number must be 9-18 digits")
        return v


class UserProfile(BaseModel):
    """Extended user profile data"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    date_of_birth: Optional[datetime] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender (MALE, FEMALE, OTHER)")
    state: Optional[str] = Field(None, description="Indian state code")
    district: Optional[str] = Field(None, min_length=1, max_length=100, description="District name")
    income: Optional[float] = Field(None, ge=0, description="Annual income in INR (non-negative)")
    category: Optional[str] = Field(None, description="Social category (GENERAL, OBC, SC, ST, EWS)")
    aadhaar_number: Optional[str] = Field(None, description="12-digit Aadhaar number (encrypted)")
    pan_number: Optional[str] = Field(None, description="PAN card number")
    bank_account: Optional[BankDetails] = None
    documents: List[str] = Field(default_factory=list, description="List of document IDs")

    @validator("gender")
    def validate_gender(cls, v):
        """Validate gender value"""
        if v is not None:
            valid_genders = ["MALE", "FEMALE", "OTHER"]
            v_upper = v.upper()
            if v_upper not in valid_genders:
                raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")
            return v_upper
        return v

    @validator("category")
    def validate_category(cls, v):
        """Validate social category"""
        if v is not None:
            valid_categories = ["GENERAL", "OBC", "SC", "ST", "EWS"]
            v_upper = v.upper()
            if v_upper not in valid_categories:
                raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
            return v_upper
        return v

    @validator("aadhaar_number")
    def validate_aadhaar(cls, v):
        """Validate Aadhaar number format (12 digits)"""
        if v is not None:
            # Remove spaces and hyphens
            v_clean = re.sub(r"[\s\-]", "", v)
            if not re.match(r"^\d{12}$", v_clean):
                raise ValueError("Aadhaar number must be exactly 12 digits")
            return v_clean
        return v

    @validator("pan_number")
    def validate_pan(cls, v):
        """Validate PAN card format (e.g., ABCDE1234F)"""
        if v is not None:
            v_upper = v.upper()
            if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", v_upper):
                raise ValueError("Invalid PAN format. Must be 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)")
            return v_upper
        return v

    @validator("state")
    def validate_state(cls, v):
        """Validate Indian state code"""
        if v is not None:
            valid_states = [
                "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
                "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
                "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY"
            ]
            v_upper = v.upper()
            if v_upper not in valid_states:
                raise ValueError(f"Invalid state code. Must be one of: {', '.join(valid_states)}")
            return v_upper
        return v

    @validator("income")
    def validate_income(cls, v):
        """Validate income is non-negative"""
        if v is not None and v < 0:
            raise ValueError("Income must be non-negative")
        return v


class UserPreferences(BaseModel):
    """User preferences"""
    notification_channels: List[str] = Field(default_factory=lambda: ["sms"], description="Notification channels (sms, email, push, whatsapp)")
    preferred_language: str = Field(default="en", description="Preferred language code")
    voice_speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Voice playback speed (0.5-2.0)")
    auto_play_audio: bool = Field(default=True, description="Auto-play audio responses")

    @validator("notification_channels")
    def validate_notification_channels(cls, v):
        """Validate notification channels"""
        valid_channels = ["sms", "email", "push", "whatsapp"]
        for channel in v:
            if channel.lower() not in valid_channels:
                raise ValueError(f"Invalid notification channel: {channel}. Must be one of: {', '.join(valid_channels)}")
        return [c.lower() for c in v]

    @validator("preferred_language")
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        if v.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v.lower()


class User(BaseModel):
    """User model"""
    user_id: str = Field(..., description="Unique user identifier (UUID)")
    phone_number: str = Field(..., description="10-digit Indian mobile number")
    language: str = Field(default="en", description="User's language preference")
    profile: Optional[UserProfile] = None
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate Indian phone number format (10 digits starting with 6-9)"""
        # Remove any spaces, hyphens, or +91 prefix
        v_clean = re.sub(r"[\s\-]", "", v)
        v_clean = re.sub(r"^\+91", "", v_clean)
        
        if not re.match(r"^[6-9]\d{9}$", v_clean):
            raise ValueError("Invalid Indian phone number. Must be 10 digits starting with 6-9")
        return v_clean

    @validator("language")
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        if v.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v.lower()


class Rule(BaseModel):
    """Eligibility rule"""
    field: str = Field(..., description="Field name to evaluate")
    operator: str = Field(..., description="Comparison operator (eq, ne, gt, lt, gte, lte, in, not_in)")
    value: Any = Field(..., description="Value to compare against")
    logical_operator: Optional[str] = Field(default="AND", description="Logical operator (AND, OR)")

    @validator("operator")
    def validate_operator(cls, v):
        """Validate operator"""
        valid_operators = ["eq", "ne", "gt", "lt", "gte", "lte", "in", "not_in", "contains", "not_contains"]
        if v.lower() not in valid_operators:
            raise ValueError(f"Operator must be one of: {', '.join(valid_operators)}")
        return v.lower()

    @validator("logical_operator")
    def validate_logical_operator(cls, v):
        """Validate logical operator"""
        if v is not None:
            valid_operators = ["AND", "OR"]
            v_upper = v.upper()
            if v_upper not in valid_operators:
                raise ValueError(f"Logical operator must be one of: {', '.join(valid_operators)}")
            return v_upper
        return v


class EligibilityCriteria(BaseModel):
    """Scheme eligibility criteria"""
    min_age: Optional[int] = Field(None, ge=0, le=120, description="Minimum age requirement")
    max_age: Optional[int] = Field(None, ge=0, le=120, description="Maximum age requirement")
    gender: List[str] = Field(default_factory=list, description="Eligible genders")
    income_limit: Optional[float] = Field(None, ge=0, description="Maximum annual income limit")
    categories: List[str] = Field(default_factory=list, description="Eligible social categories")
    states: List[str] = Field(default_factory=list, description="Eligible states")
    custom_rules: List[Rule] = Field(default_factory=list, description="Custom eligibility rules")

    @model_validator(mode='after')
    def validate_age_range(self):
        """Validate that min_age is less than max_age"""
        if self.min_age is not None and self.max_age is not None:
            if self.min_age > self.max_age:
                raise ValueError("min_age must be less than or equal to max_age")
        return self

    @validator("gender")
    def validate_gender(cls, v):
        """Validate gender values"""
        valid_genders = ["MALE", "FEMALE", "OTHER", "ALL"]
        for gender in v:
            if gender.upper() not in valid_genders:
                raise ValueError(f"Gender must be one of: {', '.join(valid_genders)}")
        return [g.upper() for g in v]

    @validator("categories")
    def validate_categories(cls, v):
        """Validate social categories"""
        valid_categories = ["GENERAL", "OBC", "SC", "ST", "EWS", "ALL"]
        for category in v:
            if category.upper() not in valid_categories:
                raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return [c.upper() for c in v]

    @validator("states")
    def validate_states(cls, v):
        """Validate state codes"""
        valid_states = [
            "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
            "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
            "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY", "ALL_INDIA"
        ]
        for state in v:
            if state.upper() not in valid_states:
                raise ValueError(f"Invalid state code: {state}")
        return [s.upper() for s in v]


class Scheme(BaseModel):
    """Government welfare scheme"""
    scheme_id: str = Field(..., description="Unique scheme identifier")
    name: Dict[str, str] = Field(..., description="Multilingual scheme name (en, hi, mr, kn, ta, te)")
    description: Dict[str, str] = Field(..., description="Multilingual scheme description")
    state: str = Field(..., description="State code or ALL_INDIA")
    category: str = Field(..., description="Scheme category")
    eligibility_criteria: EligibilityCriteria
    benefits: Dict[str, str] = Field(..., description="Multilingual benefits description")
    application_process: Dict[str, List[str]] = Field(..., description="Multilingual application steps")
    required_documents: List[str] = Field(default_factory=list, description="List of required document types")
    portal_url: Optional[str] = Field(None, description="Government portal URL")
    portal_status: str = Field(default="ACTIVE", description="Portal status (ACTIVE, MAINTENANCE, OFFLINE)")
    last_synced_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    @validator("name", "description", "benefits")
    def validate_multilingual_required(cls, v):
        """Validate that at least one language entry exists"""
        if not v or len(v) == 0:
            raise ValueError("At least one language entry is required")
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v.keys():
            if lang not in valid_languages:
                raise ValueError(f"Invalid language code: {lang}. Must be one of: {', '.join(valid_languages)}")
        return v

    @validator("application_process")
    def validate_application_process(cls, v):
        """Validate application process has at least one language"""
        if not v or len(v) == 0:
            raise ValueError("Application process must have at least one language entry")
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v.keys():
            if lang not in valid_languages:
                raise ValueError(f"Invalid language code: {lang}")
        return v

    @validator("state")
    def validate_state(cls, v):
        """Validate state code"""
        valid_states = [
            "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
            "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
            "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY", "ALL_INDIA"
        ]
        v_upper = v.upper()
        if v_upper not in valid_states:
            raise ValueError(f"Invalid state code: {v}")
        return v_upper

    @validator("category")
    def validate_category(cls, v):
        """Validate scheme category"""
        valid_categories = [
            "education", "health", "agriculture", "housing", "employment",
            "pension", "women", "children", "disability", "financial", "other"
        ]
        v_lower = v.lower()
        if v_lower not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v_lower

    @validator("portal_status")
    def validate_portal_status(cls, v):
        """Validate portal status"""
        valid_statuses = ["ACTIVE", "MAINTENANCE", "OFFLINE"]
        v_upper = v.upper()
        if v_upper not in valid_statuses:
            raise ValueError(f"Portal status must be one of: {', '.join(valid_statuses)}")
        return v_upper

    @validator("portal_url")
    def validate_portal_url(cls, v):
        """Validate portal URL format"""
        if v is not None and v.strip():
            if not re.match(r"^https?://", v):
                raise ValueError("Portal URL must start with http:// or https://")
        return v


class DocumentReference(BaseModel):
    """Document reference"""
    document_id: str = Field(..., description="Unique document identifier")
    document_type: str = Field(..., description="Document type (aadhaar, pan, income_certificate, etc.)")
    s3_key: str = Field(..., description="S3 object key")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    verified: bool = False

    @validator("document_type")
    def validate_document_type(cls, v):
        """Validate document type"""
        valid_types = [
            "aadhaar", "pan", "income_certificate", "caste_certificate",
            "bank_passbook", "photo", "address_proof", "age_proof",
            "disability_certificate", "ration_card", "other"
        ]
        v_lower = v.lower()
        if v_lower not in valid_types:
            raise ValueError(f"Document type must be one of: {', '.join(valid_types)}")
        return v_lower


class StatusChange(BaseModel):
    """Application status change"""
    status: str = Field(..., description="Application status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reason: Optional[str] = Field(None, max_length=500, description="Reason for status change")
    updated_by: str = Field(default="system", description="Who updated the status")

    @validator("status")
    def validate_status(cls, v):
        """Validate application status"""
        valid_statuses = [
            "DRAFT", "SUBMITTED", "UNDER_REVIEW", "DOCUMENTS_PENDING",
            "APPROVED", "REJECTED", "WITHDRAWN", "COMPLETED"
        ]
        v_upper = v.upper()
        if v_upper not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v_upper


class Application(BaseModel):
    """User application to a scheme"""
    application_id: str = Field(..., description="Unique application identifier")
    user_id: str = Field(..., description="User identifier")
    scheme_id: str = Field(..., description="Scheme identifier")
    status: str = Field(default="DRAFT", description="Application status")
    form_data: Dict[str, Any] = Field(default_factory=dict, description="Application form data")
    documents: List[DocumentReference] = Field(default_factory=list, description="Uploaded documents")
    submitted_at: Optional[datetime] = Field(None, description="Submission timestamp")
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)
    external_reference_id: Optional[str] = Field(None, description="External portal reference ID")
    status_history: List[StatusChange] = Field(default_factory=list, description="Status change history")
    notes: Optional[str] = Field(None, max_length=1000, description="Application notes")

    @validator("status")
    def validate_status(cls, v):
        """Validate application status"""
        valid_statuses = [
            "DRAFT", "SUBMITTED", "UNDER_REVIEW", "DOCUMENTS_PENDING",
            "APPROVED", "REJECTED", "WITHDRAWN", "COMPLETED"
        ]
        v_upper = v.upper()
        if v_upper not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return v_upper

    @model_validator(mode='after')
    def validate_submitted_at(self):
        """Validate that submitted_at is set when status is not DRAFT"""
        if self.status and self.status != "DRAFT" and self.submitted_at is None:
            raise ValueError("submitted_at must be set when status is not DRAFT")
        return self


class Message(BaseModel):
    """Conversation message"""
    message_id: str = Field(..., description="Unique message identifier")
    role: str = Field(..., description="Message role (USER, ASSISTANT, SYSTEM)")
    content: str = Field(..., min_length=1, description="Message content")
    audio_url: Optional[str] = Field(None, description="Audio file URL")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @validator("role")
    def validate_role(cls, v):
        """Validate message role"""
        valid_roles = ["USER", "ASSISTANT", "SYSTEM"]
        v_upper = v.upper()
        if v_upper not in valid_roles:
            raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
        return v_upper


class ConversationContext(BaseModel):
    """Conversation context"""
    current_intent: Optional[str] = Field(None, description="Current conversation intent")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")
    selected_scheme: Optional[str] = Field(None, description="Currently selected scheme ID")
    conversation_state: str = Field(default="READY", description="Conversation state")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")

    @validator("conversation_state")
    def validate_conversation_state(cls, v):
        """Validate conversation state"""
        valid_states = [
            "READY", "LISTENING", "PROCESSING", "SPEAKING",
            "SHOWING_SCHEMES", "ELIGIBILITY_CHECKED", "APPLICATION_STARTED", "STATUS_SHOWN"
        ]
        v_upper = v.upper()
        if v_upper not in valid_states:
            raise ValueError(f"Conversation state must be one of: {', '.join(valid_states)}")
        return v_upper


class ConversationSession(BaseModel):
    """Voice conversation session"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    language: str = Field(default="en", description="Conversation language")
    messages: List[Message] = Field(default_factory=list, description="Conversation messages")
    context: ConversationContext = Field(default_factory=ConversationContext)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    @validator("language")
    def validate_language(cls, v):
        """Validate language code"""
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        v_lower = v.lower()
        if v_lower not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v_lower


class Helpline(BaseModel):
    """Helpline information"""
    helpline_id: str = Field(..., description="Unique helpline identifier")
    name: Dict[str, str] = Field(..., description="Multilingual helpline name")
    phone_number: str = Field(..., description="Helpline phone number")
    category: str = Field(..., description="Helpline category")
    state: str = Field(..., description="State code or ALL_INDIA")
    availability: str = Field(..., description="Availability hours (e.g., 24/7, 9 AM - 6 PM)")
    languages: List[str] = Field(..., description="Supported languages")
    description: Dict[str, str] = Field(..., description="Multilingual description")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format (10 digits or toll-free)"""
        # Remove spaces and hyphens
        v_clean = re.sub(r"[\s\-]", "", v)
        # Check for 10-digit number or toll-free (1800, 1860)
        if not (re.match(r"^[6-9]\d{9}$", v_clean) or re.match(r"^1[8][0-9]{2}\d{6,7}$", v_clean)):
            raise ValueError("Invalid phone number. Must be 10 digits or toll-free format (1800XXXXXX)")
        return v_clean

    @validator("category")
    def validate_category(cls, v):
        """Validate helpline category"""
        valid_categories = ["welfare", "health", "emergency", "agriculture", "education", "other"]
        v_lower = v.lower()
        if v_lower not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v_lower

    @validator("state")
    def validate_state(cls, v):
        """Validate state code"""
        valid_states = [
            "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
            "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
            "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY", "ALL_INDIA"
        ]
        v_upper = v.upper()
        if v_upper not in valid_states:
            raise ValueError(f"Invalid state code: {v}")
        return v_upper

    @validator("languages")
    def validate_languages(cls, v):
        """Validate supported languages"""
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v:
            if lang.lower() not in valid_languages:
                raise ValueError(f"Invalid language: {lang}. Must be one of: {', '.join(valid_languages)}")
        return [lang.lower() for lang in v]

    @validator("name", "description")
    def validate_multilingual(cls, v):
        """Validate multilingual fields"""
        if not v or len(v) == 0:
            raise ValueError("At least one language entry is required")
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v.keys():
            if lang not in valid_languages:
                raise ValueError(f"Invalid language code: {lang}")
        return v


class GuideContent(BaseModel):
    """Guide content (FAQ, tutorials)"""
    content_id: str = Field(..., description="Unique content identifier")
    category: str = Field(..., description="Content category")
    state: str = Field(..., description="State code or ALL_INDIA")
    question: Dict[str, str] = Field(..., description="Multilingual question")
    answer: Dict[str, str] = Field(..., description="Multilingual answer")
    priority: int = Field(default=50, ge=1, le=100, description="Priority (1-100, higher = more important)")
    tags: List[str] = Field(default_factory=list, description="Search tags")
    related_schemes: List[str] = Field(default_factory=list, description="Related scheme IDs")
    view_count: int = Field(default=0, ge=0, description="Number of views")
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    @validator("category")
    def validate_category(cls, v):
        """Validate content category"""
        valid_categories = ["quick-guide", "faq", "tutorial", "troubleshooting"]
        v_lower = v.lower()
        if v_lower not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v_lower

    @validator("state")
    def validate_state(cls, v):
        """Validate state code"""
        valid_states = [
            "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
            "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
            "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY", "ALL_INDIA"
        ]
        v_upper = v.upper()
        if v_upper not in valid_states:
            raise ValueError(f"Invalid state code: {v}")
        return v_upper

    @validator("question", "answer")
    def validate_multilingual(cls, v):
        """Validate multilingual fields"""
        if not v or len(v) == 0:
            raise ValueError("At least one language entry is required")
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v.keys():
            if lang not in valid_languages:
                raise ValueError(f"Invalid language code: {lang}")
        return v

    @validator("tags")
    def validate_tags(cls, v):
        """Validate tags are non-empty"""
        if len(v) == 0:
            raise ValueError("At least one tag is required for searchability")
        return v


class SuggestedQuery(BaseModel):
    """Suggested voice query"""
    query_id: str = Field(..., description="Unique query identifier")
    text: Dict[str, str] = Field(..., description="Multilingual query text")
    category: str = Field(..., description="Query category")
    state: str = Field(..., description="State code or ALL_INDIA")
    intent: str = Field(..., description="Voice service intent type")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Pre-filled entities")
    popularity: int = Field(default=0, ge=0, description="Popularity score (incremented on use)")
    display_order: int = Field(default=0, ge=0, description="Display position")
    is_active: bool = True
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("category")
    def validate_category(cls, v):
        """Validate query category"""
        valid_categories = ["ration-card", "health", "agriculture", "education", "pension", "other"]
        v_lower = v.lower()
        if v_lower not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return v_lower

    @validator("state")
    def validate_state(cls, v):
        """Validate state code"""
        valid_states = [
            "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL",
            "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS",
            "TR", "UP", "UK", "WB", "AN", "CH", "DN", "DD", "DL", "JK", "LA", "LD", "PY", "ALL_INDIA"
        ]
        v_upper = v.upper()
        if v_upper not in valid_states:
            raise ValueError(f"Invalid state code: {v}")
        return v_upper

    @validator("text")
    def validate_multilingual(cls, v):
        """Validate multilingual text"""
        if not v or len(v) == 0:
            raise ValueError("Text must have entries for all supported languages")
        valid_languages = ["en", "hi", "mr", "kn", "ta", "te"]
        for lang in v.keys():
            if lang not in valid_languages:
                raise ValueError(f"Invalid language code: {lang}")
        return v

    @validator("intent")
    def validate_intent(cls, v):
        """Validate intent type"""
        valid_intents = [
            "SEARCH_SCHEMES", "CHECK_ELIGIBILITY", "START_APPLICATION",
            "GET_STATUS", "FIND_HELPLINE", "GET_GUIDE", "OTHER"
        ]
        v_upper = v.upper()
        if v_upper not in valid_intents:
            raise ValueError(f"Intent must be one of: {', '.join(valid_intents)}")
        return v_upper
