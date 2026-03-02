# Project Structure

## Overview

Voice for Bharat follows a monorepo structure with separate frontend (Next.js web + React Native mobile) and backend (FastAPI Lambda functions) codebases. The architecture is serverless, leveraging AWS services for compute, storage, and AI capabilities.

## Repository Organization

```
voice-for-bharat/
├── frontend/
│   ├── web/                    # Next.js web application
│   │   ├── src/
│   │   │   ├── app/           # Next.js 15 app directory
│   │   │   ├── components/    # Reusable UI components
│   │   │   ├── lib/           # Utilities and helpers
│   │   │   ├── hooks/         # Custom React hooks
│   │   │   ├── store/         # Zustand state management
│   │   │   └── types/         # TypeScript type definitions
│   │   ├── public/            # Static assets
│   │   └── package.json
│   │
│   └── mobile/                # React Native mobile app
│       ├── src/
│       │   ├── screens/       # Screen components
│       │   ├── components/    # Reusable components
│       │   ├── navigation/    # React Navigation setup
│       │   ├── store/         # Zustand state management
│       │   ├── services/      # API clients
│       │   └── types/         # TypeScript types
│       └── package.json
│
├── backend/
│   ├── lambdas/               # AWS Lambda functions
│   │   ├── user_service/      # User management
│   │   ├── voice_service/     # Voice processing (2GB, 300s)
│   │   ├── scheme_service/    # Scheme search and matching
│   │   ├── application_service/ # Application lifecycle
│   │   ├── document_service/  # Document upload/validation
│   │   ├── notification_service/ # Multi-channel notifications
│   │   └── sync_service/      # External API sync
│   │
│   ├── shared/                # Shared utilities
│   │   ├── models/            # Pydantic models
│   │   ├── utils/             # Helper functions
│   │   └── constants/         # Configuration constants
│   │
│   └── requirements.txt       # Python dependencies
│
├── infrastructure/            # AWS infrastructure as code
│   ├── cloudformation/        # CloudFormation templates
│   ├── sam/                   # SAM templates for Lambda
│   └── amplify/               # Amplify configuration
│
└── .kiro/                     # Kiro configuration
    ├── specs/                 # Feature specifications
    └── steering/              # AI assistant guidance
```

## Key Directories

### Frontend Web (`frontend/web/src/`)

- `app/`: Next.js 15 app directory with file-based routing
  - `(dashboard)/`: Dashboard and authenticated routes
  - `(auth)/`: Authentication flows (OTP)
  - `api/`: API route handlers
- `components/`: Reusable UI components
  - `ui/`: Base components (Button, Card, Input)
  - `dashboard/`: Dashboard-specific components (MetricCard, ActivityTimeline)
  - `voice/`: Voice assistant components (VoiceRecorder, AudioPlayer)
  - `schemes/`: Scheme-related components (SchemeCard, EligibilityBadge)
- `lib/`: Utilities and configuration
  - `api.ts`: API client setup
  - `auth.ts`: Authentication helpers
  - `constants.ts`: App-wide constants
- `hooks/`: Custom React hooks
  - `useVoiceRecorder.ts`: Audio recording logic
  - `useAuth.ts`: Authentication state
  - `useSchemes.ts`: Scheme data fetching
- `store/`: Zustand stores
  - `authStore.ts`: User authentication state
  - `voiceStore.ts`: Voice interaction state
  - `schemeStore.ts`: Scheme browsing state

### Frontend Mobile (`frontend/mobile/src/`)

- `screens/`: Full-screen components
  - `DashboardScreen.tsx`
  - `VoiceSearchScreen.tsx`
  - `SchemeDetailsScreen.tsx`
  - `ApplicationScreen.tsx`
- `navigation/`: Navigation configuration
  - `RootNavigator.tsx`: Main navigation stack
  - `AuthNavigator.tsx`: Authentication flow
  - `DashboardNavigator.tsx`: Authenticated routes
- `services/`: API integration
  - `api.ts`: REST API client
  - `websocket.ts`: WebSocket client for voice
  - `storage.ts`: AsyncStorage wrapper

### Backend (`backend/lambdas/`)

Each Lambda function follows this structure:
```
service_name/
├── handler.py          # Lambda entry point
├── service.py          # Business logic
├── models.py           # Pydantic models
├── utils.py            # Helper functions
└── requirements.txt    # Service-specific dependencies
```

### Lambda Functions

- `user_service/`: User registration, profile management, authentication
- `voice_service/`: Audio transcription, LLM processing, TTS synthesis (2GB memory, 300s timeout)
- `scheme_service/`: Scheme search, filtering, eligibility calculation
- `application_service/`: Application CRUD, submission, status tracking
- `document_service/`: Document upload to S3, OCR extraction, validation
- `notification_service/`: SMS, email, push, WhatsApp notifications
- `sync_service/`: Sync scheme data from government APIs

## Component Organization

### UI Components (Web)

Components follow atomic design principles:

- **Atoms**: Button, Input, Badge, Icon
- **Molecules**: MetricCard, SchemeCard, ActivityItem, StepIndicator
- **Organisms**: DashboardHeader, ActivityTimeline, VoiceAssistant, SchemeList
- **Templates**: DashboardLayout, ApplicationLayout
- **Pages**: Dashboard, SchemeSearch, ApplicationTracking

### State Management

Zustand stores are organized by domain:

- `authStore`: User session, profile, authentication status
- `voiceStore`: Recording state, conversation history, audio playback
- `schemeStore`: Scheme list, filters, saved schemes
- `applicationStore`: Application drafts, submissions, status
- `uiStore`: Modal state, toast notifications, loading states

## Data Flow

### Voice Interaction Flow
```
User → VoiceRecorder → WebSocket → voice_service Lambda
→ Amazon Transcribe → Bedrock (Claude) → scheme_service
→ Bedrock (Titan TTS) → S3 → CloudFront → AudioPlayer
```

### Application Submission Flow
```
User → ApplicationForm → API Gateway → application_service
→ DynamoDB → EventBridge → notification_service
→ SNS/WhatsApp → User notification
```

### Document Upload Flow
```
User → FileUpload → API Gateway → document_service
→ S3 (encrypted) → Textract (OCR) → DynamoDB metadata
→ Presigned URL → User confirmation
```

## Database Schema Organization

### DynamoDB Tables

- `users`: Partition key: `userId`, GSI: `phoneNumber`, `state+category`
- `schemes`: Partition key: `schemeId`, GSI: `state+category`, `isActive+lastSyncedAt`
- `applications`: Partition key: `applicationId`, GSI: `userId+status`, `schemeId+submittedAt`
- `activity_log`: Partition key: `activityId`, GSI: `userId+timestamp`, `type+timestamp` (90-day TTL)
- `user_profile`: Partition key: `userId`, GSI: `state+profileStrength`

### S3 Bucket Structure

**voice-for-bharat-documents/**
```
users/{userId}/
  aadhaar/{documentId}.pdf
  pan/{documentId}.pdf
  income-certificate/{documentId}.pdf
  caste-certificate/{documentId}.pdf
  bank-passbook/{documentId}.pdf
  photos/{documentId}.jpg
applications/{applicationId}/{documentType}/{documentId}.pdf
```

**voice-for-bharat-audio/**
```
conversations/{sessionId}/
  user/{messageId}.wav
  assistant/{messageId}.mp3
tts-cache/{language}/{textHash}.mp3
stt-recordings/{userId}/{timestamp}.wav
```

## Naming Conventions

### Files and Directories
- Components: PascalCase (e.g., `VoiceRecorder.tsx`, `SchemeCard.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`, `calculateEligibility.ts`)
- Hooks: camelCase with `use` prefix (e.g., `useVoiceRecorder.ts`)
- Stores: camelCase with `Store` suffix (e.g., `authStore.ts`)
- Lambda handlers: snake_case (e.g., `user_service/handler.py`)

### Code
- React components: PascalCase
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Types/Interfaces: PascalCase
- Python functions: snake_case
- Python classes: PascalCase

## Configuration Files

- `package.json`: Dependencies and scripts
- `tsconfig.json`: TypeScript configuration
- `tailwind.config.js`: Tailwind CSS customization
- `next.config.js`: Next.js configuration
- `amplify.yml`: Amplify build configuration
- `template.yaml`: SAM template for Lambda deployment
- `requirements.txt`: Python dependencies

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_URL`: API Gateway endpoint
- `NEXT_PUBLIC_WS_URL`: WebSocket endpoint
- `NEXT_PUBLIC_CLOUDFRONT_URL`: CloudFront distribution
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID`: Cognito user pool
- `NEXT_PUBLIC_COGNITO_CLIENT_ID`: Cognito app client

### Backend
- `DYNAMODB_TABLE_PREFIX`: Table name prefix
- `S3_DOCUMENTS_BUCKET`: Documents bucket name
- `S3_AUDIO_BUCKET`: Audio bucket name
- `BEDROCK_REGION`: AWS region for Bedrock
- `COGNITO_USER_POOL_ID`: Cognito user pool
- `WHATSAPP_API_KEY`: WhatsApp Business API key

## Testing Structure

### Frontend Tests
```
__tests__/
├── components/        # Component tests
├── hooks/            # Hook tests
├── utils/            # Utility tests
└── integration/      # Integration tests
```

### Backend Tests
```
tests/
├── unit/             # Unit tests
├── integration/      # Integration tests
└── fixtures/         # Test data
```

## Deployment Structure

- **Production**: AWS Amplify (web) + Lambda (backend)
- **Preview**: Vercel (web) + Lambda (backend)
- **CI/CD**: GitHub Actions → Amplify/SAM deploy
- **Environments**: dev, staging, production
