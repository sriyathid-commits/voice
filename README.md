# Voice for Bharat 2.0

A voice-first, AI-powered platform democratizing access to government welfare schemes across India through multilingual voice interaction.

> **🏆 BUILD FAST WITH AI Hackathon Submission**  
> **Problem Statement**: PS6 - AI for Bharat in Indian Languages  
> **Theme**: Building solutions that bridge language barriers for Indian citizens

## 🌟 Live Demo

**Production URL**: https://bharatvisionxai.vercel.app  
**Demo Guide**: [DEMO_GUIDE.md](DEMO_GUIDE.md)  
**Presentation**: [HACKATHON_PRESENTATION.md](HACKATHON_PRESENTATION.md)

## 📋 Overview

Voice for Bharat bridges the digital divide by enabling citizens with varying levels of digital literacy to discover, understand, and apply for government welfare schemes through voice interaction in 6 Indian languages.

### Supported Languages
- English
- Hindi
- Marathi
- Kannada
- Tamil
- Telugu

## 🚀 Key Features (NEW in 2.0)

### 🎯 Conversational AI Voice Assistant
- **6 Indian Languages**: English, Hindi, Marathi, Kannada, Tamil, Telugu
- **Context-Aware Conversations**: Remembers your profile and preferences
- **Progressive Profile Building**: Learns about you through natural dialogue
- **Intent Recognition**: Understands queries about eligibility, applications, documents

### 📊 Explainable Eligibility System
- **4-Level Status**: ELIGIBLE → LIKELY_ELIGIBLE → NEEDS_VERIFICATION → NOT_ELIGIBLE
- **Transparent Scoring**: See exactly why you qualify (or don't)
- **Matched Conditions**: Green checkmarks for requirements you meet
- **Missing Information**: Clear list of what's needed to qualify
- **Verification Needed**: Documents required for final confirmation

### 📋 Personalized Action Plans
- **Step-by-Step Guidance**: Complete roadmap from eligibility to application
- **Document Checklist**: See what you have vs. what's required
- **Application Method**: Online portal, office visit, or mobile app
- **Portal Links**: Direct URLs to official government portals
- **Multilingual Instructions**: Available in all 6 supported languages

### 📱 Additional Features
- **Visual Dashboard**: Track applications and saved schemes
- **Real-time Status**: Application tracking with timeline view
- **Document Management**: Upload and verification workflows
- **Smart Filtering**: State-specific scheme recommendations
- **24/7 Support**: Voice, chat, and WhatsApp channels

## 🏗️ Technical Architecture (2.0 Enhancements)

### Frontend (Next.js 15 + TypeScript)
- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS
- **State Management**: Zustand (voiceStore, schemeStore, authStore)
- **Voice Recording**: MediaRecorder API with 10s auto-stop
- **Components**: VoiceAssistant, EligibilityCard, ActionPlan
- **Hooks**: useSchemeAPI, useVoiceRecorder, useAuth
- **PWA**: Offline support with next-pwa
- **Hosting**: Vercel (Production + Preview branches)

### Backend (AWS Lambda + Python 3.11)
- **API Gateway**: REST + WebSocket
- **Lambda Functions**:
  - `voice_service` (2GB, 300s) - Conversational AI with context
  - `scheme_service` - Eligibility explanation + action plans
  - `user_service` - Profile management
  - `application_service` - Application lifecycle
  - `document_service` - Document handling
  - `notification_service` - Multi-channel notifications
  - `sync_service` - External API sync
- **Database**: DynamoDB (8 tables) + ElastiCache Redis (sessions)
- **Storage**: S3 (3 buckets) + CloudFront CDN
- **Auth**: AWS Cognito (Phone OTP)

### AI/ML Stack (Amazon Bedrock)
- **Speech-to-Text**: Amazon Titan (6 Indian languages)
- **Text-to-Speech**: Amazon Titan (multilingual)
- **LLM**: Anthropic Claude 3 Sonnet
  - Intent extraction
  - Entity recognition
  - Eligibility explanations
  - Action plan generation
- **Embeddings**: Amazon Titan Embeddings
- **Vector Store**: OpenSearch Serverless
- **OCR**: Amazon Textract

### Key Components (NEW)
- **ConversationManager**: 30-minute session management with Redis
- **CitizenProfile**: Progressive profile building from conversations
- **EligibilityExplainer**: 4-level status with transparent reasoning
- **ActionPlanGenerator**: Multilingual step-by-step guidance

## 📦 Project Structure

```
voice-for-bharat/
├── frontend/
│   └── web/              # Next.js web application
│       ├── src/
│       │   ├── app/      # Next.js 15 app directory
│       │   ├── components/
│       │   ├── lib/
│       │   ├── hooks/
│       │   ├── store/
│       │   └── types/
│       └── public/
├── backend/
│   ├── lambdas/          # AWS Lambda functions
│   │   ├── user_service/
│   │   ├── voice_service/
│   │   ├── scheme_service/
│   │   ├── application_service/
│   │   ├── document_service/
│   │   ├── notification_service/
│   │   └── sync_service/
│   ├── shared/           # Shared utilities
│   └── template.yaml     # SAM template
└── docs/                 # Documentation
```

## 🛠️ Quick Start (Development)

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS CLI configured
- AWS SAM CLI

### 1. Frontend Setup

```bash
cd frontend/web
npm install
cp .env.example .env.local
# Update .env.local with API endpoints (see below)
npm run dev
# Open http://localhost:3000
```

### 2. Backend Setup (Local Testing)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Test individual Lambda functions locally
cd lambdas/voice_service
python handler.py
```

### 3. Full Backend Deployment (AWS)

```bash
cd backend
sam build
sam deploy --guided --region ap-south-1

# Populate demo schemes
python scripts/populate_demo_schemes.py
```

### 4. Configure Frontend with Backend URLs

After deploying backend, update `frontend/web/.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-api-gateway-id.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://your-websocket-id.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL=https://your-cloudfront-id.cloudfront.net
NEXT_PUBLIC_COGNITO_USER_POOL_ID=ap-south-1_xxxxxxxxx
NEXT_PUBLIC_COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🎬 Demo Flow (Telugu Farmer Scenario)

See [DEMO_GUIDE.md](DEMO_GUIDE.md) for detailed step-by-step demo instructions.

**Quick Demo Path**:
1. Open https://bharatvisionxai.vercel.app
2. Navigate to Voice Assistant
3. Select "Telugu" language
4. Say: "నేను రైతును. నాకు ఏమైనా స్కీమ్‌లు ఉన్నాయా?" (I am a farmer. Are there any schemes for me?)
5. View eligibility explanation with matched conditions
6. Get personalized action plan with document checklist
7. Track profile completeness and next steps

## 🌐 API Endpoints (NEW in 2.0)

### Voice & Conversation
- `POST /voice/query` - Process voice query with conversational context
- `GET /voice/session/{id}` - Get conversation session and profile
- `POST /voice/update-profile` - Update citizen profile from conversation

### Eligibility & Action Plans
- `POST /schemes/{id}/eligibility-explanation` - Get structured eligibility with reasons
- `POST /schemes/{id}/action-plan` - Generate personalized action plan
- `GET /schemes/{id}/complete-analysis` - Combined eligibility + action plan

### Existing Endpoints
- `POST /register` - User registration
- `POST /verify-otp` - OTP verification
- `GET /profile` - Get user profile
- `GET /schemes` - List schemes with filters
- `POST /schemes/{id}/check-eligibility` - Quick eligibility check
- `POST /applications` - Create application
- `POST /documents/upload` - Upload document

### WebSocket API
- `/ws/voice` - Real-time audio streaming with context

## 📊 Database Schema

### DynamoDB Tables
- **users**: User authentication and profiles
- **schemes**: Government welfare schemes
- **applications**: User applications
- **activity_log**: User activity (90-day TTL)
- **user_profile**: Extended profile data
- **documents**: Document metadata
- **notifications**: User notifications
- **sync_status**: External API sync tracking

### S3 Buckets
- **documents**: User documents (7-year retention)
- **audio**: Voice recordings and TTS cache (30-90 day lifecycle)
- **scheme-dumps**: Scheme data backups

## 🔐 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-api-gateway-url
NEXT_PUBLIC_WS_URL=wss://your-websocket-url
NEXT_PUBLIC_CLOUDFRONT_URL=https://your-cloudfront-url
NEXT_PUBLIC_COGNITO_USER_POOL_ID=your-user-pool-id
NEXT_PUBLIC_COGNITO_CLIENT_ID=your-client-id
```

### Backend (Lambda Environment)
```env
DYNAMODB_TABLE_PREFIX=voice-for-bharat
S3_DOCUMENTS_BUCKET=voice-for-bharat-documents
S3_AUDIO_BUCKET=voice-for-bharat-audio
BEDROCK_REGION=ap-south-1
COGNITO_USER_POOL_ID=your-user-pool-id
```

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend/web
npm run build
vercel --prod
```

### Backend (AWS SAM)
```bash
cd backend
sam build
sam deploy --stack-name voicebharatai --region ap-south-1
```

## 📱 User Flows

1. **Voice Search**: User speaks → AI matches schemes → Displays eligibility
2. **Eligibility Check**: Profile-based matching with detailed reasons
3. **Application**: Document upload → Submission → Real-time tracking
4. **Dashboard**: View applications, saved schemes, profile strength

## 🎯 Hackathon Success Metrics

### User Experience
- ✅ **Zero Learning Curve**: Voice-first interaction in native language
- ✅ **Transparent Eligibility**: Citizens understand WHY they qualify
- ✅ **Clear Next Steps**: Action plans eliminate confusion
- ✅ **Progressive Profiling**: No overwhelming forms upfront

### Technical Excellence
- ✅ **Conversational Context**: 30-minute session memory
- ✅ **Intent Recognition**: Understands natural queries
- ✅ **Explainable AI**: 4-level eligibility with reasons
- ✅ **Multilingual Support**: 6 Indian languages end-to-end
- ✅ **Production Ready**: Deployed on AWS + Vercel

### Impact Potential
- 🎯 **500M+ Citizens**: Target audience with limited digital literacy
- 🎯 **6 Languages**: Covering 80%+ of Indian population
- 🎯 **24/7 Availability**: No office hours constraint
- 🎯 **Scalable Architecture**: Serverless for millions of users

## 📄 Documentation

- **[DEMO_GUIDE.md](DEMO_GUIDE.md)** - Step-by-step Telugu farmer demo scenario
- **[HACKATHON_PRESENTATION.md](HACKATHON_PRESENTATION.md)** - Complete presentation deck
- **[PHASE1_IMPLEMENTATION_SUMMARY.md](PHASE1_IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- [AWS Development Guide](AWS_DEVELOPMENT_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [DynamoDB Schemas](backend/docs/DYNAMODB_SCHEMAS.md)
- [S3 Bucket Guide](backend/docs/S3_BUCKET_GUIDE.md)

## 🔗 Production Links

- **Frontend**: https://bharatvisionxai.vercel.app
- **REST API**: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
- **WebSocket**: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
- **CloudFront**: https://d18s1aceaoasx3.cloudfront.net

## 🤝 Team & Contact

**Team**: BharatVisionXAI  
**Hackathon**: BUILD FAST WITH AI (PS6 - AI for Bharat in Indian Languages)  
**GitHub**: [Repository Link]  
**Demo**: https://bharatvisionxai.vercel.app

### Key Differentiators
1. **Conversational Context**: Unlike static forms, we remember your profile across conversations
2. **Explainable AI**: Transparent eligibility explanations build trust
3. **Action Plans**: Clear roadmap from eligibility to application submission
4. **Multilingual End-to-End**: Voice + UI + responses all in native language
5. **Production Ready**: Fully deployed AWS infrastructure, not just a prototype

## 🎨 Why We'll Win

### 1. Real Problem, Real Solution
- 400M+ Indians face language barriers accessing welfare schemes
- Our solution works for citizens with ZERO digital literacy

### 2. Technical Excellence
- Conversational AI with 30-minute context memory
- 4-level explainable eligibility system
- Multilingual action plans with document checklists
- Production-ready AWS infrastructure

### 3. User-Centric Design
- Progressive profiling (no overwhelming forms)
- Transparent explanations (trust through clarity)
- Voice-first interaction (accessibility by default)

### 4. Scalability & Impact
- Serverless architecture for millions of users
- 6 languages covering 80%+ population
- Government partnership ready (API integrations included)

---

**Built with ❤️ for Bharat's Digital Inclusion**

> _"Democratizing access to government welfare through voice, AI, and Indian languages"_
