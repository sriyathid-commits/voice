"""
Voice Service - Conversational AI Implementation
Enhanced for PS6: AI for Bharat in Indian Languages

Features:
- Conversational context management
- Progressive citizen profile building
- Scheme search integration
- Multilingual support (6 Indian languages)
"""
import os
import json
import base64
import hashlib
import logging
import uuid
import time
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from conversation_manager import ConversationManager
from models import CitizenProfile

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class VoiceService:
    """Service for processing voice queries with conversational context"""
    
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "ap-south-1")
        
        # AWS Clients
        self.s3_client = boto3.client('s3', region_name=self.region)
        self.transcribe_client = boto3.client('transcribe', region_name=self.region)
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=self.region)
        self.polly_client = boto3.client('polly', region_name=self.region)
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        
        # Configuration
        self.audio_bucket = os.getenv("S3_AUDIO_BUCKET")
        self.claude_model = "anthropic.claude-3-sonnet-20240229-v1:0"
        
        # Conversation Manager
        self.conversation_manager = ConversationManager()
        
        # DynamoDB tables
        table_prefix = os.getenv("DYNAMODB_TABLE_PREFIX", "voice-for-bharat")
        self.schemes_table = self.dynamodb.Table(f"{table_prefix}-schemes")
        
        # Language mappings
        self.language_codes = {
            "en": "en-IN",
            "hi": "hi-IN",
            "ta": "ta-IN",
            "te": "te-IN",
            "mr": "mr-IN",
            "kn": "kn-IN"
        }
        
        self.polly_voices = {
            "en": {"VoiceId": "Aditi", "Engine": "neural"},
            "hi": {"VoiceId": "Aditi", "Engine": "neural"},
            "ta": {"VoiceId": "Kajal", "Engine": "neural"},
            "te": {"VoiceId": "Kajal", "Engine": "neural"},
            "mr": {"VoiceId": "Aditi", "Engine": "neural"},
            "kn": {"VoiceId": "Aditi", "Engine": "neural"}
        }
    
    async def process_voice_query(
        self,
        audio_data: bytes,
        language: str = "hi",
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Complete voice processing pipeline (Legacy - maintained for backward compatibility)
        
        Args:
            audio_data: Audio file bytes (WAV/MP3)
            language: Language code (en, hi, ta, te, mr, kn)
            user_id: User identifier
        
        Returns:
            Response with text and audio URL
        """
        # Call new conversational method
        return await self.process_voice_query_with_context(
            audio_data=audio_data,
            language=language,
            user_id=user_id,
            session_id=None
        )
    
    async def process_voice_query_with_context(
        self,
        audio_data: bytes,
        language: str = "hi",
        user_id: str = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete voice processing pipeline with conversational context
        
        Args:
            audio_data: Audio file bytes (WAV/MP3)
            language: Language code (en, hi, ta, te, mr, kn)
            user_id: User identifier
            session_id: Optional session ID for conversation continuity
        
        Returns:
            Response with text, audio URL, and updated conversation context
        """
        try:
            logger.info(f"Processing voice query - Language: {language}, User: {user_id}, Session: {session_id}")
            
            # Get or create conversation session
            session = self.conversation_manager.get_or_create_session(
                session_id=session_id,
                user_id=user_id,
                language=language
            )
            
            # Step 1: Upload audio to S3
            audio_key = f"user-audio/{user_id}/{uuid.uuid4()}.wav"
            self.s3_client.put_object(
                Bucket=self.audio_bucket,
                Key=audio_key,
                Body=audio_data,
                ContentType='audio/wav'
            )
            audio_uri = f"s3://{self.audio_bucket}/{audio_key}"
            
            # Step 2: Transcribe audio to text
            transcription = await self.transcribe_audio(audio_uri, language)
            
            if not transcription or transcription.get("confidence", 0) < 0.5:
                return await self._generate_error_response(
                    "I'm sorry, I couldn't understand that. Could you please repeat?",
                    language,
                    session.session_id
                )
            
            user_text = transcription["text"]
            logger.info(f"Transcribed: {user_text}")
            
            # Add user message to session
            self.conversation_manager.add_message(
                session=session,
                role="USER",
                content=user_text
            )
            
            # Step 3: Extract intent and entities
            intent, entities = self._extract_intent_and_entities(user_text, language)
            
            # Step 4: Update citizen profile with extracted information
            if entities:
                self.conversation_manager.update_citizen_profile(session, entities)
            
            # Step 5: Determine what information is still needed
            profile_gaps = self.conversation_manager.get_profile_gaps(
                session.citizen_profile,
                required_for_intent=intent
            )
            
            # Step 6: Process with Claude AI (context-aware)
            ai_response = await self.process_with_claude_contextual(
                user_text=user_text,
                language=language,
                session=session,
                intent=intent,
                profile_gaps=profile_gaps
            )
            
            # Step 7: Add assistant message to session
            audio_url = await self.synthesize_speech(ai_response, language)
            self.conversation_manager.add_message(
                session=session,
                role="ASSISTANT",
                content=ai_response,
                audio_url=audio_url,
                intent=intent,
                entities=entities
            )
            
            # Step 8: Return complete response
            return {
                "success": True,
                "user_text": user_text,
                "response_text": ai_response,
                "audio_url": audio_url,
                "session_id": session.session_id,
                "language": language,
                "confidence": transcription.get("confidence", 0.9),
                "citizen_profile": session.citizen_profile.model_dump(),
                "current_intent": intent,
                "profile_gaps": profile_gaps
            }
            
        except Exception as e:
            logger.error(f"Voice processing error: {str(e)}", exc_info=True)
            return await self._generate_error_response(
                "I'm having trouble processing your request. Please try again.",
                language,
                session_id
            )
    
    async def transcribe_audio(
        self,
        audio_uri: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Amazon Transcribe
        
        Args:
            audio_uri: S3 URI of audio file
            language: Language code
        
        Returns:
            Dictionary with text and confidence
        """
        try:
            job_name = f"transcribe-{uuid.uuid4()}"
            language_code = self.language_codes.get(language, "en-IN")
            
            logger.info(f"Starting transcription job: {job_name}")
            
            # Start transcription job
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                LanguageCode=language_code,
                MediaFormat='wav',
                Media={'MediaFileUri': audio_uri},
                OutputBucketName=self.audio_bucket
            )
            
            # Wait for completion (with timeout)
            max_wait = 60  # seconds
            wait_time = 0
            
            while wait_time < max_wait:
                response = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                
                status = response['TranscriptionJob']['TranscriptionJobStatus']
                
                if status == 'COMPLETED':
                    # Get transcript
                    transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    transcript_data = self._fetch_transcript(transcript_uri)
                    
                    # Clean up job
                    try:
                        self.transcribe_client.delete_transcription_job(
                            TranscriptionJobName=job_name
                        )
                    except:
                        pass
                    
                    return {
                        "text": transcript_data["text"],
                        "confidence": transcript_data.get("confidence", 0.9)
                    }
                
                elif status == 'FAILED':
                    logger.error(f"Transcription failed: {response}")
                    return {"text": "", "confidence": 0.0}
                
                time.sleep(2)
                wait_time += 2
            
            logger.warning(f"Transcription timeout for job: {job_name}")
            return {"text": "", "confidence": 0.0}
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}", exc_info=True)
            return {"text": "", "confidence": 0.0}
    
    def _fetch_transcript(self, transcript_uri: str) -> Dict[str, Any]:
        """Fetch and parse transcript from S3"""
        import urllib.request
        
        try:
            with urllib.request.urlopen(transcript_uri) as response:
                data = json.loads(response.read())
                
            # Extract text and confidence
            results = data.get("results", {})
            transcripts = results.get("transcripts", [])
            
            if transcripts:
                text = transcripts[0].get("transcript", "")
                
                # Calculate average confidence
                items = results.get("items", [])
                confidences = [
                    float(item.get("alternatives", [{}])[0].get("confidence", 0))
                    for item in items
                    if "confidence" in item.get("alternatives", [{}])[0]
                ]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.9
                
                return {
                    "text": text,
                    "confidence": avg_confidence
                }
            
            return {"text": "", "confidence": 0.0}
            
        except Exception as e:
            logger.error(f"Error fetching transcript: {str(e)}")
            return {"text": "", "confidence": 0.0}
    
    async def process_with_claude(
        self,
        user_text: str,
        language: str,
        user_id: str
    ) -> str:
        """
        Process user query with Claude AI
        
        Args:
            user_text: Transcribed user text
            language: Language code
            user_id: User identifier
        
        Returns:
            AI-generated response text
        """
        try:
            # Build prompt for Claude
            prompt = self._build_claude_prompt(user_text, language)
            
            # Call Bedrock Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            logger.info(f"Calling Claude with prompt length: {len(prompt)}")
            
            response = self.bedrock_client.invoke_model(
                modelId=self.claude_model,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_text = response_body['content'][0]['text']
            
            logger.info(f"Claude response: {ai_text[:100]}...")
            
            return ai_text
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                logger.error("Bedrock access denied. Please request model access in AWS Console.")
                return "I'm currently unable to process your request. Please contact support."
            else:
                logger.error(f"Bedrock error: {str(e)}")
                return "I'm having trouble understanding your request. Please try again."
        
        except Exception as e:
            logger.error(f"Claude processing error: {str(e)}", exc_info=True)
            return "I'm having trouble processing your request. Please try again."
    
    def _build_claude_prompt(self, user_text: str, language: str) -> str:
        """Build prompt for Claude based on user query"""
        
        language_names = {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "mr": "Marathi",
            "kn": "Kannada"
        }
        
        lang_name = language_names.get(language, "English")
        
        prompt = f"""You are a helpful assistant for Voice for Bharat, a platform that helps Indian citizens find and apply for government welfare schemes.

User's query (in {lang_name}): {user_text}

Your task:
1. Understand the user's intent (searching for schemes, checking eligibility, asking about application status, etc.)
2. Provide a helpful, concise response in {lang_name}
3. If they're looking for schemes, mention that you can help them find relevant welfare programs
4. If they're asking about eligibility, explain that you need their profile information
5. Keep the response conversational and friendly
6. Maximum 2-3 sentences

Respond ONLY in {lang_name}. Be helpful and empathetic."""

        return prompt
    
    async def synthesize_speech(
        self,
        text: str,
        language: str
    ) -> str:
        """
        Synthesize speech using Amazon Polly
        
        Args:
            text: Text to convert to speech
            language: Language code
        
        Returns:
            S3 presigned URL for audio file
        """
        try:
            # Check cache first
            text_hash = hashlib.md5(text.encode()).hexdigest()
            cache_key = f"tts-cache/{language}/{text_hash}.mp3"
            
            # Check if cached audio exists
            try:
                self.s3_client.head_object(Bucket=self.audio_bucket, Key=cache_key)
                logger.info(f"TTS cache hit: {cache_key}")
                return self._generate_presigned_url(cache_key)
            except:
                pass  # Cache miss, generate new audio
            
            # Get voice configuration
            voice_config = self.polly_voices.get(language, self.polly_voices["en"])
            language_code = self.language_codes.get(language, "en-IN")
            
            logger.info(f"Synthesizing speech with voice: {voice_config['VoiceId']}")
            
            # Synthesize speech
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_config['VoiceId'],
                Engine=voice_config['Engine'],
                LanguageCode=language_code
            )
            
            # Read audio stream
            audio_data = response['AudioStream'].read()
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.audio_bucket,
                Key=cache_key,
                Body=audio_data,
                ContentType='audio/mpeg'
            )
            
            logger.info(f"TTS audio cached: {cache_key}")
            
            # Generate presigned URL
            return self._generate_presigned_url(cache_key)
            
        except Exception as e:
            logger.error(f"TTS error: {str(e)}", exc_info=True)
            return ""
    
    def _generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.audio_bucket,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return ""
    
    async def _generate_error_response(
        self,
        error_message: str,
        language: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate error response with audio"""
        
        # Translate error message if needed
        error_messages = {
            "en": error_message,
            "hi": "क्षमा करें, मुझे समझ नहीं आया। कृपया दोबारा कहें।",
            "ta": "மன்னிக்கவும், எனக்கு புரியவில்லை. தயவுசெய்து மீண்டும் சொல்லுங்கள்.",
            "te": "క్షమించండి, నాకు అర్థం కాలేదు. దయచేసి మళ్లీ చెప్పండి.",
            "mr": "माफ करा, मला समजले नाही. कृपया पुन्हा सांगा.",
            "kn": "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ."
        }
        
        localized_message = error_messages.get(language, error_message)
        audio_url = await self.synthesize_speech(localized_message, language)
        
        return {
            "success": False,
            "error": error_message,
            "response_text": localized_message,
            "audio_url": audio_url,
            "language": language,
            "session_id": session_id
        }
    
    def _extract_intent_and_entities(
        self,
        user_text: str,
        language: str
    ) -> tuple[str, Dict[str, Any]]:
        """
        Extract intent and entities from user text
        
        Args:
            user_text: User's transcribed text
            language: Language code
        
        Returns:
            Tuple of (intent, entities dict)
        """
        entities = {}
        intent = "GENERAL_QUERY"
        
        # Normalize text for pattern matching
        text_lower = user_text.lower()
        
        # Intent detection patterns by language
        scheme_keywords = {
            "en": ["scheme", "schemes", "program", "benefit", "welfare", "apply"],
            "hi": ["योजना", "योजनाओं", "कार्यक्रम", "लाभ", "आवेदन"],
            "te": ["పథకం", "పథకాలు", "కార్యక్రమం", "ప్రయోజనం", "దరఖాస్తు"],
            "ta": ["திட்டம்", "திட்டங்கள்", "திட்டவரை", "நன்மை", "விண்ணப்பம்"],
            "mr": ["योजना", "योजनांची", "कार्यक्रम", "लाभ", "अर्ज"],
            "kn": ["ಯೋಜನೆ", "ಯೋಜನೆಗಳು", "ಕಾರ್ಯಕ್ರಮ", "ಪ್ರಯೋಜನ", "ಅರ್ಜಿ"]
        }
        
        farmer_keywords = {
            "en": ["farmer", "agriculture", "farming", "crop", "land"],
            "hi": ["किसान", "कृषि", "खेती", "फसल", "जमीन"],
            "te": ["రైతు", "వ్యవసాయం", "పంట", "భూమి"],
            "ta": ["விவசாயி", "விவசாயம்", "பயிர்", "நிலம்"],
            "mr": ["शेतकरी", "शेती", "पीक", "जमीन"],
            "kn": ["ರೈತ", "ಕೃಷಿ", "ಬೆಳೆ", "ಭೂಮಿ"]
        }
        
        student_keywords = {
            "en": ["student", "education", "scholarship", "study", "college"],
            "hi": ["छात्र", "शिक्षा", "छात्रवृत्ति", "अध्ययन", "कॉलेज"],
            "te": ["విద్యార్థి", "విద్య", "స్కాలర్‌షిప్", "చదువు", "కాలేజీ"],
            "ta": ["மாணவர்", "கல்வி", "புலமைப்பரிசில்", "படிப்பு", "கல்லூரி"],
            "mr": ["विद्यार्थी", "शिक्षण", "शिष्यवृत्ती", "अभ्यास", "महाविद्यालय"],
            "kn": ["ವಿದ್ಯಾರ್ಥಿ", "ಶಿಕ್ಷಣ", "ವಿದ್ಯಾರ್ಥಿವೇತನ", "ಅಧ್ಯಯನ", "ಕಾಲೇಜು"]
        }
        
        # Detect scheme search intent
        for keyword in scheme_keywords.get(language, scheme_keywords["en"]):
            if keyword in text_lower:
                intent = "SEARCH_SCHEMES"
                break
        
        # Extract farmer occupation
        for keyword in farmer_keywords.get(language, farmer_keywords["en"]):
            if keyword in text_lower:
                entities["is_farmer"] = True
                entities["occupation"] = "farmer"
                break
        
        # Extract student occupation
        for keyword in student_keywords.get(language, student_keywords["en"]):
            if keyword in text_lower:
                entities["is_student"] = True
                entities["occupation"] = "student"
                break
        
        # Extract state mentions (simple pattern matching)
        state_patterns = {
            "telangana": "TS", "తెలంగాణ": "TS",
            "andhra pradesh": "AP", "ఆంధ్ర": "AP",
            "karnataka": "KA", "ಕರ್ನಾಟಕ": "KA",
            "tamil nadu": "TN", "தமிழ்நாடு": "TN",
            "maharashtra": "MH", "महाराष्ट्र": "MH",
            "kerala": "KL", "കേരളം": "KL"
        }
        
        for state_name, state_code in state_patterns.items():
            if state_name in text_lower:
                entities["state"] = state_code
                break
        
        logger.info(f"Extracted intent: {intent}, entities: {entities}")
        return intent, entities
    
    async def process_with_claude_contextual(
        self,
        user_text: str,
        language: str,
        session: Any,
        intent: str,
        profile_gaps: List[str]
    ) -> str:
        """
        Process user query with Claude AI using conversation context
        
        Args:
            user_text: Transcribed user text
            language: Language code
            session: Conversation session
            intent: Detected intent
            profile_gaps: Missing profile information
        
        Returns:
            AI-generated response text
        """
        try:
            # Build context-aware prompt
            prompt = self._build_contextual_prompt(
                user_text=user_text,
                language=language,
                session=session,
                intent=intent,
                profile_gaps=profile_gaps
            )
            
            # Call Bedrock Claude
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            logger.info(f"Calling Claude with contextual prompt (length: {len(prompt)})")
            
            response = self.bedrock_client.invoke_model(
                modelId=self.claude_model,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_text = response_body['content'][0]['text']
            
            logger.info(f"Claude response: {ai_text[:100]}...")
            
            return ai_text
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                logger.error("Bedrock access denied. Please request model access in AWS Console.")
                return "I'm currently unable to process your request. Please contact support."
            else:
                logger.error(f"Bedrock error: {str(e)}")
                return "I'm having trouble understanding your request. Please try again."
        
        except Exception as e:
            logger.error(f"Claude processing error: {str(e)}", exc_info=True)
            return "I'm having trouble processing your request. Please try again."
    
    def _build_contextual_prompt(
        self,
        user_text: str,
        language: str,
        session: Any,
        intent: str,
        profile_gaps: List[str]
    ) -> str:
        """Build context-aware prompt for Claude"""
        
        language_names = {
            "en": "English",
            "hi": "Hindi",
            "ta": "Tamil",
            "te": "Telugu",
            "mr": "Marathi",
            "kn": "Kannada"
        }
        
        lang_name = language_names.get(language, "English")
        profile = session.citizen_profile
        
        # Build conversation history context
        history = self.conversation_manager.get_conversation_history(session, last_n=3)
        history_text = "\n".join([
            f"{msg.role}: {msg.content}" for msg in history
        ])
        
        # Build citizen profile context
        profile_context = f"""
Current citizen information known:
- Language: {lang_name}
- State: {profile.state or "Not provided"}
- Occupation: {profile.occupation or "Not provided"}
- Farmer: {"Yes" if profile.is_farmer else "Unknown"}
- Student: {"Yes" if profile.is_student else "Unknown"}
"""
        
        # Determine response strategy
        if intent == "SEARCH_SCHEMES" and profile_gaps:
            # Need to ask for missing information
            strategy = f"""
Your task: Ask for ONE missing piece of information to help find relevant schemes.
Missing information: {', '.join(profile_gaps)}
Ask only for the MOST IMPORTANT missing item. Be conversational and natural.
"""
        elif intent == "SEARCH_SCHEMES" and not profile_gaps:
            # Have enough info to search
            strategy = f"""
Your task: Inform the user that you're searching for relevant schemes based on their profile.
Confirm what you know about them and tell them you'll find matching schemes.
"""
        else:
            # General conversational response
            strategy = f"""
Your task: Provide a helpful, conversational response in {lang_name}.
Help them understand how to use the platform to find government welfare schemes.
"""
        
        prompt = f"""You are a helpful assistant for Voice for Bharat, helping Indian citizens find government welfare schemes.

{profile_context}

Recent conversation:
{history_text if history_text else "This is the first message."}

User's current query (in {lang_name}): {user_text}

{strategy}

IMPORTANT RULES:
1. Respond ONLY in {lang_name}
2. Be warm, conversational, and empathetic
3. Keep response to 2-3 sentences maximum
4. Do NOT ask for multiple pieces of information at once
5. Do NOT repeat questions already answered
6. Do NOT invent scheme details - only acknowledge their request

Your response in {lang_name}:"""

        return prompt
    
    async def _generate_error_response(
        self,
        error_message: str,
        language: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate error response with audio"""
        
        # Translate error message if needed
        error_messages = {
            "en": error_message,
            "hi": "क्षमा करें, मुझे समझ नहीं आया। कृपया दोबारा कहें।",
            "ta": "மன்னிக்கவும், எனக்கு புரியவில்லை. தயவுசெய்து மீண்டும் சொல்லுங்கள்.",
            "te": "క్షమించండి, నాకు అర్థం కాలేదు. దయచేసి మళ్లీ చెప్పండి.",
            "mr": "माफ करा, मला समजले नाही. कृपया पुन्हा सांगा.",
            "kn": "ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ."
        }
        
        localized_message = error_messages.get(language, error_message)
        audio_url = await self.synthesize_speech(localized_message, language)
        
        return {
            "success": False,
            "error": error_message,
            "response_text": localized_message,
            "audio_url": audio_url,
            "language": language,
            "session_id": session_id
        }
