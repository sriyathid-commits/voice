# 🚀 Deploy Voice AI - Quick Start

## ✅ Deployment Package Ready!

File: `voice_service.zip` (8 KB)
Location: `C:\Users\yathi\voice\voice_service.zip`

---

## 📋 3 Simple Steps to Deploy

### Step 1: Upload to Lambda (5 minutes)

1. **Open Lambda Console**: https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev

2. **Upload the zip file**:
   - Click "Upload from" button (orange)
   - Select ".zip file"
   - Choose: `C:\Users\yathi\voice\voice_service.zip`
   - Click "Save"
   - Wait for success message

3. **Verify**:
   - Open `service.py` in the code editor
   - Look for these methods:
     - `transcribe_audio()`
     - `process_with_claude()`
     - `synthesize_speech()`
   - If you see them, deployment successful! ✅

---

### Step 2: Request Bedrock Access (2 minutes)

1. **Open Bedrock Console**: https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess

2. **Request Claude access**:
   - Click "Manage model access" (orange button)
   - Find "Anthropic" section
   - Check: ✅ Claude 3 Sonnet
   - Click "Request model access"
   - Wait for approval (usually instant)

3. **Verify**:
   - Refresh the page
   - Claude 3 Sonnet should show "Access granted" ✅

---

### Step 3: Test Voice Services (3 minutes)

#### Test Polly (Hindi Voice)

1. **Open Polly Console**: https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1#/home

2. **Try Hindi voice**:
   - Click "Try Polly"
   - Engine: **Neural**
   - Language: **Hindi, Indian (hi-IN)**
   - Voice: **Aditi**
   - Text: `नमस्ते, मैं आपकी मदद के लिए यहां हूं`
   - Click "Listen"
   - **You should hear Hindi speech!** 🎉

3. **Try English voice**:
   - Language: **English, Indian (en-IN)**
   - Voice: **Aditi**
   - Text: `Hello, I am here to help you`
   - Click "Listen"

---

## 🎯 What You'll Have After This

✅ **Real Speech-to-Text** - Amazon Transcribe (6 Indian languages)
✅ **Real AI Understanding** - Amazon Bedrock Claude
✅ **Real Text-to-Speech** - Amazon Polly (Neural voices)
✅ **Complete Voice Pipeline** - End-to-end voice interaction

---

## 🔗 Quick Access Links

**Deploy:**
- Lambda Function: https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev

**Setup:**
- Bedrock Access: https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess

**Test:**
- Polly (TTS): https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1
- Transcribe (STT): https://ap-south-1.console.aws.amazon.com/transcribe/home?region=ap-south-1
- CloudWatch Logs: https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fvoice-for-bharat-voice-service-dev

---

## 💡 Pro Tips

1. **Test Polly first** - It works immediately, no setup needed
2. **Bedrock approval** - Usually instant, but can take up to 24 hours
3. **Check logs** - If something doesn't work, check CloudWatch logs
4. **Cost monitoring** - Set up billing alerts in AWS Cost Explorer

---

## 📊 Expected Costs

For testing (100 queries):
- Transcribe: ~$2.40
- Polly: ~$0.80
- Bedrock: ~$0.30
- **Total: ~$3.50**

For production (1000 queries/day):
- ~$35/day (~$1,050/month)
- With caching: ~$13/day (~$400/month)

---

## 🎉 Ready to Deploy!

1. Click the Lambda link above
2. Upload `voice_service.zip`
3. Request Bedrock access
4. Test Polly voice

**Total time: ~10 minutes**

---

## 📞 Need Help?

- Check: `MANUAL_LAMBDA_DEPLOY.md` for detailed instructions
- Check: `REAL_AI_DEPLOYMENT.md` for technical details
- Check: `VOICE_SERVICES_SETUP.md` for service information

---

**Let's deploy real AI voice services!** 🚀
