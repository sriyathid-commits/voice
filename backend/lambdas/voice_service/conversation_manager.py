"""
Conversation Manager - Session and Context Management
Handles conversational context storage and retrieval using Redis cache
"""
import os
import json
import uuid
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from models import ConversationSession, CitizenProfile, ConversationMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConversationManager:
    """Manages conversation sessions and context"""
    
    def __init__(self):
        self.redis_client = None
        self.session_ttl = 1800  # 30 minutes
        
        # Initialize Redis if available
        if REDIS_AVAILABLE:
            try:
                redis_endpoint = os.getenv("REDIS_ENDPOINT")
                redis_port = int(os.getenv("REDIS_PORT", "6379"))
                
                if redis_endpoint:
                    self.redis_client = redis.Redis(
                        host=redis_endpoint,
                        port=redis_port,
                        db=0,
                        decode_responses=True
                    )
                    logger.info("Redis client initialized successfully")
            except Exception as e:
                logger.warning(f"Redis not available, using in-memory fallback: {e}")
        
        # In-memory fallback for development
        self.memory_store = {}
    
    def create_session(
        self,
        user_id: str,
        language: str = "en"
    ) -> ConversationSession:
        """
        Create a new conversation session
        
        Args:
            user_id: User identifier
            language: Conversation language
        
        Returns:
            New ConversationSession instance
        """
        session_id = f"session-{uuid.uuid4()}"
        
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            language=language,
            citizen_profile=CitizenProfile(user_id=user_id, language=language)
        )
        
        # Save session
        self._save_session(session)
        
        logger.info(f"Created new session: {session_id} for user: {user_id}")
        return session
    
    def get_session(
        self,
        session_id: str
    ) -> Optional[ConversationSession]:
        """
        Retrieve existing conversation session
        
        Args:
            session_id: Session identifier
        
        Returns:
            ConversationSession if found, None otherwise
        """
        # Try Redis first
        if self.redis_client:
            try:
                session_json = self.redis_client.get(f"session:{session_id}")
                if session_json:
                    session_dict = json.loads(session_json)
                    return ConversationSession(**session_dict)
            except Exception as e:
                logger.warning(f"Error retrieving from Redis: {e}")
        
        # Fallback to memory store
        if session_id in self.memory_store:
            return self.memory_store[session_id]
        
        logger.info(f"Session not found: {session_id}")
        return None
    
    def get_or_create_session(
        self,
        session_id: Optional[str],
        user_id: str,
        language: str = "en"
    ) -> ConversationSession:
        """
        Get existing session or create new one
        
        Args:
            session_id: Optional existing session ID
            user_id: User identifier
            language: Conversation language
        
        Returns:
            ConversationSession instance
        """
        if session_id:
            session = self.get_session(session_id)
            if session and session.is_active:
                # Update last activity
                session.last_activity_at = datetime.utcnow().isoformat()
                self._save_session(session)
                return session
        
        # Create new session
        return self.create_session(user_id, language)
    
    def update_session(
        self,
        session: ConversationSession
    ) -> bool:
        """
        Update existing conversation session
        
        Args:
            session: ConversationSession to update
        
        Returns:
            True if successful
        """
        session.last_activity_at = datetime.utcnow().isoformat()
        return self._save_session(session)
    
    def add_message(
        self,
        session: ConversationSession,
        role: str,
        content: str,
        audio_url: Optional[str] = None,
        intent: Optional[str] = None,
        entities: Optional[Dict[str, Any]] = None
    ) -> ConversationMessage:
        """
        Add a message to the conversation
        
        Args:
            session: ConversationSession
            role: Message role (USER, ASSISTANT, SYSTEM)
            content: Message content
            audio_url: Optional audio URL
            intent: Optional detected intent
            entities: Optional extracted entities
        
        Returns:
            Created ConversationMessage
        """
        message = ConversationMessage(
            message_id=f"msg-{uuid.uuid4()}",
            role=role,
            content=content,
            audio_url=audio_url,
            intent=intent,
            entities=entities or {}
        )
        
        session.messages.append(message)
        
        # Keep only last 20 messages to manage memory
        if len(session.messages) > 20:
            session.messages = session.messages[-20:]
        
        self.update_session(session)
        
        return message
    
    def update_citizen_profile(
        self,
        session: ConversationSession,
        updates: Dict[str, Any]
    ) -> CitizenProfile:
        """
        Update citizen profile with new information
        
        Args:
            session: ConversationSession
            updates: Dictionary of profile updates
        
        Returns:
            Updated CitizenProfile
        """
        profile = session.citizen_profile
        
        # Update only provided fields
        for key, value in updates.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        
        self.update_session(session)
        
        logger.info(f"Updated citizen profile for session {session.session_id}: {updates}")
        return profile
    
    def get_profile_gaps(
        self,
        profile: CitizenProfile,
        required_for_intent: str = "SEARCH_SCHEMES"
    ) -> list[str]:
        """
        Identify missing information in citizen profile
        
        Args:
            profile: CitizenProfile to check
            required_for_intent: Intent that determines required fields
        
        Returns:
            List of missing field names
        """
        gaps = []
        
        # Essential fields for scheme search
        if required_for_intent == "SEARCH_SCHEMES":
            if not profile.state:
                gaps.append("state")
            # Add more conditionally based on occupation
            if profile.occupation and "farmer" in profile.occupation.lower():
                if profile.has_land is None:
                    gaps.append("has_land")
        
        # Essential fields for eligibility check
        elif required_for_intent == "CHECK_ELIGIBILITY":
            if not profile.age:
                gaps.append("age")
            if not profile.income_range:
                gaps.append("income_range")
            if not profile.state:
                gaps.append("state")
        
        return gaps
    
    def close_session(
        self,
        session_id: str
    ) -> bool:
        """
        Mark session as inactive
        
        Args:
            session_id: Session identifier
        
        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if session:
            session.is_active = False
            return self._save_session(session)
        return False
    
    def _save_session(
        self,
        session: ConversationSession
    ) -> bool:
        """
        Save session to Redis or memory store
        
        Args:
            session: ConversationSession to save
        
        Returns:
            True if successful
        """
        session_json = session.model_dump_json()
        
        # Try Redis first
        if self.redis_client:
            try:
                self.redis_client.setex(
                    f"session:{session.session_id}",
                    self.session_ttl,
                    session_json
                )
                return True
            except Exception as e:
                logger.warning(f"Error saving to Redis: {e}")
        
        # Fallback to memory store
        self.memory_store[session.session_id] = session
        return True
    
    def get_conversation_history(
        self,
        session: ConversationSession,
        last_n: int = 5
    ) -> list[ConversationMessage]:
        """
        Get recent conversation history
        
        Args:
            session: ConversationSession
            last_n: Number of recent messages to retrieve
        
        Returns:
            List of recent ConversationMessage objects
        """
        return session.messages[-last_n:] if session.messages else []
