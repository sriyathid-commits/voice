# Real AI Voice Services Deployment

## 🎯 What We're Deploying

Updating the Voice for Bharat backend to use **REAL AWS AI services**:

1. ✅ **Amazon Transcribe** - Speech-to-Text (6 Indian languages)
2. ✅ **Amazon Bedrock Claude** - Natural Language Understanding
3. ✅ **Amazon Polly** - Text-to-Speech (Neural voices)

## 📋 Current Status

### Infrastructure (Already Deployed)
- ✅ CloudFormation Stack: `voicebharatai` in ap-south-1
- ✅ 7 Lambda Functions deployed
- ✅ 8 DynamoDB Tables created
- ✅ 3 S3 Buckets configured
- ✅ API Gateway (REST + WebSocket)
- ✅ Cognito User Pool
- ✅ ElastiCache Redis
- ✅ CloudFront CDN

### What's Updated
- ✅ IAM Permissions: Added Transcribe + Polly access
- ✅ VoiceService Code: Complete rewrite with real AI
- ⏳ Deployment: Need to update stack

## 🚀 Deployment Steps

### Step 1: Build Lambda Package
```bash
cd backend
sam build --use-container
```

### Step 2: Deploy Updated Stack
```bash
sam deploy --stack-name voicebharatai --region ap-south-1 --capabilities CAPABILITY_NAMED_IAM --parameter-overrides Environment=dev WhatsAppApiKey=placeholder
```

### Step 3: Request Bedrock Access
1. Go to AWS Console → Bedrock
2. Request access to Claude 3 Sonnet
3. Wait for approval (usually instant for Claude)

### Step 4: Test Voice Services

#### Test Transcribe (STT)
```bash
# Upload test audio
aws s3 cp test-audio.wav s3://voice-for-bharat-audio-dev-[ACCOUNT_ID]/ --region ap-south-1

# Start transcription
aws transcribe start-transcription-job \
  --transcription-job-name test-job-1 \
  --language-code hi-IN \
  --media-format wav \
  --media MediaFileUri=s3://voice-for-bharat-audio-dev-[ACCOUNT_ID]/test-audio.wav \
  --region ap-south-1
```

#### Test Polly (TTS)
```bash
# Synthesize Hindi speech
aws polly synthesize-speech \
  --text "नमस्ते, आपका स्वागत है" \
  --output-format mp3 \
  --voice-id Aditi \
  --engine neural \
  --language-code hi-IN \
  --region ap-south-1 \
  output.mp3
```

#### Test Claude (NLU)
```bash
# Test via Lambda function
aws lambda invoke \
  --function-name voice-for-bharat-voice-service-dev \
  --region ap-south-1 \
  --payload '{"body": "{\"text\": \"मुझे राशन कार्ड चाहिए\"}"}' \
  response.json
```

## 🔧 Updated Components

### 1. CloudFormation Template (`backend/template.yaml`)
**Added IAM Policies:**
- TranscribeAccess: Start/Get/Delete transcription jobs
- PollyAccess: Synthesize speech, describe voices
- BedrockAccess: Invoke Claude models (already existed)

### 2. Voice Service (`backend/lambdas/voice_service/service.py`)
**Complete Rewrite:**
- Real Amazon Transcribe integration (STT)
- Real Amazon Bedrock Claude integration (NLU)
- Real Amazon Polly integration (TTS)
- Multi-language support (6 Indian languages)
- TTS caching in S3
- Error handling and fallbacks

**Key Methods:**
- `process_voice_query()` - Main pipeline
- `transcribe_audio()` - STT with Transcribe
- `process_with_claude()` - NLU with Bedrock
- `synthesize_speech()` - TTS with Polly

### 3. Voice Handler (`backend/lambdas/voice_service/handler.py`)
**Endpoints:**
- `POST /voice/query` - Process voice query (REST)
- `GET /voice/session/{id}` - Get conversation session
- `WebSocket /ws/voice` - Real-time voice streaming

## 📊 Language Support

| Language | Code | Transcribe | Polly Voice | Claude |
|----------|------|-----------|-------------|--------|
| English | en | ✅ en-IN | ✅ Aditi (Neural) | ✅ |
| Hindi | hi | ✅ hi-IN | ✅ Aditi (Neural) | ✅ |
| Tamil | ta | ✅ ta-IN | ✅ Kajal (Neural) | ✅ |
| Telugu | te | ✅ te-IN | ✅ Kajal (Neural) | ✅ |
| Marathi | mr | ✅ mr-IN | ⚠️ Fallback to Hindi | ✅ |
| Kannada | kn | ⚠️ Limited | ⚠️ Fallback to Hindi | ✅ |

## 💰 Cost Estimate

### For 1000 voice interactions/day (30 days):

**Amazon Transcribe:**
- 1000 queries × 1 min × $0.024 × 30 days = $720/month
- With free tier: $720 - $1.44 = $718.56/month

**Amazon Polly (Neural):**
- 1000 queries × 500 chars × $16/1M × 30 days = $240/month
- With free tier: $240 - $80 = $160/month

**Amazon Bedrock Claude:**
- Input: 1000 × 100 tokens × $0.003/1K × 30 = $9/month
- Output: 1000 × 200 tokens × $0.015/1K × 30 = $90/month
- Total: $99/month

**Total Voice AI Cost: ~$977/month**

### Cost Optimization:
- Cache TTS responses (reduces Polly cost by 70%)
- Use batch transcription for non-real-time queries
- Implement conversation context to reduce Claude tokens

**Optimized Cost: ~$400/month**

## 🎯 Testing Checklist

After deployment:

- [ ] Test Transcribe with Hindi audio
- [ ] Test Transcribe with English audio
- [ ] Test Polly Hindi voice (Aditi)
- [ ] Test Polly English voice (Aditi)
- [ ] Request Bedrock Claude access
- [ ] Test Claude with Hindi query
- [ ] Test Claude with English query
- [ ] Test complete voice pipeline (STT → NLU → TTS)
- [ ] Test TTS caching
- [ ] Test error handling
- [ ] Test multi-language support
- [ ] Update frontend to call real API

## 🔗 Useful Links

**AWS Console:**
- Transcribe: https://ap-south-1.console.aws.amazon.com/transcribe/
- Polly: https://ap-south-1.console.aws.amazon.com/polly/
- Bedrock: https://ap-south-1.console.aws.amazon.com/bedrock/
- Lambda: https://ap-south-1.console.aws.amazon.com/lambda/
- CloudFormation: https://ap-south-1.console.aws.amazon.com/cloudformation/

**Documentation:**
- Transcribe: https://docs.aws.amazon.com/transcribe/
- Polly: https://docs.aws.amazon.com/polly/
- Bedrock: https://docs.aws.amazon.com/bedrock/

## ⚠️ Important Notes

1. **Bedrock Access Required:**
   - Claude 3 Sonnet needs access request
   - Usually approved instantly
   - Go to Bedrock Console → Model Access → Request

2. **Transcribe & Polly:**
   - Available immediately, no access request needed
   - Work out of the box in ap-south-1

3. **Cost Management:**
   - Monitor usage in AWS Cost Explorer
   - Set up billing alerts
   - Use TTS caching to reduce costs

4. **Testing:**
   - Test each service independently first
   - Then test complete pipeline
   - Use small audio files for testing

## 🎉 Expected Results

After deployment:
- Real voice transcription in 6 Indian languages
- AI-powered understanding with Claude
- Natural-sounding voice responses
- Complete voice interaction pipeline
- Production-ready voice assistant

## 📞 Support

If you encounter issues:
1. Check CloudWatch Logs for Lambda errors
2. Verify IAM permissions
3. Confirm Bedrock model access
4. Test each service independently
5. Check S3 bucket permissions

---

**Ready to deploy real AI voice services!** 🚀
