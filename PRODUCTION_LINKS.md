# Voice for Bharat - Production Links

## Frontend (Vercel)
- **Production URL**: https://bharatvisionxai.vercel.app
- **Deployment URL**: https://bharatvisionxai-brnp0qfpz-sriyathid-commits-projects.vercel.app
- **Inspect**: https://vercel.com/sriyathid-commits-projects/bharatvisionxai/D63Pof7nuuaDZFJtEXSQZoE436WM

## Backend (AWS - ap-south-1 Mumbai)

### API Endpoints
- **REST API**: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
- **WebSocket API**: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev

### CloudFront CDN
- **Distribution**: https://d18s1aceaoasx3.cloudfront.net

### AWS Cognito
- **User Pool ID**: ap-south-1_lbk6t80Qf
- **Client ID**: 78d8776ct03jlp6n5heqic32gn
- **Region**: ap-south-1

### Lambda Functions (7 services)
- UserService
- VoiceService (2GB memory, 300s timeout)
- SchemeService
- ApplicationService
- DocumentService
- NotificationService
- SyncService

### DynamoDB Tables (8 tables)
- users
- schemes
- applications
- activity_log (90-day TTL)
- user_profile
- documents
- notifications
- sync_status

### S3 Buckets (3 buckets)
- voice-for-bharat-documents (7-year retention)
- voice-for-bharat-audio (30-90 day lifecycle)
- voice-for-bharat-scheme-dumps

### ElastiCache Redis
- Cluster: voice-for-bharat-cache
- Node Type: cache.t3.micro

## Stack Information
- **Stack Name**: voicebharatai
- **Region**: ap-south-1 (Mumbai)
- **Status**: Deployed and operational

## Deployment Date
- March 2, 2026

## Access
- Frontend is publicly accessible
- Backend APIs require authentication via AWS Cognito
- All AWS resources are in ap-south-1 region
