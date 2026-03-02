# Technology Stack

## Frontend

### Web Application
- Framework: Next.js 15 with TypeScript
- Styling: Tailwind CSS
- State Management: Zustand
- Data Fetching: React Query
- Audio Recording: MediaRecorder API
- PWA: next-pwa for offline support
- Hosting: AWS Amplify (production), Vercel (preview branches)

### Mobile Application
- Framework: React Native with TypeScript
- Navigation: React Navigation
- State Management: Zustand
- Audio: react-native-audio-recorder
- Storage: AsyncStorage

## Backend

### API Layer
- Framework: FastAPI with Python 3.11
- Validation: Pydantic models
- Gateway: AWS API Gateway (REST + WebSocket)

### Compute
- Platform: AWS Lambda (Python 3.11, arm64 Graviton2)
- Memory: 512MB-2GB depending on service
- Timeout: 30s-300s depending on service
- Functions: UserService, VoiceService (2GB, 300s), SchemeService, ApplicationService, DocumentService, NotificationService, SyncService

## AI/ML Services (Amazon Bedrock)

- STT/TTS: Amazon Titan (supports 6 Indian languages)
- LLM: Anthropic Claude 3 Sonnet
- Embeddings: Amazon Titan Embeddings
- Vector Store: OpenSearch Serverless
- OCR: Amazon Textract
- Agents: Bedrock Agents with action groups

## Data Storage

### DynamoDB Tables
- users: User authentication and profile data
- schemes: Government welfare scheme information
- applications: User applications to schemes
- activity_log: User activity tracking (90-day TTL)
- user_profile: Extended profile data for eligibility

All tables use On-Demand billing with AWS-managed encryption and Point-in-Time Recovery.

### S3 Buckets
- voice-for-bharat-documents: User documents (SSE-S3 encryption, 7-year retention)
- voice-for-bharat-audio: Voice recordings and TTS cache (30-90 day lifecycle)
- voice-for-bharat-scheme-dumps: Scheme data backups

## Authentication
- Service: AWS Cognito
- Method: Phone number OTP
- Optional: MFA support
- Custom Lambda triggers for user lifecycle events

## Caching
- Service: ElastiCache (Redis)
- Usage: Active conversation sessions, frequently accessed schemes

## Content Delivery
- CDN: CloudFront
- DNS: Route 53
- Signed URLs for secure document access

## Messaging & Events
- EventBridge: Event-driven architecture
- SQS: Asynchronous job queues
- SNS: Notifications (SMS, Email, Push)
- WhatsApp Business API: Chat support

## Common Commands

### Development
```bash
# Install dependencies
npm install

# Run development server (web)
npm run dev

# Run mobile app
npm run ios
npm run android

# Type checking
npm run type-check

# Linting
npm run lint
```

### Testing
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Build & Deploy
```bash
# Build for production
npm run build

# Deploy to Amplify (production)
amplify push

# Deploy preview (Vercel)
vercel deploy
```

### Backend (Python)
```bash
# Install dependencies
pip install -r requirements.txt

# Run local API server
uvicorn main:app --reload

# Run tests
pytest

# Deploy Lambda functions
sam build && sam deploy
```

## API Endpoints

### REST API
- POST /register - User registration
- POST /verify-otp - OTP verification
- GET /profile - Get user profile
- PUT /profile - Update user profile
- GET /schemes - List schemes (with filters)
- GET /schemes/{id} - Get scheme details
- POST /schemes/{id}/check-eligibility - Check eligibility
- POST /schemes/{id}/save - Save scheme
- POST /applications - Create application
- GET /applications - List user applications
- GET /applications/{id} - Get application details
- PUT /applications/{id} - Update application
- POST /applications/{id}/submit - Submit application
- POST /documents/upload - Upload document (multipart)
- GET /documents/{id} - Get document
- DELETE /documents/{id} - Delete document
- POST /voice/query - Process voice query (multipart audio)
- GET /voice/session/{id} - Get conversation session
- GET /activity - Get activity log

### WebSocket API
- /ws/voice - Real-time audio streaming
- Messages: StartRecording, AudioChunk, StopRecording, TranscriptionUpdate, ResponseReady, Error

## Supported Languages
- English (EN)
- Hindi (HI)
- Marathi (MR)
- Kannada (KN)
- Tamil (TA)
- Telugu (TE)

## Design System

### Responsive Breakpoints
- Mobile: 320px - 767px (single column)
- Tablet: 768px - 1023px (2 columns)
- Desktop: 1024px+ (3 columns)

### Touch Targets
- Minimum size: 44x44px
- Card padding: 20px
- Button height: 48px (secondary), 56px (primary)

### Typography
- Metric numbers: 32px bold
- Card titles: 14px medium
- Activity items: 16px regular
- Timestamps: 12px light
- Primary CTA: 18px
- Secondary CTA: 16px

### Colors
- Primary: Blue
- Success: Green
- Warning: Orange/Yellow
- Error: Red
- Info: Purple
