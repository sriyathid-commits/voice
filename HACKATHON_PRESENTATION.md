# Voice for Bharat 2.0
## AI for Bharat in Indian Languages

**BUILD FAST WITH AI: AI BUILD CHALLENGE 2026**

**Problem Statement:** PS6 - AI for Bharat in Indian Languages

**Live Demo:** https://bharatvisionxai.vercel.app

---

## Slide 1: The Problem We're Solving

### WHO FACES IT
**Millions of Indian citizens** with limited digital literacy seeking government welfare schemes
- Farmers with land ownership questions
- Students seeking education scholarships
- Citizens who prefer their native language over English
- People intimidated by complex government portals

### WHAT IT COSTS THEM TODAY
- **Hours wasted** navigating confusing government websites
- **Schemes missed** due to language barriers (English-only portals)
- **No guidance** on eligibility requirements or next steps
- **Confusion** about which documents are actually needed
- **Zero support** for conversational follow-up questions

### THE SPECIFIC PROBLEM
Citizens can't simply **ask in their language**: 
- "నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి" (Telugu)
- "I need farmer schemes"
- And get immediate, actionable guidance in return

---

## Slide 2: Our Solution

### IN TWO LINES
**Voice for Bharat 2.0** is a conversational AI assistant that lets citizens speak naturally in 6 Indian languages to discover schemes, check eligibility with explainable reasons, and receive step-by-step action plans with document checklists.

### WHAT THE USER DOES
1. **Selects their language** (English, Hindi, Telugu, Tamil, Marathi, Kannada)
2. **Taps microphone** and speaks naturally
3. **Asks follow-up questions** in the same conversation
4. **Gets eligibility explanation** with matched/missing criteria
5. **Receives action plan** with document checklist

### WHAT THEY GET BACK
- **Real-time transcription** of their voice query
- **Conversational AI response** that remembers context
- **Eligibility status** (Eligible / Likely Eligible / Needs Verification / Not Eligible)
- **Explainable scoring** (0-100) with matched conditions and gaps
- **Action plan** with step-by-step next steps
- **Document checklist** (available ✓ vs required ⚠)
- **Voice response** in their selected language

---

## Slide 3: Technical Approach

### MODELS
- **Amazon Transcribe**: Multilingual speech-to-text (6 Indian languages)
- **Anthropic Claude 3 Sonnet (via Amazon Bedrock)**: Conversational AI, intent detection, entity extraction
- **Amazon Polly**: Neural text-to-speech with Indian voices (Aditi, Kajal)
- **Amazon Titan Embeddings**: Scheme search and matching (ready for RAG)

### TOOLS & FRAMEWORKS
**Backend:**
- AWS Lambda (7 services: voice, scheme, user, application, document, notification, sync)
- DynamoDB (8 tables with GSI) - session context, schemes, user profiles
- Amazon API Gateway (REST + WebSocket)
- Redis (ElastiCache) - conversation session storage with 30min TTL
- S3 - audio storage with lifecycle policies

**Frontend:**
- Next.js 15 + TypeScript
- Zustand (state management for conversations and citizen profile)
- MediaRecorder API (audio capture)
- Tailwind CSS (responsive UI)

**Architecture:**
```
Voice Input → Transcribe → Claude (contextual) → Profile Builder
   ↓
DynamoDB Session ← Redis Cache → Conversation Memory (20 msgs)
   ↓
Scheme Service → Eligibility Engine → Action Plan Generator
   ↓
Polly TTS → S3 Audio → CloudFront → Voice Output
```

### DATA
- **Demo schemes** (clearly labeled): Rythu Bandhu (Telangana farmer), PM-KISAN (All India), NSP Scholarship
- **Multilingual content**: All scheme data in 6 languages
- **Production-ready schemas**: DynamoDB tables with eligibility criteria, document requirements

### HUMAN APPROVAL
None required for scheme discovery. Human verifies:
- Document uploads before submission
- Final application review before portal submission

---

## Slide 4: Key Features

### 01. Bharat Voice Mode
6 Indian languages with real-time voice interaction. Language selection controls entire experience: STT, AI reasoning, UI text, TTS output.

### 02. Conversational Citizen Profile
Progressive information gathering - only asks what's relevant. Remembers state, occupation (farmer/student), age, income, land ownership across the session. Never repeats questions.

### 03. Explainable Eligibility Agent
**NOT** just "Eligible" - shows:
- Status determination (4 levels)
- Score breakdown (age: 20pt, income: 25pt, category: 20pt, state: 20pt, gender: 15pt)
- Matched conditions: "Age 35 is within range (18-70)"
- Missing information: "Income not provided"
- Verification required: "Land records document"

### 04. Citizen Action Plan
Step-by-step guidance with:
- Document checklist (✓ available vs ⚠ required)
- Numbered action steps with status (COMPLETED/REQUIRED/OPTIONAL)
- Application method and portal URL
- Estimated completion time
- Helpful notes in user's language

### 05. Session-Based Context
30-minute sessions with 20-message history. User can ask "ఇప్పుడు నేను ఏమి చేయాలి?" (What should I do now?) and get contextual guidance based on current scheme and eligibility status.

---

## Slide 5: Baseline & Evaluation

### TODAY - WITHOUT OUR SYSTEM
- **30-60 minutes** per scheme: Navigate portal → Read eligibility (English) → Google translate → Guess documents → Call helpline
- **~40% give up** before applying due to confusion
- **Zero explainability** on why not eligible
- **No voice interface** for low-literacy users

### TARGET - WITH OUR SYSTEM
- **3-5 minutes** per scheme: Voice query → Instant eligibility → Clear action plan
- **<10% drop-off** with conversational guidance
- **100% explainability** on eligibility decisions
- **Full voice support** in native languages

### HOW WE'LL EVALUATE IT
**Test Set:**
- Telugu farmer scenario (demo-critical)
- 5 user profiles across languages
- 10 scheme-eligibility pairs

**Metrics:**
- Transcription accuracy (>90% target)
- Eligibility determination correctness (100% for demo schemes)
- Profile completeness after conversation (>80% fields filled)
- Response latency (<5s end-to-end)
- Action plan generation success rate (100%)

**Failure Detection:**
- Intent misclassification → Fallback to general guidance
- Low transcription confidence → Request repeat
- Missing profile data → Contextual follow-up questions
- API timeouts → Graceful error messages + retry

---

## Slide 6: Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (Mobile/Web)                         │
│         6 Languages: en, hi, te, ta, mr, kn                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                    Voice Input
                         │
┌────────────────────────┴────────────────────────────────────┐
│                   FRONTEND (Next.js 15)                      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ VoiceStore  │  │ SchemeStore  │  │ Voice Assistant  │   │
│  │ (Zustand)   │  │ (Zustand)    │  │ Component        │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/WSS
                         │
┌────────────────────────┴────────────────────────────────────┐
│              AWS API GATEWAY (ap-south-1)                    │
│              REST + WebSocket                                 │
└──────┬──────────────────────────────────────────────────────┘
       │
       ├──────► Lambda: VoiceService (2GB, 300s)
       │         ├──► Amazon Transcribe (STT)
       │         ├──► Bedrock Claude 3 Sonnet (NLU)
       │         ├──► ConversationManager → Redis/DynamoDB
       │         ├──► Intent Detection & Entity Extraction
       │         └──► Amazon Polly (TTS) → S3 → CloudFront
       │
       ├──────► Lambda: SchemeService
       │         ├──► DynamoDB Schemes Table
       │         ├──► Eligibility Algorithm (preserved)
       │         ├──► Eligibility Explanation Builder
       │         └──► Action Plan Generator (multilingual)
       │
       └──────► Lambda: UserService
                 └──► DynamoDB User Profile Table

┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                               │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ DynamoDB (8)  │  │ S3 (3 buckets)│  │ ElastiCache     │   │
│  │ • schemes     │  │ • documents   │  │ Redis           │   │
│  │ • users       │  │ • audio       │  │ • Sessions      │   │
│  │ • applications│  │ • dumps       │  │ • 30min TTL     │   │
│  └───────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. User speaks → Transcribe (language-specific)
2. Text → Claude with session context
3. Extract entities → Update citizen profile in Redis
4. Detect profile gaps → Ask follow-up OR search schemes
5. Calculate eligibility → Format explanation
6. Generate action plan → Return with TTS audio

---

## Slide 7: Team

### TEAM NAME
[Your Team Name]

### MEMBER 01
**Full Name:** [Name]  
**College:** [College Name]  
**Year:** [3rd / Final Year / Fresher]  
**Role:** Full-stack Development & AWS Infrastructure  
**LinkedIn:** [URL]

### MEMBER 02
**Full Name:** [Name]  
**College:** [College Name]  
**Year:** [3rd / Final Year]  
**Role:** AI/ML Integration & Backend Logic  
**LinkedIn:** [URL]

### MEMBER 03
**Full Name:** [Name]  
**College:** [College Name]  
**Year:** [3rd / Final Year]  
**Role:** Frontend Development & UI/UX  
**LinkedIn:** [URL]

---

## Slide 8: Implementation Highlights

### WHAT WE BUILT (Hackathon Scope)

**Phase 1: Backend Foundation ✅**
- Conversational context manager with Redis
- Progressive citizen profile building
- Enhanced eligibility explanation API
- Citizen action plan generator (multilingual)
- Demo scheme data (3 schemes, 6 languages)

**Phase 2: Frontend Integration ✅**
- Voice & conversation Zustand stores
- Enhanced VoiceAssistant component
- EligibilityCard with status visualization
- ActionPlan with document checklist
- API integration hooks

**What Already Existed:**
- AWS infrastructure (deployed)
- Voice pipeline (Transcribe + Bedrock + Polly)
- Eligibility scoring algorithm
- DynamoDB schemas
- S3 buckets & CloudFront

### INNOVATION POINTS

1. **Conversational Memory**: 30-min sessions with 20-message history
2. **Progressive Profiling**: Only asks relevant questions
3. **Explainable AI**: Not just eligible/not - shows WHY
4. **Action Plans**: From eligibility to application in clear steps
5. **True Multilingual**: Language affects entire experience (STT + AI + TTS + UI)

---

## Slide 9: Demo Flow (Telugu Farmer)

### STEP-BY-STEP DEMO

**1. Open Voice for Bharat**
   - https://bharatvisionxai.vercel.app

**2. Navigate to Voice Assistant**
   - Select language: తెలుగు (Telugu)

**3. User speaks:**
   > "నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి"
   > (I want government schemes for farmers)

**4. AI understands:**
   - Intent: SEARCH_SCHEMES
   - Entities: is_farmer=true, occupation=farmer

**5. AI asks follow-up:**
   > "మీరు ఏ రాష్ట్రంలో ఉన్నారు?"
   > (Which state are you in?)

**6. User responds:**
   > "తెలంగాణ"

**7. System shows:**
   - **Citizen Profile**: State=TS, Occupation=Farmer
   - **Matched Scheme**: Rythu Bandhu - రైతు బంధు
   
**8. User asks:**
   > "ఇప్పుడు నేను ఏమి చేయాలి?"
   > (What should I do now?)

**9. System displays:**
   - **Eligibility Card**: LIKELY_ELIGIBLE (75/100)
     - ✓ State: Telangana matches
     - ✓ Occupation: Farmer eligible
     - ⚠ Land ownership: Not verified
   
   - **Action Plan**:
     - Step 1: Obtain Land Records (REQUIRED)
     - Step 2: Upload Aadhaar (REQUIRED)
     - Step 3: Submit Bank Details (REQUIRED)
     - Step 4: Review & Submit
     - Documents: ✓ Aadhaar | ⚠ Land Records | ⚠ Bank Passbook

**10. All in Telugu with voice output**

---

## Slide 10: Technical Excellence

### CODE QUALITY
- **TypeScript** throughout frontend
- **Type-safe** API contracts
- **Error boundaries** and fallbacks
- **Modular architecture** (stores, hooks, components)
- **Clean separation**: Voice logic, scheme logic, UI

### SCALABILITY
- **Serverless** Lambda (auto-scales)
- **DynamoDB On-Demand** (no capacity planning)
- **CloudFront CDN** (global distribution)
- **Redis caching** (fast session retrieval)
- **S3 lifecycle** (auto-cleanup old audio)

### RELIABILITY
- **Graceful degradation** (voice fails → text fallback)
- **Retry logic** for transient failures
- **Session recovery** (30min TTL, extendable)
- **Confidence thresholds** (transcription >0.7)
- **Input validation** (Pydantic models)

### SECURITY
- **No secrets in code** (environment variables)
- **AWS-managed encryption** (DynamoDB, S3)
- **Presigned URLs** (time-limited audio access)
- **CORS configured** (origin whitelisting ready)
- **Demo data labeled** (not real government policy)

---

## Slide 11: AI Integration Details

### MODEL USAGE

**Amazon Transcribe**
- Real-time streaming capable
- Language-specific models (en-IN, hi-IN, te-IN, ta-IN, mr-IN, kn-IN)
- Confidence scoring for quality control

**Anthropic Claude 3 Sonnet (Bedrock)**
- Conversational context (20-message window)
- Intent classification (7 intents)
- Entity extraction (state, occupation, age, etc.)
- Multilingual prompt engineering
- Temperature: 0.7 for natural responses

**Amazon Polly**
- Neural voices (better quality)
- Voice selection per language (Aditi for Hindi, Kajal for Tamil/Telugu)
- TTS caching (MD5 hash) for performance
- Presigned URL delivery

**Future: Amazon Titan Embeddings**
- Semantic scheme search
- RAG for scheme content
- User query understanding

### PROMPT ENGINEERING EXAMPLE

```
You are a helpful assistant for Voice for Bharat, helping Indian 
citizens find government welfare schemes.

Current citizen information known:
- Language: Telugu
- State: Telangana
- Occupation: farmer
- Farmer: Yes

Recent conversation:
USER: నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి
ASSISTANT: మీరు ఏ రాష్ట్రంలో ఉన్నారు?

User's current query (in Telugu): తెలంగాణ

Your task: Confirm their state and tell them you're finding relevant 
farmer schemes in Telangana.

Respond ONLY in Telugu. Keep it to 2-3 sentences. Be warm and helpful.
```

---

## Slide 12: Impact & Future Scope

### IMMEDIATE IMPACT
- **Language inclusion**: 6 Indian languages (covers ~80% population)
- **Voice-first**: Accessible to low-literacy citizens
- **Time saved**: 30-60min → 3-5min per scheme search
- **Explainability**: Users understand WHY they're eligible
- **Actionable**: Clear next steps, not just information dump

### METRICS WE'LL TRACK
- **Scheme discovery rate**: % users who find relevant schemes
- **Application initiation**: % who start application after eligibility check
- **Language distribution**: Which languages are most used
- **Session completion**: % who complete full flow
- **Profile completeness**: Average fields filled per session

### FUTURE ENHANCEMENTS
1. **More languages**: Bengali, Gujarati, Odia, Punjabi
2. **Document AI**: OCR + validation for uploaded docs
3. **Application submission**: Direct portal integration
4. **Scheme recommendation**: ML-based personalization
5. **Multi-modal**: Image input (show your land, we'll verify)
6. **Offline mode**: PWA with cached schemes
7. **WhatsApp integration**: Chatbot on familiar platform
8. **Voice biometrics**: Secure authentication

### SCALABILITY PATH
- **Current**: Demo with 3 schemes
- **Phase 2**: 100+ central government schemes
- **Phase 3**: State-specific schemes (28 states)
- **Phase 4**: District/local schemes
- **Target**: 5000+ schemes across India

---

## Slide 13: Deployment & Live Demo

### PRODUCTION URLS

**Frontend (Live):**
https://bharatvisionxai.vercel.app

**Backend (AWS Mumbai):**
- REST API: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
- WebSocket: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
- CloudFront CDN: https://d18s1aceaoasx3.cloudfront.net

**GitHub Repository:**
https://github.com/sriyathid-commits/voice

### INFRASTRUCTURE
- **Region**: ap-south-1 (Mumbai)
- **Compute**: 7 Lambda functions
- **Database**: 8 DynamoDB tables
- **Storage**: 3 S3 buckets
- **Cache**: Redis (ElastiCache)
- **CDN**: CloudFront
- **Auth**: Cognito (ready)

### CI/CD
- **Frontend**: Vercel (auto-deploy on push)
- **Backend**: AWS SAM (manual deploy for safety)
- **Monitoring**: CloudWatch Logs
- **Alerts**: SNS topics configured

---

## Slide 14: Challenges & Solutions

### CHALLENGE 1: Conversational Context
**Problem**: Voice queries need context - "What should I do next?" depends on current scheme  
**Solution**: Redis-backed session manager with 30min TTL, stores 20 messages + citizen profile

### CHALLENGE 2: Eligibility Explainability
**Problem**: Users don't trust black-box "not eligible" results  
**Solution**: Preserved existing algorithm, built structured explanation layer showing score breakdown

### CHALLENGE 3: Multilingual Consistency
**Problem**: Language affects 5 layers (STT, UI, AI prompts, responses, TTS)  
**Solution**: Language-first architecture - selected language propagates through entire system

### CHALLENGE 4: Progressive Profiling
**Problem**: Don't want 20-question form before showing any schemes  
**Solution**: Intent-based questioning - only ask what's needed for current search/eligibility check

### CHALLENGE 5: Demo Reliability
**Problem**: Real government APIs are slow/unavailable  
**Solution**: Demo scheme data clearly labeled, production-ready schema, swap data source when APIs available

---

## Slide 15: Why We'll Win

### COMPLETENESS
✅ Working voice pipeline (6 languages)  
✅ Conversational AI (not one-shot Q&A)  
✅ Explainable eligibility (not black box)  
✅ Actionable guidance (not just information)  
✅ Production deployment (live demo)

### INNOVATION
🚀 Session-based context memory  
🚀 Progressive profile building  
🚀 Multilingual action plans  
🚀 Document checklist visualization  
🚀 Intent-aware follow-up questions

### TECHNICAL EXCELLENCE
⚡ Serverless architecture (scales automatically)  
⚡ Type-safe code (TypeScript + Pydantic)  
⚡ Clean separation of concerns  
⚡ Error handling & fallbacks  
⚡ Performance optimized (caching, CDN)

### REAL-WORLD READY
🎯 Solves actual problem (language barriers)  
🎯 Serves underserved population (low-literacy)  
🎯 Clear path to scale (5000+ schemes)  
🎯 Deployment infrastructure in place  
🎯 Usable TODAY (live URL)

### HACKATHON ALIGNMENT
✨ Built FOR PS6 (AI for Bharat in Indian Languages)  
✨ Uses cutting-edge AI (Bedrock Claude 3)  
✨ Actual citizen impact (not toy problem)  
✨ Works end-to-end (not proof-of-concept)  
✨ Reproducible & testable

---

## Slide 16: Live Demo QR Code

```
[Generate QR code for https://bharatvisionxai.vercel.app]
```

### TRY IT NOW
1. Scan QR code or visit: **https://bharatvisionxai.vercel.app**
2. Go to "Voice Assistant"
3. Select Telugu (తెలుగు)
4. Tap microphone
5. Say: "నాకు రైతులకు సంబంధించిన ప్రభుత్వ పథకాలు కావాలి"

### WHAT YOU'LL SEE
- Real-time transcription
- Conversational follow-up
- Profile building
- Eligibility explanation
- Action plan generation
- Voice output in Telugu

---

## Slide 17: Social Card Post

**LinkedIn/X Post URL:** [YOUR POST URL HERE]

**Post Text:**
```
🎤 Built Voice for Bharat 2.0 for #BuildFastWithAI Hackathon! 

A voice-first AI assistant helping Indian citizens discover government 
welfare schemes in 6 languages (English, Hindi, Telugu, Tamil, Marathi, 
Kannada).

✨ What makes it special:
• Conversational context (remembers what you said)
• Explainable eligibility (shows WHY you match)
• Action plans (exact steps to apply)
• True multilingual (voice in, voice out)

🚀 Live at: bharatvisionxai.vercel.app
💡 Problem Statement: PS6 - AI for Bharat in Indian Languages

Built with Amazon Bedrock (Claude 3 Sonnet), Transcribe, Polly, and AWS 
serverless stack.

Proud to serve citizens with limited digital literacy! 🇮🇳

#AI #BuildFastWithAI #VoiceAI #AWS #Bedrock #IndianLanguages
```

---

## Slide 18: Code Repositories

### GitHub: https://github.com/sriyathid-commits/voice

```
voice-for-bharat/
├── backend/
│   ├── lambdas/
│   │   ├── voice_service/
│   │   │   ├── conversation_manager.py   (NEW - PS6)
│   │   │   ├── service.py                (ENHANCED)
│   │   │   └── models.py                 (ENHANCED)
│   │   └── scheme_service/
│   │       ├── action_plan_generator.py  (NEW - PS6)
│   │       └── handler.py                (ENHANCED)
│   └── scripts/
│       └── populate_demo_schemes.py      (NEW - PS6)
│
└── frontend/web/src/
    ├── components/
    │   ├── voice/
    │   │   └── VoiceAssistant.tsx        (NEW - PS6)
    │   └── schemes/
    │       ├── EligibilityCard.tsx       (NEW - PS6)
    │       └── ActionPlan.tsx            (NEW - PS6)
    ├── store/
    │   ├── voiceStore.ts                 (NEW - PS6)
    │   └── schemeStore.ts                (NEW - PS6)
    └── hooks/
        └── useSchemeAPI.ts               (NEW - PS6)
```

### KEY COMMITS
1. `feat: AWS infrastructure deployment` (Pre-hackathon)
2. `feat: add conversational context and action planning for PS6` (Hackathon)

---

## Thank You!

### Voice for Bharat 2.0
**Democratizing access to government welfare schemes through voice**

**Live Demo:** https://bharatvisionxai.vercel.app  
**GitHub:** https://github.com/sriyathid-commits/voice  
**Problem Statement:** PS6 - AI for Bharat in Indian Languages

**Built with:**
Amazon Bedrock • Claude 3 Sonnet • Transcribe • Polly  
Next.js 15 • TypeScript • AWS Lambda • DynamoDB

**Team:** [Your Team Name]

**Contact:** [Your LinkedIn/Email]

---

**BUILD FAST WITH AI: AI BUILD CHALLENGE 2026**
