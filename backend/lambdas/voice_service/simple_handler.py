"""
Voice Service Lambda Handler with Real AI Integration
Uses boto3 (pre-installed) for Transcribe, Bedrock, and Polly
"""
import json
import boto3
import base64
import uuid
import time
from datetime import datetime
from urllib.parse import parse_qs

# Initialize AWS clients
transcribe = boto3.client('transcribe', region_name='ap-south-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-south-1')
polly = boto3.client('polly', region_name='ap-south-1')
s3 = boto3.client('s3', region_name='ap-south-1')

# Configuration
AUDIO_BUCKET = 'voice-for-bharat-audio'
BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

# Language mappings
TRANSCRIBE_LANGUAGES = {
    'en': 'en-US',
    'hi': 'hi-IN',
    'ta': 'ta-IN',
    'te': 'te-IN',
    'mr': 'mr-IN',
    'kn': 'kn-IN'
}

POLLY_VOICES = {
    'en': {'Engine': 'neural', 'VoiceId': 'Joanna'},
    'hi': {'Engine': 'standard', 'VoiceId': 'Aditi'}
}

def lambda_handler(event, context):
    """
    Main Lambda handler for voice processing
    """
    print(f"Event: {json.dumps(event)}")
    
    try:
        # Handle different event types
        if event.get('httpMethod') == 'POST' and '/voice/query' in event.get('path', ''):
            return handle_voice_query(event)
        elif event.get('httpMethod') == 'GET' and '/health' in event.get('path', ''):
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'status': 'healthy', 'service': 'voice-service-ai'})
            }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Voice Service with AI is running',
                    'endpoints': ['/voice/query', '/health'],
                    'ai_services': ['Transcribe', 'Bedrock Claude', 'Polly']
                })
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }

def handle_voice_query(event):
    """
    Handle voice query with real AI integration
    """
    try:
        # Parse multipart form data
        content_type = event.get('headers', {}).get('content-type', '') or event.get('headers', {}).get('Content-Type', '')
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if is_base64:
            body = base64.b64decode(body)
        
        # Extract parameters from body
        language = 'hi'  # Default to Hindi
        session_id = f"session-{int(time.time())}"
        user_id = 'demo-user'
        audio_data = None
        
        # Try to parse form data
        if 'multipart/form-data' in content_type:
            # For now, use a simple approach - extract audio from body
            # In production, you'd use a proper multipart parser
            print("Received multipart form data")
            # Since we can't easily parse multipart without dependencies,
            # we'll extract the audio binary data
            if isinstance(body, bytes):
                audio_data = body
        
        # If no audio data, return test response
        if not audio_data or len(audio_data) < 100:
            print("No valid audio data, returning test response")
            return get_test_response(language, session_id)
        
        # Step 1: Upload audio to S3 for Transcribe
        audio_key = f"stt-recordings/{user_id}/{session_id}.wav"
        s3.put_object(
            Bucket=AUDIO_BUCKET,
            Key=audio_key,
            Body=audio_data,
            ContentType='audio/wav'
        )
        audio_uri = f"s3://{AUDIO_BUCKET}/{audio_key}"
        print(f"Uploaded audio to: {audio_uri}")
        
        # Step 2: Transcribe audio
        user_text = transcribe_audio(audio_uri, language, session_id)
        print(f"Transcribed text: {user_text}")
        
        # Step 3: Get AI response from Bedrock
        ai_response = get_bedrock_response(user_text, language)
        print(f"AI response: {ai_response}")
        
        # Step 4: Generate speech with Polly (only for Hindi and English)
        audio_url = None
        if language in POLLY_VOICES:
            audio_url = generate_speech(ai_response, language, session_id)
            print(f"Generated speech: {audio_url}")
        
        # Return response
        response_data = {
            'user_text': user_text,
            'response_text': ai_response,
            'audio_url': audio_url,
            'language': language,
            'session_id': session_id,
            'status': 'success',
            'ai_powered': True
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"Error in handle_voice_query: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return fallback response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'user_text': 'Audio processing in progress...',
                'response_text': 'नमस्ते! मैं आपकी मदद के लिए यहाँ हूँ। कृपया अपना सवाल पूछें।',
                'language': 'hi',
                'session_id': f"session-{int(time.time())}",
                'status': 'fallback',
                'error': str(e)
            })
        }

def transcribe_audio(audio_uri, language, session_id):
    """
    Transcribe audio using Amazon Transcribe
    """
    try:
        job_name = f"transcribe-{session_id}"
        language_code = TRANSCRIBE_LANGUAGES.get(language, 'hi-IN')
        
        # Start transcription job
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_uri},
            MediaFormat='wav',
            LanguageCode=language_code
        )
        
        # Wait for completion (max 30 seconds)
        max_tries = 30
        for i in range(max_tries):
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            
            if job_status == 'COMPLETED':
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                # Get transcript from S3
                import urllib.request
                with urllib.request.urlopen(transcript_uri) as response:
                    transcript_data = json.loads(response.read())
                    text = transcript_data['results']['transcripts'][0]['transcript']
                    return text if text else "Could not transcribe audio"
            elif job_status == 'FAILED':
                return "Transcription failed"
            
            time.sleep(1)
        
        return "Transcription timeout"
        
    except Exception as e:
        print(f"Transcribe error: {str(e)}")
        return "Error transcribing audio"

def get_bedrock_response(user_text, language):
    """
    Get AI response from Bedrock Claude
    """
    try:
        # Create prompt based on language
        system_prompt = """You are a helpful assistant for Voice for Bharat, helping Indian citizens find government welfare schemes.
Respond in the same language as the user's question. Be concise and helpful."""
        
        # Prepare request for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            "temperature": 0.7
        }
        
        # Call Bedrock
        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        ai_text = response_body['content'][0]['text']
        
        return ai_text
        
    except Exception as e:
        print(f"Bedrock error: {str(e)}")
        # Fallback responses by language
        fallbacks = {
            'hi': 'नमस्ते! मैं आपकी मदद के लिए यहाँ हूँ। कृपया अपना सवाल फिर से पूछें।',
            'en': 'Hello! I am here to help you. Please ask your question again.',
            'ta': 'வணக்கம்! நான் உங்களுக்கு உதவ இங்கே இருக்கிறேன்.',
            'te': 'నమస్కారం! నేను మీకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను.',
            'mr': 'नमस्कार! मी तुम्हाला मदत करण्यासाठी येथे आहे.',
            'kn': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ.'
        }
        return fallbacks.get(language, fallbacks['hi'])

def generate_speech(text, language, session_id):
    """
    Generate speech using Amazon Polly
    """
    try:
        voice_config = POLLY_VOICES.get(language)
        if not voice_config:
            return None
        
        # Generate speech
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_config['VoiceId'],
            Engine=voice_config['Engine']
        )
        
        # Upload to S3
        audio_key = f"tts-cache/{language}/{session_id}.mp3"
        s3.put_object(
            Bucket=AUDIO_BUCKET,
            Key=audio_key,
            Body=response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )
        
        # Generate presigned URL (valid for 1 hour)
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': AUDIO_BUCKET, 'Key': audio_key},
            ExpiresIn=3600
        )
        
        return url
        
    except Exception as e:
        print(f"Polly error: {str(e)}")
        return None

def get_test_response(language, session_id):
    """
    Return test response when no audio data
    """
    responses = {
        'hi': 'नमस्ते! मैं आपकी मदद के लिए यहाँ हूँ। कृपया अपना सवाल पूछें।',
        'en': 'Hello! I am here to help you. Please ask your question.',
        'ta': 'வணக்கம்! நான் உங்களுக்கு உதவ இங்கே இருக்கிறேன்.',
        'te': 'నమస్కారం! నేను మీకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను.',
        'mr': 'नमस्कार! मी तुम्हाला मदत करण्यासाठी येथे आहे.',
        'kn': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ.'
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'user_text': 'Test mode - no audio received',
            'response_text': responses.get(language, responses['hi']),
            'language': language,
            'session_id': session_id,
            'status': 'test_mode',
            'message': 'AI services ready - send audio to activate'
        })
    }
