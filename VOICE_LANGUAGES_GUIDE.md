# 🗣️ Voice for Bharat - Supported Languages

## 🇮🇳 6 Indian Languages Supported

Voice for Bharat supports multilingual voice interaction in 6 major Indian languages, covering over 1 billion speakers across India.

---

## 📊 Language Support Matrix

| # | Language | Code | Speakers | Transcribe (STT) | Polly Voice (TTS) | Claude (NLU) | Status |
|---|----------|------|----------|------------------|-------------------|--------------|--------|
| 1 | **English** | `en` | 125M+ | ✅ en-IN | ✅ Aditi (Neural) | ✅ | Full Support |
| 2 | **Hindi** | `hi` | 600M+ | ✅ hi-IN | ✅ Aditi (Neural) | ✅ | Full Support |
| 3 | **Tamil** | `ta` | 80M+ | ✅ ta-IN | ✅ Kajal (Neural) | ✅ | Full Support |
| 4 | **Telugu** | `te` | 95M+ | ✅ te-IN | ✅ Kajal (Neural) | ✅ | Full Support |
| 5 | **Marathi** | `mr` | 95M+ | ✅ mr-IN | ⚠️ Hindi fallback | ✅ | Partial Support |
| 6 | **Kannada** | `kn` | 50M+ | ⚠️ Limited | ⚠️ Hindi fallback | ✅ | Partial Support |

**Total Coverage**: ~1.045 billion speakers across India

---

## 🎤 Language Details

### 1. English (en) - Full Support ✅

**Speakers**: 125 million (India)
**Regions**: Pan-India, Urban areas, Education

**Voice Services**:
- **Transcribe**: `en-IN` (English, Indian)
- **Polly Voice**: Aditi (Female, Neural)
- **Alternative Voice**: Raveena (Female, Standard)
- **Claude**: Full support

**Sample Text**:
```
Hello, I am here to help you find government welfare schemes.
```

**Test in Polly**:
- Language: English, Indian (en-IN)
- Voice: Aditi
- Engine: Neural

---

### 2. Hindi (hi) - Full Support ✅

**Speakers**: 600 million (Native + Second language)
**Regions**: North India, Central India, Official language

**Voice Services**:
- **Transcribe**: `hi-IN` (Hindi, Indian)
- **Polly Voice**: Aditi (Female, Neural)
- **Alternative Voice**: Kajal (Female, Neural)
- **Claude**: Full support

**Sample Text**:
```
नमस्ते, मैं आपकी मदद के लिए यहां हूं। सरकारी योजनाओं के बारे में जानकारी प्राप्त करें।
```
(Namaste, I am here to help you. Get information about government schemes.)

**Test in Polly**:
- Language: Hindi, Indian (hi-IN)
- Voice: Aditi
- Engine: Neural

---

### 3. Tamil (ta) - Full Support ✅

**Speakers**: 80 million
**Regions**: Tamil Nadu, Puducherry, Sri Lanka

**Voice Services**:
- **Transcribe**: `ta-IN` (Tamil, Indian)
- **Polly Voice**: Kajal (Female, Neural)
- **Claude**: Full support

**Sample Text**:
```
வணக்கம், நான் உங்களுக்கு உதவ இங்கே இருக்கிறேன். அரசாங்க திட்டங்கள் பற்றி தகவல் பெறுங்கள்.
```
(Vanakkam, I am here to help you. Get information about government schemes.)

**Test in Polly**:
- Language: Tamil, Indian (ta-IN)
- Voice: Kajal
- Engine: Neural

---

### 4. Telugu (te) - Full Support ✅

**Speakers**: 95 million
**Regions**: Andhra Pradesh, Telangana

**Voice Services**:
- **Transcribe**: `te-IN` (Telugu, Indian)
- **Polly Voice**: Kajal (Female, Neural)
- **Claude**: Full support

**Sample Text**:
```
నమస్కారం, నేను మీకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను। ప్రభుత్వ పథకాల గురించి సమాచారం పొందండి.
```
(Namaskaram, I am here to help you. Get information about government schemes.)

**Test in Polly**:
- Language: Telugu, Indian (te-IN)
- Voice: Kajal
- Engine: Neural

---

### 5. Marathi (mr) - Partial Support ⚠️

**Speakers**: 95 million
**Regions**: Maharashtra, Goa

**Voice Services**:
- **Transcribe**: ✅ `mr-IN` (Marathi, Indian)
- **Polly Voice**: ⚠️ No native voice (uses Hindi Aditi as fallback)
- **Claude**: ✅ Full support

**Sample Text**:
```
नमस्कार, मी तुम्हाला मदत करण्यासाठी येथे आहे। सरकारी योजनांबद्दल माहिती मिळवा.
```
(Namaskar, I am here to help you. Get information about government schemes.)

**Workaround**:
- Transcribe: Works perfectly for Marathi speech
- Claude: Understands and responds in Marathi
- TTS: Uses Hindi voice (Aditi) - still understandable for Marathi speakers

---

### 6. Kannada (kn) - Partial Support ⚠️

**Speakers**: 50 million
**Regions**: Karnataka

**Voice Services**:
- **Transcribe**: ⚠️ Limited support `kn-IN`
- **Polly Voice**: ⚠️ No native voice (uses Hindi Aditi as fallback)
- **Claude**: ✅ Full support

**Sample Text**:
```
ನಮಸ್ಕಾರ, ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ. ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ಪಡೆಯಿರಿ.
```
(Namaskara, I am here to help you. Get information about government schemes.)

**Workaround**:
- Transcribe: Limited accuracy, may need manual testing
- Claude: Understands and responds in Kannada
- TTS: Uses Hindi voice (Aditi) - may not be ideal

---

## 🧪 Test All Languages

### Test in Polly Console

**Open**: https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1

#### 1. English
- Language: **English, Indian (en-IN)**
- Voice: **Aditi**
- Engine: **Neural**
- Text: `Hello, welcome to Voice for Bharat`

#### 2. Hindi
- Language: **Hindi, Indian (hi-IN)**
- Voice: **Aditi**
- Engine: **Neural**
- Text: `नमस्ते, वॉइस फॉर भारत में आपका स्वागत है`

#### 3. Tamil
- Language: **Tamil, Indian (ta-IN)**
- Voice: **Kajal**
- Engine: **Neural**
- Text: `வணக்கம், வாய்ஸ் ஃபார் பாரத்திற்கு வரவேற்கிறோம்`

#### 4. Telugu
- Language: **Telugu, Indian (te-IN)**
- Voice: **Kajal**
- Engine: **Neural**
- Text: `నమస్కారం, వాయిస్ ఫర్ భారత్‌కు స్వాగతం`

#### 5. Marathi (using Hindi voice)
- Language: **Hindi, Indian (hi-IN)**
- Voice: **Aditi**
- Engine: **Neural**
- Text: `नमस्कार, व्हॉइस फॉर भारत मध्ये आपले स्वागत आहे`

#### 6. Kannada (using Hindi voice)
- Language: **Hindi, Indian (hi-IN)**
- Voice: **Aditi**
- Engine: **Neural**
- Text: `ನಮಸ್ಕಾರ, ವಾಯ್ಸ್ ಫಾರ್ ಭಾರತ್‌ಗೆ ಸ್ವಾಗತ`

---

## 🎯 Language Implementation in Code

### Backend (service.py)

```python
# Language mappings for Transcribe
self.language_codes = {
    "en": "en-IN",  # English, Indian
    "hi": "hi-IN",  # Hindi, Indian
    "ta": "ta-IN",  # Tamil, Indian
    "te": "te-IN",  # Telugu, Indian
    "mr": "mr-IN",  # Marathi, Indian
    "kn": "kn-IN"   # Kannada, Indian
}

# Polly voice mappings
self.polly_voices = {
    "en": {"VoiceId": "Aditi", "Engine": "neural"},
    "hi": {"VoiceId": "Aditi", "Engine": "neural"},
    "ta": {"VoiceId": "Kajal", "Engine": "neural"},
    "te": {"VoiceId": "Kajal", "Engine": "neural"},
    "mr": {"VoiceId": "Aditi", "Engine": "neural"},  # Fallback
    "kn": {"VoiceId": "Aditi", "Engine": "neural"}   # Fallback
}
```

### Frontend (Assistant Page)

Users can select their preferred language from a dropdown:
- English
- हिंदी (Hindi)
- தமிழ் (Tamil)
- తెలుగు (Telugu)
- मराठी (Marathi)
- ಕನ್ನಡ (Kannada)

---

## 📊 Coverage Statistics

### By Region

| Region | Primary Languages | Coverage |
|--------|------------------|----------|
| North India | Hindi, English | ✅ Full |
| South India | Tamil, Telugu, Kannada | ✅ Full (Tamil, Telugu), ⚠️ Partial (Kannada) |
| West India | Marathi, Hindi, English | ⚠️ Partial (Marathi), ✅ Full (Hindi, English) |
| East India | Hindi, English | ✅ Full |
| Northeast | English, Hindi | ✅ Full |

### By Population

- **Full Support**: ~900M speakers (English, Hindi, Tamil, Telugu)
- **Partial Support**: ~145M speakers (Marathi, Kannada)
- **Total Coverage**: ~1.045 billion speakers

---

## 🔧 How to Add More Languages

### Step 1: Check AWS Support
1. Transcribe: https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html
2. Polly: https://docs.aws.amazon.com/polly/latest/dg/SupportedLanguage.html

### Step 2: Update Backend Code

Add to `backend/lambdas/voice_service/service.py`:

```python
# Add language code
self.language_codes["bn"] = "bn-IN"  # Bengali

# Add Polly voice
self.polly_voices["bn"] = {"VoiceId": "Aditi", "Engine": "neural"}
```

### Step 3: Update Frontend

Add language option in `frontend/web/src/app/(dashboard)/assistant/page.tsx`

---

## 💡 Best Practices

### For Full Support Languages (en, hi, ta, te):
- Use native voices for best user experience
- Transcription accuracy is high
- Claude understands context well

### For Partial Support Languages (mr, kn):
- Inform users about voice fallback
- Transcription may need verification
- Consider adding manual text input option

### General:
- Always provide language selection UI
- Cache TTS responses to reduce costs
- Monitor transcription accuracy per language
- Collect user feedback for improvements

---

## 🎉 Summary

Voice for Bharat supports **6 major Indian languages**:

✅ **Full Support** (4 languages):
1. English - Aditi voice
2. Hindi - Aditi voice
3. Tamil - Kajal voice
4. Telugu - Kajal voice

⚠️ **Partial Support** (2 languages):
5. Marathi - Hindi voice fallback
6. Kannada - Hindi voice fallback

**Total Coverage**: Over 1 billion speakers across India! 🇮🇳

---

## 🔗 Quick Links

- **Test Polly**: https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1
- **Test Transcribe**: https://ap-south-1.console.aws.amazon.com/transcribe/home?region=ap-south-1
- **Language Docs**: https://docs.aws.amazon.com/polly/latest/dg/SupportedLanguage.html

---

**Voice for Bharat - Democratizing access to government welfare in every Indian language!** 🗣️🇮🇳
