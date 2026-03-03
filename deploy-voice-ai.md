# Deploy Real AI Voice Services - Step by Step

## 🎯 Goal
Update the Voice for Bharat backend with REAL AI voice services (Transcribe, Claude, Polly)

## ✅ What's Already Done
1. ✅ CloudFormation template updated with IAM permissions
2. ✅ Voice service code completely rewritten with real AI
3. ✅ Infrastructure already deployed (voicebharatai stack)

## 🚀 Deployment Options

### Option 1: AWS Console (Easiest - Recommended)

#### Step 1: Package Lambda Code
1. Open File Explorer
2. Go to: `C:\Users\yathi\voice\backend\lambdas\voice_service`
3. Select all files: `handler.py`, `service.py`, `models.py`, `requirements.txt`, `__init__.py`
4. Right-click → Send to → Compressed (zipped) folder
5. Name it: `voice_service.zip`

#### Step 2: Update Lambda via Console
1. Open: https://ap-south-1.console.aws.amazon.com/lambda/
2. Search for: `voice-for-bharat-voice-service-dev`
3. Click on the function
4. Click "Upload from" → ".zip file"
5. Upload `voice_service.zip`
6. Click "Save"
7. Wait for deployment to complete

#### Step 3: Update Lambda Configuration
1. In the same Lambda function page
2. Go to "Configuration" tab → "General configuration"
3. Click "Edit"
4. Set:
   - Memory: 2048 MB (already set)
   - Timeout: 5 minutes (300 seconds) (already set)
5. Click "Save"

#### Step 4: Update Environment Variables
1. Go to "Configuration" tab → "Environment variables"
2. Verify these exist:
   - `S3_AUDIO_BUCKET`: voice-for-bharat-audio-dev-[ACCOUNT_ID]
   - `BEDROCK_REGION`: ap-south-1
   - `AWS_REGION`: ap-south-1
3. If missing, add them

#### Step 5: Request Bedrock Access
1. Open: https://ap-south-1.console.aws.amazon.com/bedrock/
2. Click "Model access" in left sidebar
3. Click "Manage model access" (orange button)
4. Find "Anthropic" section
5. Check: ✅ Claude 3 Sonnet
6. Click "Request model access"
7. Wait for approval (usually instant)

#### Step 6: Test Voice Services

**Test Polly (TTS) - Works Immediately:**
1. Open: https://ap-south-1.console.aws.amazon.com/polly/
2. Click "Try Polly"
3. Select:
   - Engine: Neural
   - Language: Hindi, Indian (hi-IN)
   - Voice: Aditi
4. Enter text: `नमस्ते, आपका स्वागत है`
5. Click "Listen"
6. You should hear Hindi speech! ✅

**Test Transcribe (STT) - Works Immediately:**
1. Open: https://ap-south-1.console.aws.amazon.com/transcribe/
2. Click "Create job"
3. Job name: `test-job-1`
4. Language: Hindi, Indian (hi-IN)
5. Upload a Hindi audio file (WAV or MP3)
6. Click "Create job"
7. Wait for completion
8. View transcript ✅

**Test Lambda Function:**
1. Open: https://ap-south-1.console.aws.amazon.com/lambda/
2. Go to: `voice-for-bharat-voice-service-dev`
3. Click "Test" tab
4. Create test event:
```json
{
  "body": "{\"text\": \"Hello, test query\"}",
  "httpMethod": "POST"
}
```
5. Click "Test"
6. Check logs for any errors

---

### Option 2: Command Line (If AWS CLI is installed)

#### Install AWS CLI (if not installed):
```powershell
# Download AWS CLI installer
# https://awscli.amazonaws.com/AWSCLIV2.msi
# Run the installer
```

#### Deploy via CLI:
```bash
# Navigate to backend
cd C:\Users\yathi\voice\backend

# Package Lambda
Compress-Archive -Path lambdas\voice_service\* -DestinationPath voice_service.zip -Force

# Update Lambda function
aws lambda update-function-code `
  --function-name voice-for-bharat-voice-service-dev `
  --zip-file fileb://voice_service.zip `
  --region ap-south-1
```

---

## 🧪 Testing After Deployment

### Test 1: Check Lambda Logs
1. Open: https://ap-south-1.console.aws.amazon.com/cloudwatch/
2. Go to "Log groups"
3. Find: `/aws/lambda/voice-for-bharat-voice-service-dev`
4. Check recent logs for errors

### Test 2: Test Polly Voice
```powershell
# If AWS CLI is installed
aws polly synthesize-speech `
  --text "नमस्ते, आपका स्वागत है" `
  --output-format mp3 `
  --voice-id Aditi `
  --engine neural `
  --language-code hi-IN `
  --region ap-south-1 `
  output.mp3

# Play the audio
start output.mp3
```

### Test 3: Test Complete Pipeline
1. Use Postman or curl to call API:
```bash
POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/voice/query
Content-Type: multipart/form-data

Fields:
- audio: [upload WAV file]
- session_id: test-session-123
- language: hi
- user_id: test-user-123
```

---

## 📊 Verify Deployment

### Check 1: Lambda Function Updated
1. Open Lambda console
2. Go to `voice-for-bharat-voice-service-dev`
3. Check "Last modified" timestamp - should be recent
4. Check code - should see `transcribe_audio()`, `process_with_claude()`, `synthesize_speech()` methods

### Check 2: IAM Permissions
1. Open Lambda console
2. Go to `voice-for-bharat-voice-service-dev`
3. Click "Configuration" → "Permissions"
4. Click on the execution role
5. Verify policies exist:
   - TranscribeAccess ✅
   - PollyAccess ✅
   - BedrockAccess ✅

### Check 3: Bedrock Access
1. Open: https://ap-south-1.console.aws.amazon.com/bedrock/
2. Click "Model access"
3. Verify: Claude 3 Sonnet shows "Access granted" ✅

---

## 🎯 Success Criteria

After deployment, you should have:
- ✅ Lambda function updated with real AI code
- ✅ Polly working (test in console)
- ✅ Transcribe working (test in console)
- ✅ Bedrock access granted for Claude
- ✅ No errors in CloudWatch logs
- ✅ API endpoint responding

---

## 🔧 Troubleshooting

### Issue: Lambda deployment fails
**Solution:** Check zip file contains all required files

### Issue: Bedrock access denied
**Solution:** Request model access in Bedrock console

### Issue: Transcribe job fails
**Solution:** Check audio file format (WAV, MP3, OGG supported)

### Issue: Polly synthesis fails
**Solution:** Check language code matches voice (hi-IN for Aditi)

### Issue: Lambda timeout
**Solution:** Increase timeout to 300 seconds (5 minutes)

---

## 📞 Next Steps After Deployment

1. ✅ Deploy Lambda function
2. ✅ Request Bedrock access
3. ✅ Test each service independently
4. ✅ Test complete voice pipeline
5. 🔄 Update frontend to call real API
6. 🔄 Test end-to-end voice flow
7. 🔄 Monitor costs in AWS Cost Explorer

---

## 💡 Quick Win: Test Polly Now!

You can test Polly RIGHT NOW without any deployment:

1. Open: https://ap-south-1.console.aws.amazon.com/polly/
2. Click "Try Polly"
3. Select: Neural engine, Hindi voice (Aditi)
4. Enter: `नमस्ते, मैं आपकी मदद के लिए यहां हूं`
5. Click "Listen"

**You'll hear real AI voice in Hindi!** 🎉

---

**Choose Option 1 (AWS Console) for easiest deployment!**
