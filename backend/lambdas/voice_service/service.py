"""
Voice Service - Real AI Implementation
Uses Amazon Transcribe (STT), Bedrock Claude (NLU), and Polly (TTS)
"""
import os
import json
import base64
import hashlib
import logging
import uuid
import time
from typing import Dict, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class VoiceService:
    """Service for processing voice queries with real AWS AI services"""
    
    def __init__(self):
        self.region = os.getenv("AWS_REGION", "ap-south-1")
        
        # AWS Clients
        self.s3_client = boto3.client('s3', region_name=self.region)
        self.transcribe_client = boto3.client('transcribe', region_name=self.region)
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=self.region)
        self.polly_client = boto3.client('polly', region_name=self.region)
        
        # Configuration
        self.audio_bucket = os.getenv("S3_AUDIO_BUCKET")
        self.claude_model = "anthropic.claude-3-sonnet-20240229-v1:0"
        
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
            "mr": {"VoiceId": "Aditi", "Engine": "neural"},  # Fallback to Hindi voice
            "kn": {"VoiceId": "Aditi", "Engine": "neural"}   # Fallback to Hindi voice
        }
    
    async def process_voice_query(
        self,
        audio_data: bytes,
        language: str = "hi",
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Complete voice processing pipeline
        
        Args:
            audio_data: Audio file bytes (WAV/MP3)
            language: Language code (en, hi, ta, te, mr, kn)
            user_id: User identifier
        
        Returns:
            Response with text and audio URL
        """
        try:
            logger.info(f"Processing voice query - Language: {language}, User: {user_id}")
            
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
                    language
                )
            
            user_text = transcription["text"]
            logger.info(f"Transcribed: {user_text}")
            
            # Step 3: Process with Claude AI
            ai_response = await self.process_with_claude(user_text, language, user_id)
            
            # Step 4: Synthesize speech response
            audio_url = await self.synthesize_speech(ai_response, language)
            
            # Step 5: Return complete response
            return {
                "success": True,
                "user_text": user_text,
                "response_text": ai_response,
                "audio_url": audio_url,
                "language": language,
                "confidence": transcription.get("confidence", 0.9)
            }
            
        except Exception as e:
            logger.error(f"Voice processing error: {str(e)}", exc_info=True)
            return await self._generate_error_response(
                "I'm having trouble processing your request. Please try again.",
                language
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
        language: str
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
            "language": language
        }
