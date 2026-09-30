"""
Voice Service Lambda Handler
Handles WebSocket connections and voice query processing for Voice for Bharat.
"""
import json
import os
import logging
from typing import Dict, Any
from mangum import Mangum
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from service import VoiceService

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="Voice Service API",
    description="Voice processing service for Voice for Bharat",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Voice Service
voice_service = VoiceService()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "voice-service"}


@app.websocket("/ws/voice")
async def websocket_voice_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time voice interaction
    
    Message types:
    - StartRecording: {"type": "start", "sessionId": "...", "language": "en"}
    - AudioChunk: {"type": "audio", "data": "base64_audio_data"}
    - StopRecording: {"type": "stop"}
    
    Response types:
    - TranscriptionUpdate: {"type": "transcription", "text": "..."}
    - ResponseReady: {"type": "response", "text": "...", "audioUrl": "..."}
    - Error: {"type": "error", "message": "..."}
    """
    await websocket.accept()
    session_id = None
    
    try:
        logger.info("WebSocket connection established")
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "start":
                # Start recording session
                session_id = message.get("sessionId")
                language = message.get("language", "en")
                user_id = message.get("userId")
                
                logger.info(f"Starting voice session: {session_id}, language: {language}")
                
                # Initialize or retrieve session
                session = await voice_service.get_or_create_session(session_id, user_id, language)
                
                await websocket.send_json({
                    "type": "ready",
                    "sessionId": session_id,
                    "message": "Ready to receive audio"
                })
            
            elif message_type == "audio":
                # Receive audio chunk
                audio_data = message.get("data")
                
                if not session_id:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Session not started. Send 'start' message first."
                    })
                    continue
                
                # Process audio chunk (accumulate for now)
                await voice_service.accumulate_audio_chunk(session_id, audio_data)
            
            elif message_type == "stop":
                # Stop recording and process complete audio
                if not session_id:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Session not started."
                    })
                    continue
                
                logger.info(f"Processing voice query for session: {session_id}")
                
                # Send processing status
                await websocket.send_json({
                    "type": "processing",
                    "message": "Processing your query..."
                })
                
                # Process the complete audio
                response = await voice_service.process_voice_query_websocket(session_id)
                
                # Send response
                await websocket.send_json({
                    "type": "response",
                    "text": response.get("text"),
                    "audioUrl": response.get("audio_url"),
                    "context": response.get("context"),
                    "schemes": response.get("schemes", [])
                })
            
            elif message_type == "ping":
                # Keep-alive ping
                await websocket.send_json({"type": "pong"})
            
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Internal server error: {str(e)}"
            })
        except:
            pass
    finally:
        # Clean up session if needed
        if session_id:
            await voice_service.cleanup_audio_buffer(session_id)


@app.post("/voice/query")
async def process_voice_query(
    audio: UploadFile = File(...),
    session_id: str = Form(...),
    language: str = Form(default="en"),
    user_id: str = Form(...)
):
    """
    REST endpoint for voice query processing (alternative to WebSocket)
    
    Args:
        audio: Audio file (WAV, MP3, OGG)
        session_id: Conversation session ID
        language: Language code (en, hi, mr, kn, ta, te)
        user_id: User ID
    
    Returns:
        JSON response with text, audio URL, and context
    """
    try:
        logger.info(f"Processing voice query - Session: {session_id}, Language: {language}")
        
        # Read audio file
        audio_data = await audio.read()
        
        # Process voice query — session_id is passed as a keyword arg;
        # the service signature is (audio_data, language, user_id, session_id=None)
        response = await voice_service.process_voice_query(
            audio_data=audio_data,
            language=language,
            user_id=user_id,
            session_id=session_id or None,
        )
        
        return JSONResponse(content=response)
    
    except Exception as e:
        logger.error(f"Error processing voice query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/voice/session/{session_id}")
async def get_conversation_session(session_id: str):
    """
    Get conversation session details
    
    Args:
        session_id: Conversation session ID
    
    Returns:
        Session details including messages and context
    """
    try:
        session = await voice_service.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return JSONResponse(content=session)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice/session/{session_id}/end")
async def end_conversation_session(session_id: str):
    """
    End conversation session
    
    Args:
        session_id: Conversation session ID
    
    Returns:
        Success message
    """
    try:
        await voice_service.end_session(session_id)
        return {"message": "Session ended successfully", "sessionId": session_id}
    
    except Exception as e:
        logger.error(f"Error ending session: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Lambda handler
handler = Mangum(app, lifespan="off")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function
    
    Args:
        event: Lambda event
        context: Lambda context
    
    Returns:
        Lambda response
    """
    return handler(event, context)
