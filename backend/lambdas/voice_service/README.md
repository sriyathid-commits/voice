# Voice Service Lambda

The Voice Service is the **critical path** service for Voice for Bharat. It orchestrates the entire voice interaction flow including speech-to-text, natural language understanding, and text-to-speech conversion.

## Overview

This service implements the `processVoiceQuery` algorithm from the design document and provides:

- Real-time WebSocket communication for voice streaming
- REST API endpoint for voice query processing
- Speech-to-text using Amazon Bedrock Titan
- Natural language processing using Anthropic Claude 3 Sonnet
- Text-to-speech using Amazon Bedrock Titan
- Intent recognition (SEARCH_SCHEMES, CHECK_ELIGIBILITY, START_APPLICATION, GET_STATUS)
- Conversation session management
- Audio file storage in S3 with presigned URLs
- Support for 6 Indian languages (en, hi, mr, kn, ta, te)

## Architecture

```
User Audio → WebSocket/REST → Voice Service → Bedrock (STT) → Claude (NLP) 
→ Scheme Service → Claude (Response) → Bedrock (TTS) → S3 → User
```

## Endpoints

### WebSocket: `/ws/voice`

Real-time voice interaction endpoint.

**Message Types:**
- `start`: Initialize session
- `audio`: Send audio chunk
- `stop`: Process complete audio
- `ping`: Keep-alive

**Example:**
```json
{
  "type": "start",
  "sessionId": "uuid",
  "userId": "user-123",
  "language": "hi"
}
```

### REST: `POST /voice/query`

Process voice query via REST API.

**Parameters:**
- `audio`: Audio file (multipart)
- `session_id`: Session ID
- `user_id`: User ID
- `language`: Language code (default: "en")

**Response:**
```json
{
  "text": "I found 3 schemes for you...",
  "audio_url": "https://s3.../audio.mp3",
  "context": {...},
  "schemes": [...]
}
```

### REST: `GET /voice/session/{session_id}`

Get conversation session details.

### REST: `POST /voice/session/{session_id}/end`

End conversation session.

## Configuration

### Lambda Settings
- Memory: 2GB
- Timeout: 300s (5 minutes)
- Runtime: Python 3.11
- Architecture: arm64 (Graviton2)

### Environment Variables
- `AWS_REGION`: AWS region (default: ap-south-1)
- `DYNAMODB_TABLE_PREFIX`: Table name prefix
- `S3_AUDIO_BUCKET`: Audio storage bucket
- `S3_DOCUMENTS_BUCKET`: Documents bucket

## Supported Languages

- English (en) - en-IN
- Hindi (hi) - hi-IN
- Marathi (mr) - mr-IN
- Kannada (kn) - kn-IN
- Tamil (ta) - ta-IN
- Telugu (te) - te-IN

## Intent Recognition

The service recognizes the following intents:

1. **SEARCH_SCHEMES**: Search for welfare schemes
2. **CHECK_ELIGIBILITY**: Check eligibility for a scheme
3. **START_APPLICATION**: Create application draft
4. **GET_STATUS**: Get application status
5. **FIND_HELPLINE**: Find helpline information
6. **GET_GUIDE**: Get guide content
7. **GENERAL_QUERY**: Fallback for other queries

## Audio Processing

### Input Formats
- WAV (16kHz, mono recommended)
- MP3
- OGG

### Output Format
- MP3 (for TTS responses)

### Storage
- User audio: `conversations/{sessionId}/user/{messageId}.wav`
- Assistant audio: `conversations/{sessionId}/assistant/{messageId}.mp3`
- TTS cache: `tts-cache/{language}/{textHash}.mp3`

## Confidence Thresholds

- Transcription: 0.7
- Intent recognition: 0.6
- Eligibility match: 0.5

## Error Handling

The service handles errors gracefully:
- Low confidence transcription → Ask user to repeat
- NLP errors → Fallback to general query
- Service errors → Return error message with audio

## Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Test WebSocket locally
python test_websocket.py
```

## Deployment

```bash
# Build and deploy
sam build
sam deploy --guided

# Or use deployment script
./deploy.sh voice-service
```

## Monitoring

Key metrics to monitor:
- WebSocket connection count
- Average processing time
- Transcription confidence scores
- Intent recognition accuracy
- TTS cache hit rate
- Error rates by type

## Dependencies

See `requirements.txt` for full list:
- fastapi
- mangum
- boto3
- pydantic
- websockets
