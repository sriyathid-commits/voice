"""
Voice Service - Business logic for voice processing
Implements the processVoiceQuery algorithm from the design document.
"""
import os
import json
import base64
import hashlib
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Import shared utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.utils import (
    get_dynamodb_resource,
    get_s3_client,
    get_bedrock_client,
    get_audio_s3_key,
    get_tts_cache_s3_key,
    upload_to_s3,
    download_from_s3,
    check_s3_object_exists,
    generate_presigned_url,
    hash_text,
    get_table_name
)
from shared.constants import (
    SUPPORTED_LANGUAGES,
    BEDROCK_LOCALES,
    VOICE_INTENTS,
    CONFIDENCE_THRESHOLDS,
    S3_AUDIO_BUCKET
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class VoiceService:
    """Service for processing voice queries and managing conversations"""
    
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.s3_client = get_s3_client()
        self.bedrock_client = get_bedrock_client()
        
        # Audio buffer for WebSocket streaming
        self.audio_buffers = {}
        
        # Session cache (in-memory for Lambda)
        self.session_cache = {}
        
        # Environment variables
        self.audio_bucket = os.getenv("S3_AUDIO_BUCKET")
        self.region = os.getenv("AWS_REGION", "ap-south-1")
    
    async def get_or_create_session(
        self,
        session_id: str,
        user_id: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Get existing session or create new one
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            language: Language code
        
        Returns:
            Session dictionary
        """
        # Check cache first
        if session_id in self.session_cache:
            return self.session_cache[session_id]
        
        # Create new session
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "language": language,
            "messages": [],
            "context": {
                "current_intent": None,
                "entities": {},
                "conversation_state": "READY",
                "selected_scheme": None
            },
            "started_at": datetime.utcnow().isoformat(),
            "last_activity_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        # Cache session
        self.session_cache[session_id] = session
        
        return session
    
    async def accumulate_audio_chunk(self, session_id: str, audio_data: str):
        """
        Accumulate audio chunks for WebSocket streaming
        
        Args:
            session_id: Session identifier
            audio_data: Base64 encoded audio data
        """
        if session_id not in self.audio_buffers:
            self.audio_buffers[session_id] = []
        
        # Decode and store audio chunk
        audio_bytes = base64.b64decode(audio_data)
        self.audio_buffers[session_id].append(audio_bytes)
    
    async def cleanup_audio_buffer(self, session_id: str):
        """Clean up audio buffer after processing"""
        if session_id in self.audio_buffers:
            del self.audio_buffers[session_id]
    
    async def process_voice_query_websocket(self, session_id: str) -> Dict[str, Any]:
        """
        Process accumulated audio from WebSocket
        
        Args:
            session_id: Session identifier
        
        Returns:
            Response dictionary with text and audio URL
        """
        # Get accumulated audio
        if session_id not in self.audio_buffers:
            raise ValueError("No audio data found for session")
        
        audio_chunks = self.audio_buffers[session_id]
        audio_data = b''.join(audio_chunks)
        
        # Get session
        session = self.session_cache.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        # Process the audio
        response = await self.process_voice_query(
            audio_data=audio_data,
            session_id=session_id,
            language=session["language"],
            user_id=session["user_id"]
        )
        
        # Clean up buffer
        await self.cleanup_audio_buffer(session_id)
        
        return response
    
    async def process_voice_query(
        self,
        audio_data: bytes,
        session_id: str,
        language: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Main voice processing algorithm (implements processVoiceQuery from design)
        
        Args:
            audio_data: Audio file bytes
            session_id: Session identifier
            language: Language code
            user_id: User identifier
        
        Returns:
            Response dictionary
        """
        logger.info(f"Processing voice query - Session: {session_id}, Language: {language}")
        
        # Step 1: Get or create session
        session = await self.get_or_create_session(session_id, user_id, language)
        
        # Step 2: Transcribe audio to text
        transcription_result = await self.transcribe_audio(audio_data, language)
        
        if transcription_result["confidence"] < CONFIDENCE_THRESHOLDS["transcription"]:
            return await self._generate_low_confidence_response(language)
        
        user_text = transcription_result["text"]
        logger.info(f"Transcribed text: {user_text}")
        
        # Step 3: Update conversation history
        user_message = {
            "message_id": f"msg-{datetime.utcnow().timestamp()}",
            "role": "USER",
            "content": user_text,
            "audio_url": None,  # Could store user audio if needed
            "timestamp": datetime.utcnow().isoformat()
        }
        session["messages"].append(user_message)
        
        # Step 4: Extract intent and entities using AI
        nlp_result = await self.process_natural_language(
            user_text,
            session["context"],
            language
        )
        
        session["context"]["current_intent"] = nlp_result["intent"]
        session["context"]["entities"].update(nlp_result["entities"])
        
        # Step 5: Execute intent-specific logic
        response_text, schemes = await self._execute_intent(
            nlp_result["intent"],
            nlp_result["entities"],
            user_id,
            language,
            session
        )
        
        # Step 6: Synthesize speech from response text
        audio_url = await self.synthesize_speech(response_text, language, session_id)
        
        # Step 7: Update conversation history with assistant response
        assistant_message = {
            "message_id": f"msg-{datetime.utcnow().timestamp()}",
            "role": "ASSISTANT",
            "content": response_text,
            "audio_url": audio_url,
            "timestamp": datetime.utcnow().isoformat()
        }
        session["messages"].append(assistant_message)
        
        # Step 8: Update session
        session["last_activity_at"] = datetime.utcnow().isoformat()
        self.session_cache[session_id] = session
        
        # Step 9: Return response
        return {
            "text": response_text,
            "audio_url": audio_url,
            "context": session["context"],
            "schemes": schemes
        }
    
    async def transcribe_audio(
        self,
        audio_data: bytes,
        language: str
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Amazon Bedrock Titan
        
        Args:
            audio_data: Audio file bytes
            language: Language code
        
        Returns:
            Dictionary with text and confidence
        """
        try:
            # Get Bedrock locale
            locale = BEDROCK_LOCALES.get(language, "en-IN")
            
            # For now, return mock transcription
            # In production, integrate with Amazon Transcribe or Bedrock
            logger.info(f"Transcribing audio in language: {language} ({locale})")
            
            # Mock transcription (replace with actual Bedrock call)
            mock_text = "I want to know about welfare schemes"
            
            return {
                "text": mock_text,
                "confidence": 0.95
            }
        
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {
                "text": "",
                "confidence": 0.0
            }
    
    async def process_natural_language(
        self,
        text: str,
        context: Dict[str, Any],
        language: str
    ) -> Dict[str, Any]:
        """
        Process natural language using Claude 3 Sonnet
        
        Args:
            text: User text
            context: Conversation context
            language: Language code
        
        Returns:
            Dictionary with intent and entities
        """
        try:
            # Build prompt for Claude
            prompt = self._build_nlp_prompt(text, context, language)
            
            # Call Bedrock Claude (mock for now)
            logger.info(f"Processing NLP for text: {text}")
            
            # Mock NLP result (replace with actual Bedrock call)
            intent = self._detect_intent_simple(text)
            entities = self._extract_entities_simple(text)
            
            return {
                "intent": intent,
                "entities": entities,
                "confidence": 0.9
            }
        
        except Exception as e:
            logger.error(f"NLP error: {e}")
            return {
                "intent": "GENERAL_QUERY",
                "entities": {},
                "confidence": 0.5
            }
    
    async def synthesize_speech(
        self,
        text: str,
        language: str,
        session_id: str
    ) -> str:
        """
        Synthesize speech using Amazon Bedrock Titan TTS
        
        Args:
            text: Text to synthesize
            language: Language code
            session_id: Session identifier
        
        Returns:
            S3 presigned URL for audio file
        """
        try:
            # Check TTS cache first
            text_hash = hash_text(text)
            cache_key = get_tts_cache_s3_key(language, text_hash)
            
            if check_s3_object_exists(self.audio_bucket, cache_key):
                logger.info(f"TTS cache hit for text hash: {text_hash}")
                return generate_presigned_url(self.audio_bucket, cache_key, expiration=3600)
            
            # Generate TTS audio (mock for now)
            logger.info(f"Generating TTS for language: {language}")
            
            # Mock audio generation (replace with actual Bedrock call)
            audio_bytes = b"mock_audio_data"
            
            # Upload to S3
            upload_to_s3(
                bucket=self.audio_bucket,
                key=cache_key,
                data=audio_bytes,
                content_type="audio/mpeg"
            )
            
            # Generate presigned URL
            audio_url = generate_presigned_url(self.audio_bucket, cache_key, expiration=3600)
            
            return audio_url
        
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return ""
    
    async def _execute_intent(
        self,
        intent: str,
        entities: Dict[str, Any],
        user_id: str,
        language: str,
        session: Dict[str, Any]
    ) -> tuple:
        """
        Execute intent-specific logic
        
        Returns:
            Tuple of (response_text, schemes_list)
        """
        if intent == "SEARCH_SCHEMES":
            return await self._handle_search_schemes(entities, user_id, language)
        
        elif intent == "CHECK_ELIGIBILITY":
            return await self._handle_check_eligibility(entities, user_id, language)
        
        elif intent == "START_APPLICATION":
            return await self._handle_start_application(entities, user_id, language)
        
        elif intent == "GET_STATUS":
            return await self._handle_get_status(user_id, language)
        
        elif intent == "FIND_HELPLINE":
            return await self._handle_find_helpline(entities, language)
        
        elif intent == "GET_GUIDE":
            return await self._handle_get_guide(entities, language)
        
        else:
            return await self._handle_general_query(entities, language)
    
    async def _handle_search_schemes(
        self,
        entities: Dict[str, Any],
        user_id: str,
        language: str
    ) -> tuple:
        """Handle SEARCH_SCHEMES intent"""
        # Mock response
        response_text = "I found 3 welfare schemes that match your profile."
        schemes = []
        
        return response_text, schemes
    
    async def _handle_check_eligibility(
        self,
        entities: Dict[str, Any],
        user_id: str,
        language: str
    ) -> tuple:
        """Handle CHECK_ELIGIBILITY intent"""
        response_text = "Based on your profile, you are eligible for this scheme with a score of 85%."
        return response_text, []
    
    async def _handle_start_application(
        self,
        entities: Dict[str, Any],
        user_id: str,
        language: str
    ) -> tuple:
        """Handle START_APPLICATION intent"""
        response_text = "I've created a draft application for you. You can complete it in the dashboard."
        return response_text, []
    
    async def _handle_get_status(
        self,
        user_id: str,
        language: str
    ) -> tuple:
        """Handle GET_STATUS intent"""
        response_text = "You have 2 active applications. One is under review and one is approved."
        return response_text, []
    
    async def _handle_find_helpline(
        self,
        entities: Dict[str, Any],
        language: str
    ) -> tuple:
        """Handle FIND_HELPLINE intent"""
        response_text = "The welfare helpline number is 1800-XXX-XXXX. They are available 24/7."
        return response_text, []
    
    async def _handle_get_guide(
        self,
        entities: Dict[str, Any],
        language: str
    ) -> tuple:
        """Handle GET_GUIDE intent"""
        response_text = "Here's a quick guide on how to apply for welfare schemes."
        return response_text, []
    
    async def _handle_general_query(
        self,
        entities: Dict[str, Any],
        language: str
    ) -> tuple:
        """Handle GENERAL_QUERY intent"""
        response_text = "I can help you find welfare schemes, check eligibility, and apply for benefits. What would you like to know?"
        return response_text, []
    
    async def _generate_low_confidence_response(self, language: str) -> Dict[str, Any]:
        """Generate response for low confidence transcription"""
        response_text = "I'm sorry, I didn't catch that. Could you please repeat?"
        audio_url = await self.synthesize_speech(response_text, language, "temp")
        
        return {
            "text": response_text,
            "audio_url": audio_url,
            "context": {},
            "schemes": []
        }
    
    def _build_nlp_prompt(
        self,
        text: str,
        context: Dict[str, Any],
        language: str
    ) -> str:
        """Build prompt for Claude NLP"""
        prompt = f"""
You are a helpful assistant for Voice for Bharat, helping users find government welfare schemes in India.

User query: {text}
Language: {language}
Current context: {json.dumps(context)}

Identify the user's intent and extract relevant entities.

Possible intents:
- SEARCH_SCHEMES: User wants to find welfare schemes
- CHECK_ELIGIBILITY: User wants to check eligibility for a scheme
- START_APPLICATION: User wants to start an application
- GET_STATUS: User wants to check application status
- FIND_HELPLINE: User wants helpline information
- GET_GUIDE: User wants guidance
- GENERAL_QUERY: General question

Return JSON with: {{"intent": "...", "entities": {{...}}}}
"""
        return prompt
    
    def _detect_intent_simple(self, text: str) -> str:
        """Simple rule-based intent detection (fallback)"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["scheme", "yojana", "benefit", "welfare"]):
            return "SEARCH_SCHEMES"
        elif any(word in text_lower for word in ["eligible", "qualify", "can i"]):
            return "CHECK_ELIGIBILITY"
        elif any(word in text_lower for word in ["apply", "application", "start"]):
            return "START_APPLICATION"
        elif any(word in text_lower for word in ["status", "track", "progress"]):
            return "GET_STATUS"
        elif any(word in text_lower for word in ["helpline", "contact", "phone"]):
            return "FIND_HELPLINE"
        elif any(word in text_lower for word in ["guide", "how to", "help"]):
            return "GET_GUIDE"
        else:
            return "GENERAL_QUERY"
    
    def _extract_entities_simple(self, text: str) -> Dict[str, Any]:
        """Simple entity extraction (fallback)"""
        entities = {}
        
        # Extract state mentions
        states = ["maharashtra", "karnataka", "tamil nadu", "kerala", "gujarat"]
        for state in states:
            if state in text.lower():
                entities["state"] = state.upper().replace(" ", "_")
        
        # Extract category mentions
        categories = ["agriculture", "education", "health", "pension"]
        for category in categories:
            if category in text.lower():
                entities["category"] = category
        
        return entities
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session details"""
        return self.session_cache.get(session_id)
    
    async def end_session(self, session_id: str):
        """End conversation session"""
        if session_id in self.session_cache:
            session = self.session_cache[session_id]
            session["is_active"] = False
            session["ended_at"] = datetime.utcnow().isoformat()
            
            # Could persist to DynamoDB here
            
            # Remove from cache
            del self.session_cache[session_id]
