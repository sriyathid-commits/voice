# Test Voice Assistant - Quick Guide

## 🎯 Quick Test (After CloudFormation Update)

### Step 1: Open Assistant
```
https://bharatvisionxai.vercel.app/assistant
```

### Step 2: Test with These Queries

**Hindi (Best Experience - Has TTS)**
- "मुझे राशन कार्ड चाहिए" (I need a ration card)
- "किसान योजना के बारे में बताओ" (Tell me about farmer schemes)
- "आयुष्मान भारत क्या है?" (What is Ayushman Bharat?)

**English (Has TTS)**
- "How to apply for Ayushman Bharat?"
- "What schemes are available for farmers?"
- "Tell me about education scholarships"

**Tamil (Text Only - No TTS)**
- "எனக்கு ரேஷன் கார்டு வேண்டும்" (I need a ration card)

**Telugu (Text Only - No TTS)**
- "నాకు రేషన్ కార్డు కావాలి" (I need a ration card)

**Marathi (Text Only - No TTS)**
- "मला शिधापत्रिका हवी आहे" (I need a ration card)

**Kannada (Text Only - No TTS)**
- "ನನಗೆ ಪಡಿತರ ಚೀಟಿ ಬೇಕು" (I need a ration card)

## 🔍 What to Expect

### Recording Phase (5 seconds)
- Microphone button turns RED and pulses
- Status: "Listening... (speak now)"
- Browser may ask for microphone permission (allow it)

### Processing Phase (5-10 seconds)
- Button turns YELLOW
- Status: "Processing with AI..."
- Backend is calling:
  1. Amazon Transcribe (STT)
  2. Amazon Bedrock Claude (AI)
  3. Amazon Polly (TTS)

### Response Phase
- Button turns GREEN
- Status: "Playing response..."
- You see:
  - **Your transcript**: What you said
  - **AI response**: Text answer
  - **Audio plays**: For English/Hindi only

## ✅ Success Indicators

1. **Microphone works**: Button turns red when clicked
2. **Recording works**: Status shows "Listening..."
3. **API works**: Status changes to "Processing..."
4. **Transcribe works**: You see "You said: [your text]"
5. **Claude works**: You see "AI Response: [answer]"
6. **Polly works**: Audio plays (English/Hindi only)

## ❌ Common Issues

### "Could not access microphone"
- **Fix**: Click the lock icon in browser address bar
- Allow microphone access
- Refresh page and try again

### "Failed to process voice query"
- **Fix**: Check if CloudFormation update is complete
- Status should be "UPDATE_COMPLETE"
- Wait a few minutes after update

### "Missing Authentication Token"
- **Fix**: CloudFormation stack not updated yet
- Follow steps in `VOICE_ASSISTANT_COMPLETE.md`

### No audio plays (but text shows)
- **Expected**: Tamil, Telugu, Marathi, Kannada don't have TTS
- **Fix for English/Hindi**: Check browser audio settings

## 🔧 Debug Steps

### 1. Check Browser Console (F12)
```javascript
// Should see:
"Processing voice query..."
"API response received"
"Playing audio..."
```

### 2. Check Network Tab (F12 → Network)
- Look for POST to `/voice/query`
- Status should be 200 OK
- Response should have `user_text` and `response_text`

### 3. Check CloudFormation
```
https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1
```
- Stack: `voicebharatai`
- Status: `UPDATE_COMPLETE` ✅

### 4. Check Lambda Logs
```
https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fvoice-for-bharat-voice-service-dev
```
- Look for recent invocations
- Check for errors

## 📊 Expected Response Format

```json
{
  "user_text": "मुझे राशन कार्ड चाहिए",
  "response_text": "राशन कार्ड के लिए आवेदन करने के लिए...",
  "audio_url": "https://d18s1aceaoasx3.cloudfront.net/audio/...",
  "language": "hi",
  "session_id": "session-1234567890"
}
```

## 🎉 Success Criteria

- ✅ Can record audio
- ✅ Transcript appears correctly
- ✅ AI response is relevant
- ✅ Audio plays (for English/Hindi)
- ✅ Can do multiple queries in a row

## 📞 Support

If issues persist:
1. Check `VOICE_ASSISTANT_COMPLETE.md` for detailed setup
2. Check `UPDATE_VOICE_API.md` for CloudFormation update steps
3. Check Lambda logs in CloudWatch
4. Verify all AWS services are in `ap-south-1` region
