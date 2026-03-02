"""
Shared constants for Voice for Bharat backend services.
"""

# Supported languages
SUPPORTED_LANGUAGES = ["en", "hi", "mr", "kn", "ta", "te"]

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu"
}

# Bedrock locale mapping
BEDROCK_LOCALES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "mr": "mr-IN",
    "kn": "kn-IN",
    "ta": "ta-IN",
    "te": "te-IN"
}

# Indian states
INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry"
]

# Scheme categories
SCHEME_CATEGORIES = [
    "education",
    "health",
    "agriculture",
    "pension",
    "housing",
    "employment",
    "women-welfare",
    "child-welfare",
    "disability",
    "financial-assistance"
]

# Application statuses
APPLICATION_STATUSES = [
    "DRAFT",
    "SUBMITTED",
    "UNDER_REVIEW",
    "DOCUMENTS_PENDING",
    "APPROVED",
    "REJECTED",
    "WITHDRAWN",
    "COMPLETED"
]

# Document types
DOCUMENT_TYPES = [
    "aadhaar",
    "pan",
    "income-certificate",
    "caste-certificate",
    "bank-passbook",
    "photo",
    "domicile-certificate",
    "age-proof",
    "land-records",
    "disability-certificate"
]

# Activity types
ACTIVITY_TYPES = [
    "APPLICATION_CREATED",
    "APPLICATION_UPDATED",
    "APPLICATION_SUBMITTED",
    "DOCUMENT_UPLOADED",
    "DOCUMENT_VERIFIED",
    "SCHEME_VIEWED",
    "SCHEME_SAVED",
    "ELIGIBILITY_CHECKED",
    "VOICE_QUERY",
    "PROFILE_UPDATED"
]

# Voice intents
VOICE_INTENTS = [
    "SEARCH_SCHEMES",
    "CHECK_ELIGIBILITY",
    "START_APPLICATION",
    "GET_STATUS",
    "FIND_HELPLINE",
    "GET_GUIDE",
    "GENERAL_QUERY"
]

# Notification channels
NOTIFICATION_CHANNELS = [
    "sms",
    "email",
    "push",
    "whatsapp"
]

# S3 bucket names (will be prefixed with environment)
S3_DOCUMENTS_BUCKET = "voice-for-bharat-documents"
S3_AUDIO_BUCKET = "voice-for-bharat-audio"
S3_SCHEME_DUMPS_BUCKET = "voice-for-bharat-scheme-dumps"

# DynamoDB table names (will be prefixed with environment)
DYNAMODB_TABLES = {
    "users": "users",
    "schemes": "schemes",
    "applications": "applications",
    "activity_log": "activity_log",
    "user_profile": "user_profile",
    "helplines": "helplines",
    "guide_content": "guide_content",
    "suggested_queries": "suggested_queries"
}

# Cache TTL (seconds)
CACHE_TTL = {
    "schemes": 3600,  # 1 hour
    "user_profile": 300,  # 5 minutes
    "conversation_session": 1800,  # 30 minutes
    "tts_audio": 7776000  # 90 days
}

# API rate limits
RATE_LIMITS = {
    "voice_query": 10,  # per minute
    "document_upload": 5,  # per minute
    "application_submit": 3  # per minute
}

# Bedrock model IDs
BEDROCK_MODELS = {
    "stt": "amazon.titan-tts-v1",
    "tts": "amazon.titan-tts-v1",
    "llm": "anthropic.claude-3-sonnet-20240229-v1:0",
    "embeddings": "amazon.titan-embed-v1"
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "transcription": 0.7,
    "intent_recognition": 0.6,
    "eligibility_match": 0.5
}
