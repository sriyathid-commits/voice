# Voice Services Setup - Transcribe & Polly

## 🎤 AWS Services for Voice

For Voice for Bharat, we'll use:
1. **Amazon Transcribe** - Speech-to-Text (STT)
2. **Amazon Polly** - Text-to-Speech (TTS)
3. **Amazon Bedrock Claude** - Natural Language Understanding

---

## 🚀 Option 1: Amazon Transcribe (Speech-to-Text)

### ✅ Advantages:
- **No access request needed** - Available immediately
- **Supports Indian languages**: Hindi, Tamil, Telugu, Marathi
- **Real-time streaming** - WebSocket support
- **Better accuracy** than Bedrock Titan for Indian accents

### 📍 Supported Languages:
- English (en-IN) ✅
- Hindi (hi-IN) ✅
- Tamil (ta-IN) ✅
- Telugu (te-IN) ✅
- Marathi (mr-IN) ✅
- Kannada (kn-IN) ⚠️ (Limited support)

### 💰 Pricing:
- **Standard**: $0.024 per minute ($1.44 per hour)
- **Streaming**: $0.025 per minute ($1.50 per hour)
- **Free tier**: 60 minutes/month for 12 months

### 🔗 Console Access:
```
https://ap-south-1.console.aws.amazon.com/transcribe/home?region=ap-south-1
```

### ✅ No Setup Required!
Transcribe is available immediately in ap-south-1. No access request needed!

---

## 🔊 Option 2: Amazon Polly (Text-to-Speech)

### ✅ Advantages:
- **No access request needed** - Available immediately
- **Neural voices** - Natural sounding
- **Supports Indian languages**: Hindi, Tamil, Telugu
- **SSML support** - Control pronunciation, speed, pitch

### 📍 Supported Voices:

#### Hindi (hi-IN):
- **Aditi** (Female, Neural) ✅
- **Kajal** (Female, Neural) ✅

#### Tamil (ta-IN):
- **Kajal** (Female, Neural) ✅

#### Telugu (te-IN):
- **Kajal** (Female, Neural) ✅

#### English (en-IN):
- **Aditi** (Female, Neural) ✅
- **Raveena** (Female, Standard) ✅

### 💰 Pricing:
- **Standard voices**: $4 per 1M characters
- **Neural voices**: $16 per 1M characters
- **Free tier**: 5M characters/month for 12 months

### 🔗 Console Access:
```
https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1
```

### ✅ No Setup Required!
Polly is available immediately in ap-south-1. No access request needed!

---

## 🎯 Recommended Architecture

### Voice Flow:
```
User speaks (Hindi/English/etc.)
    ↓
Amazon Transcribe (STT)
    ↓
Text: "मुझे राशन कार्ड चाहिए"
    ↓
Amazon Bedrock Claude (NLU)
    ↓
Response: "आपके लिए 3 योजनाएं उपलब्ध हैं..."
    ↓
Amazon Polly (TTS)
    ↓
Audio response in Hindi
```

---

## 💻 Implementation Code

### 1. Transcribe Audio (STT)

```python
import boto3
import json

transcribe = boto3.client('transcribe', region_name='ap-south-1')

# Start transcription job
response = transcribe.start_transcription_job(
    TranscriptionJobName='voice-query-123',
    LanguageCode='hi-IN',  # Hindi
    MediaFormat='wav',
    Media={
        'MediaFileUri': 's3://voice-for-bharat-audio/user-audio.wav'
    },
    OutputBucketName='voice-for-bharat-audio'
)

# Get transcription result
job_name = response['TranscriptionJob']['TranscriptionJobName']
result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
transcript_uri = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
```

### 2. Synthesize Speech (TTS)

```python
import boto3

polly = boto3.client('polly', region_name='ap-south-1')

# Synthesize speech
response = polly.synthesize_speech(
    Text='आपके लिए 3 योजनाएं उपलब्ध हैं',
    OutputFormat='mp3',
    VoiceId='Aditi',  # Hindi female voice
    Engine='neural',  # Use neural engine for better quality
    LanguageCode='hi-IN'
)

# Save audio
with open('response.mp3', 'wb') as file:
    file.write(response['AudioStream'].read())
```

### 3. Process with Claude (NLU)

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Process with Claude
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": "User query: मुझे राशन कार्ड चाहिए. Extract intent and entities."
            }
        ]
    })
)

result = json.loads(response['body'].read())
ai_response = result['content'][0]['text']
```

---

## 🔐 IAM Permissions Required

### Add to Lambda Execution Roles:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:ListTranscriptionJobs"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "polly:SynthesizeSpeech",
        "polly:DescribeVoices"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:ap-south-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    }
  ]
}
```

---

## 🧪 Test Commands

### Test Transcribe:
```bash
# Create test audio file (or use existing)
# Upload to S3
python -m awscli s3 cp test-audio.wav s3://voice-for-bharat-audio/test-audio.wav --region ap-south-1

# Start transcription
python -m awscli transcribe start-transcription-job ^
  --transcription-job-name test-job-1 ^
  --language-code hi-IN ^
  --media-format wav ^
  --media MediaFileUri=s3://voice-for-bharat-audio/test-audio.wav ^
  --output-bucket-name voice-for-bharat-audio ^
  --region ap-south-1

# Check status
python -m awscli transcribe get-transcription-job ^
  --transcription-job-name test-job-1 ^
  --region ap-south-1
```

### Test Polly:
```bash
# Synthesize speech
python -m awscli polly synthesize-speech ^
  --text "नमस्ते, आपका स्वागत है" ^
  --output-format mp3 ^
  --voice-id Aditi ^
  --engine neural ^
  --language-code hi-IN ^
  --region ap-south-1 ^
  output.mp3

# Play the audio
start output.mp3
```

---

## 📊 Language Support Matrix

| Language | Transcribe | Polly | Bedrock Claude |
|----------|-----------|-------|----------------|
| English (en-IN) | ✅ | ✅ Aditi, Raveena | ✅ |
| Hindi (hi-IN) | ✅ | ✅ Aditi, Kajal | ✅ |
| Tamil (ta-IN) | ✅ | ✅ Kajal | ✅ |
| Telugu (te-IN) | ✅ | ✅ Kajal | ✅ |
| Marathi (mr-IN) | ✅ | ❌ | ✅ |
| Kannada (kn-IN) | ⚠️ Limited | ❌ | ✅ |

### Workaround for Marathi & Kannada:
- Use Transcribe for STT (works)
- Use Claude to translate to Hindi
- Use Polly Hindi voice for TTS
- Or use English voice as fallback

---

## 🎯 Updated Voice Service Implementation

I'll update the voice service to use:
1. **Amazon Transcribe** for STT (instead of Bedrock Titan)
2. **Amazon Polly** for TTS (instead of Bedrock Titan)
3. **Amazon Bedrock Claude** for NLU (understanding)

### Benefits:
- ✅ No waiting for Bedrock Titan access
- ✅ Better Indian language support
- ✅ More cost-effective
- ✅ Real-time streaming support
- ✅ Higher quality voices

---

## 💰 Cost Comparison

### For 1000 voice interactions/day:

**Option 1: Bedrock Titan (if available)**
- STT: ~$30/month
- TTS: ~$50/month
- Total: ~$80/month

**Option 2: Transcribe + Polly (Recommended)**
- Transcribe: ~$36/month (1000 × 1 min × $0.024 × 30 days)
- Polly Neural: ~$16/month (1000 × 500 chars × $16/1M × 30 days)
- Total: ~$52/month

**Savings: $28/month (35% cheaper!)**

---

## 🚀 Quick Start

### 1. Test Polly Now (No Setup!)
```bash
# Test Hindi voice
python -m awscli polly synthesize-speech ^
  --text "आपके लिए तीन योजनाएं उपलब्ध हैं" ^
  --output-format mp3 ^
  --voice-id Aditi ^
  --engine neural ^
  --language-code hi-IN ^
  --region ap-south-1 ^
  hindi-test.mp3

start hindi-test.mp3
```

### 2. Test Transcribe (Needs audio file)
```bash
# Upload test audio
python -m awscli s3 cp your-audio.wav s3://voice-for-bharat-audio/ --region ap-south-1

# Start transcription
python -m awscli transcribe start-transcription-job ^
  --transcription-job-name test-$(date +%s) ^
  --language-code hi-IN ^
  --media-format wav ^
  --media MediaFileUri=s3://voice-for-bharat-audio/your-audio.wav ^
  --region ap-south-1
```

---

## ✅ Action Items

1. **Immediate** (No approval needed):
   - [ ] Test Polly voices
   - [ ] Test Transcribe with sample audio
   - [ ] Update Lambda IAM roles

2. **Waiting for approval**:
   - [ ] Bedrock Claude access (for NLU)

3. **Code updates**:
   - [ ] Update voice_service to use Transcribe
   - [ ] Update voice_service to use Polly
   - [ ] Keep Claude integration for NLU

---

## 🎓 Documentation

- **Transcribe**: https://docs.aws.amazon.com/transcribe/
- **Polly**: https://docs.aws.amazon.com/polly/
- **Supported languages**: https://docs.aws.amazon.com/polly/latest/dg/SupportedLanguage.html

---

**Ready to implement! These services are available NOW in ap-south-1!** 🚀
