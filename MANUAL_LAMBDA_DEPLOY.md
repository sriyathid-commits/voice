# Manual Lambda Deployment - AWS Console

## 🎯 Goal
Deploy the updated Voice Service Lambda with real AI (Transcribe, Claude, Polly)

## ✅ What You Need
- AWS Console access
- The voice service files (already on your computer)

---

## 📦 Step 1: Create Deployment Package

### Option A: Using File Explorer (Easiest)

1. Open File Explorer
2. Navigate to: `C:\Users\yathi\voice\backend\lambdas\voice_service`
3. You should see these files:
   - `handler.py`
   - `service.py`
   - `models.py`
   - `requirements.txt`
   - `__init__.py`

4. **Select these 5 files** (NOT the folder, just the files)
5. Right-click → "Send to" → "Compressed (zipped) folder"
6. Name it: `voice_service.zip`
7. Move the zip file to your Desktop for easy access

### Option B: Using PowerShell

```powershell
# Navigate to voice service directory
cd C:\Users\yathi\voice\backend\lambdas\voice_service

# Create zip file (select only Python files)
Compress-Archive -Path handler.py,service.py,models.py,requirements.txt,__init__.py -DestinationPath C:\Users\yathi\Desktop\voice_service.zip -Force
```

---

## 🚀 Step 2: Deploy to AWS Lambda

### 2.1 Open Lambda Console
1. Open your browser
2. Go to: https://ap-south-1.console.aws.amazon.com/lambda/
3. Sign in to your AWS account

### 2.2 Find Your Function
1. In the search box, type: `voice-for-bharat-voice-service-dev`
2. Click on the function name

### 2.3 Upload New Code
1. Scroll down to the "Code" section
2. Click the **"Upload from"** button (orange button)
3. Select **".zip file"**
4. Click **"Upload"**
5. Browse and select: `voice_service.zip` (from your Desktop)
6. Click **"Save"**
7. Wait for the upload to complete (you'll see a success message)

### 2.4 Verify Upload
1. In the code editor, you should now see:
   - `handler.py`
   - `service.py`
   - `models.py`
   - `__init__.py`
2. Open `service.py` and verify you see methods like:
   - `transcribe_audio()`
   - `process_with_claude()`
   - `synthesize_speech()`

✅ **Lambda function updated!**

---

## 🔐 Step 3: Request Bedrock Access

### 3.1 Open Bedrock Console
1. Go to: https://ap-south-1.console.aws.amazon.com/bedrock/
2. Click **"Model access"** in the left sidebar

### 3.2 Request Claude Access
1. Click **"Manage model access"** (orange button at top right)
2. Scroll down to find **"Anthropic"** section
3. Check the box: ✅ **Claude 3 Sonnet**
4. Scroll to bottom
5. Click **"Request model access"**
6. Wait for approval (usually instant - refresh the page)

### 3.3 Verify Access
1. Go back to "Model access" page
2. Find "Claude 3 Sonnet"
3. Status should show: **"Access granted"** ✅

---

## 🧪 Step 4: Test Voice Services

### Test 1: Test Polly (Text-to-Speech) - Works Immediately!

1. Open: https://ap-south-1.console.aws.amazon.com/polly/
2. Click **"Try Polly"** button
3. Configure:
   - **Engine**: Neural
   - **Language**: Hindi, Indian (hi-IN)
   - **Voice**: Aditi (Female)
4. Enter text: `नमस्ते, मैं आपकी मदद के लिए यहां हूं`
5. Click **"Listen"** button
6. **You should hear Hindi speech!** 🎉

Try other languages:
- **English**: Select "English, Indian (en-IN)", Voice: Aditi
- **Tamil**: Select "Tamil, Indian (ta-IN)", Voice: Kajal
- **Telugu**: Select "Telugu, Indian (te-IN)", Voice: Kajal

### Test 2: Test Transcribe (Speech-to-Text)

1. Open: https://ap-south-1.console.aws.amazon.com/transcribe/
2. Click **"Create job"**
3. Configure:
   - **Job name**: `test-job-1`
   - **Language**: Hindi, Indian (hi-IN)
   - **Input file location**: Upload a Hindi audio file (WAV or MP3)
4. Click **"Create job"**
5. Wait for status to change to "Complete"
6. Click on job name to view transcript

### Test 3: Check Lambda Logs

1. Open: https://ap-south-1.console.aws.amazon.com/cloudwatch/
2. Click **"Log groups"** in left sidebar
3. Find: `/aws/lambda/voice-for-bharat-voice-service-dev`
4. Click on the log group
5. Click on the most recent log stream
6. Check for any errors

---

## ✅ Verification Checklist

After completing all steps:

- [ ] Lambda function shows updated code with `service.py` containing real AI methods
- [ ] Bedrock shows "Access granted" for Claude 3 Sonnet
- [ ] Polly test produces Hindi audio successfully
- [ ] No errors in CloudWatch logs
- [ ] Lambda "Last modified" timestamp is recent

---

## 🎯 What's Now Working

After this deployment:

1. ✅ **Amazon Transcribe** - Converts speech to text in 6 Indian languages
2. ✅ **Amazon Bedrock Claude** - Understands user intent and generates responses
3. ✅ **Amazon Polly** - Converts text responses to natural speech
4. ✅ **Complete Voice Pipeline** - STT → AI Understanding → TTS

---

## 🔧 Troubleshooting

### Issue: Upload fails
**Solution**: Make sure you're uploading a .zip file, not a folder

### Issue: Bedrock access denied
**Solution**: 
1. Go to Bedrock console
2. Click "Model access"
3. Request access for Claude 3 Sonnet
4. Wait for approval (usually instant)

### Issue: Can't find Lambda function
**Solution**: 
1. Check you're in the correct region: **ap-south-1** (Mumbai)
2. Look at the top right of AWS console - should say "Asia Pacific (Mumbai)"

### Issue: Polly test doesn't work
**Solution**: 
1. Make sure you selected "Neural" engine
2. Select a voice that supports the language (Aditi for Hindi/English, Kajal for Tamil/Telugu)

---

## 📊 Cost Information

For 1000 voice queries per day:

- **Transcribe**: ~$24/day ($720/month)
- **Polly**: ~$8/day ($240/month)
- **Bedrock Claude**: ~$3/day ($90/month)

**Total**: ~$35/day or ~$1,050/month

**With optimizations** (caching, batching): ~$400/month

**Free tier** (first 12 months):
- Transcribe: 60 minutes/month free
- Polly: 5M characters/month free
- Bedrock: Pay as you go (no free tier)

---

## 🎉 Success!

Once you complete these steps:

1. Your Lambda function has REAL AI voice services
2. You can test Polly and hear actual Hindi/English speech
3. Transcribe can convert speech to text
4. Claude can understand and respond to queries
5. Complete voice pipeline is ready!

---

## 📞 Next Steps

1. ✅ Deploy Lambda (this guide)
2. ✅ Request Bedrock access
3. ✅ Test Polly voice
4. 🔄 Update frontend to call real API
5. 🔄 Test end-to-end voice flow
6. 🔄 Monitor costs in AWS Cost Explorer

---

## 🔗 Quick Links

- **Lambda Console**: https://ap-south-1.console.aws.amazon.com/lambda/
- **Bedrock Console**: https://ap-south-1.console.aws.amazon.com/bedrock/
- **Polly Console**: https://ap-south-1.console.aws.amazon.com/polly/
- **Transcribe Console**: https://ap-south-1.console.aws.amazon.com/transcribe/
- **CloudWatch Logs**: https://ap-south-1.console.aws.amazon.com/cloudwatch/

---

**Start with Step 1: Create the zip file!** 📦
