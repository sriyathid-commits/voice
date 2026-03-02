# Voice for Bharat

A voice-first, AI-powered platform democratizing access to government welfare schemes across India through multilingual voice interaction.

## 🌟 Live Demo

**Production URL**: https://bharatvisionxai.vercel.app

## 📋 Overview

Voice for Bharat bridges the digital divide by enabling citizens with varying levels of digital literacy to discover, understand, and apply for government welfare schemes through voice interaction in 6 Indian languages.

### Supported Languages
- English
- Hindi
- Marathi
- Kannada
- Tamil
- Telugu

## 🚀 Features

- **Voice Assistant**: Multilingual AI-powered voice interaction
- **Visual Dashboard**: Track applications and saved schemes
- **Real-time Status**: Application tracking with timeline view
- **Document Management**: Upload and verification workflows
- **Smart Filtering**: State-specific scheme recommendations
- **Eligibility Matching**: Personalized scheme suggestions
- **24/7 Support**: Voice, chat, and WhatsApp channels

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 15 with TypeScript
- **Styling**: Tailwind CSS
- **State**: Zustand
- **PWA**: Offline support with next-pwa
- **Hosting**: Vercel

### Backend (AWS - Mumbai Region)
- **API**: AWS API Gateway (REST + WebSocket)
- **Compute**: AWS Lambda (7 services)
  - User Service
  - Voice Service (2GB, 300s timeout)
  - Scheme Service
  - Application Service
  - Document Service
  - Notification Service
  - Sync Service
- **Database**: DynamoDB (8 tables)
- **Storage**: S3 (3 buckets)
- **Auth**: AWS Cognito
- **Cache**: ElastiCache Redis
- **CDN**: CloudFront

### AI/ML (Amazon Bedrock)
- **STT/TTS**: Amazon Titan
- **LLM**: Anthropic Claude 3 Sonnet
- **Embeddings**: Amazon Titan Embeddings
- **OCR**: Amazon Textract

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

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS CLI configured
- AWS SAM CLI

### Frontend Setup

```bash
cd frontend/web
npm install
cp .env.example .env.local
# Update .env.local with your API endpoints
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
sam build
sam deploy --guided
```

## 🌐 API Endpoints

### REST API
- `POST /register` - User registration
- `POST /verify-otp` - OTP verification
- `GET /profile` - Get user profile
- `GET /schemes` - List schemes
- `POST /schemes/{id}/check-eligibility` - Check eligibility
- `POST /applications` - Create application
- `POST /documents/upload` - Upload document
- `POST /voice/query` - Process voice query

### WebSocket API
- `/ws/voice` - Real-time audio streaming

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

## 🎯 Success Metrics

- Profile strength percentage
- Active applications count
- Saved schemes count
- Application submission success rate
- Voice interaction completion rate

## 📄 Documentation

- [AWS Development Guide](AWS_DEVELOPMENT_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Production Links](PRODUCTION_LINKS.md)
- [Complete Setup Guide](COMPLETE_SETUP_GUIDE.md)

## 🔗 Production Links

- **Frontend**: https://bharatvisionxai.vercel.app
- **REST API**: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
- **WebSocket**: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
- **CloudFront**: https://d18s1aceaoasx3.cloudfront.net

## 🤝 Contributing

This is a production application serving citizens across India. Contributions should focus on:
- Accessibility improvements
- Language support enhancements
- Performance optimizations
- Security hardening

## 📝 License

Proprietary - Voice for Bharat Platform

## 👥 Target Users

Citizens across India seeking government welfare schemes, particularly those with limited digital literacy or language barriers.

## 🌍 Impact

Serving millions of concurrent users across diverse geographic locations, democratizing access to government welfare information.

---

Built with ❤️ for Bharat
