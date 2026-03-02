# Voice for Bharat - Backend Services

This directory contains the backend Lambda services for the Voice for Bharat platform, built with FastAPI and Python 3.11.

## Architecture

The backend consists of 7 microservices deployed as AWS Lambda functions:

1. **User Service** (512MB, 30s) - User registration, authentication, and profile management
2. **Voice Service** (2GB, 300s) - Voice processing with STT, NLP, and TTS (critical path)
3. **Scheme Service** (1GB, 60s) - Scheme search, filtering, and eligibility matching
4. **Application Service** (512MB, 60s) - Application lifecycle management
5. **Document Service** (1GB, 60s) - Document upload, validation, and OCR
6. **Notification Service** (512MB, 30s) - Multi-channel notifications
7. **Sync Service** (1GB, 300s) - Scheduled scheme data synchronization

## Directory Structure

```
backend/
├── lambdas/
│   ├── user_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── voice_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── scheme_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── application_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── document_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   ├── notification_service/
│   │   ├── handler.py
│   │   └── requirements.txt
│   └── sync_service/
│       ├── handler.py
│       └── requirements.txt
├── shared/
│   ├── constants.py
│   ├── models.py
│   └── utils.py
├── template.yaml
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.11
- AWS CLI configured
- AWS SAM CLI installed
- Access to AWS account with appropriate permissions

### Local Development

1. Create a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install service-specific dependencies:
```bash
cd lambdas/user_service
pip install -r requirements.txt
cd ../..
```

### Environment Variables

Create a `.env` file with the following variables:

```env
AWS_REGION=ap-south-1
DYNAMODB_TABLE_PREFIX=voice-for-bharat-dev
S3_DOCUMENTS_BUCKET=voice-for-bharat-documents-dev
S3_AUDIO_BUCKET=voice-for-bharat-audio-dev
S3_SCHEME_DUMPS_BUCKET=voice-for-bharat-scheme-dumps-dev
COGNITO_USER_POOL_ID=your-user-pool-id
BEDROCK_REGION=ap-south-1
```

## Deployment

### Using SAM CLI

1. Build the application:
```bash
sam build
```

2. Deploy to AWS:
```bash
sam deploy --guided
```

Follow the prompts to configure:
- Stack name: `voice-for-bharat-backend-dev`
- AWS Region: `ap-south-1`
- Environment: `dev`
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`

### Deploy to Specific Environment

```bash
# Development
sam deploy --parameter-overrides Environment=dev

# Staging
sam deploy --parameter-overrides Environment=staging

# Production
sam deploy --parameter-overrides Environment=production
```

## Testing

### Run Unit Tests

```bash
pytest tests/unit/
```

### Run Integration Tests

```bash
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=lambdas --cov-report=html
```

## API Endpoints

### User Service
- `POST /register` - Register new user
- `POST /verify-otp` - Verify OTP
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile

### Voice Service
- `POST /voice/query` - Process voice query
- `GET /voice/session/{session_id}` - Get conversation session
- `WS /ws/voice` - WebSocket for real-time voice

### Scheme Service
- `GET /schemes` - List schemes with filters
- `GET /schemes/{scheme_id}` - Get scheme details
- `POST /schemes/{scheme_id}/check-eligibility` - Check eligibility
- `POST /schemes/{scheme_id}/save` - Save scheme

### Application Service
- `POST /applications` - Create application
- `GET /applications` - List applications
- `GET /applications/{application_id}` - Get application
- `PUT /applications/{application_id}` - Update application
- `POST /applications/{application_id}/submit` - Submit application

### Document Service
- `POST /documents/upload` - Upload document
- `GET /documents/{document_id}` - Get document
- `DELETE /documents/{document_id}` - Delete document

### Notification Service
- `POST /notifications/send` - Send notification
- `GET /notifications/history` - Get notification history

## Shared Utilities

### Constants (`shared/constants.py`)
- Supported languages, states, categories
- DynamoDB table names
- S3 bucket names
- Bedrock model IDs
- Configuration constants

### Models (`shared/models.py`)
- Pydantic models for all data structures
- Validation rules
- Type definitions

### Utils (`shared/utils.py`)
- AWS client helpers
- Presigned URL generation
- Profile strength calculation
- Validation functions
- Utility functions

## Lambda Configuration

| Service | Memory | Timeout | Trigger |
|---------|--------|---------|---------|
| User Service | 512MB | 30s | API Gateway |
| Voice Service | 2GB | 300s | API Gateway + WebSocket |
| Scheme Service | 1GB | 60s | API Gateway |
| Application Service | 512MB | 60s | API Gateway |
| Document Service | 1GB | 60s | API Gateway |
| Notification Service | 512MB | 30s | API Gateway + SQS |
| Sync Service | 1GB | 300s | EventBridge (daily) |

## IAM Permissions

Each Lambda function has access to:
- DynamoDB tables (read/write)
- S3 buckets (read/write)
- Amazon Bedrock (invoke models)
- AWS Cognito (user management)
- Amazon SNS (notifications)
- Amazon Textract (OCR)
- EventBridge (event publishing)

## Monitoring

### CloudWatch Logs
All Lambda functions log to CloudWatch Logs with the following format:
- Log Group: `/aws/lambda/voice-for-bharat-{service}-{environment}`
- Retention: 30 days (dev), 90 days (production)

### CloudWatch Metrics
Key metrics tracked:
- Invocation count
- Error count
- Duration
- Throttles
- Concurrent executions

### X-Ray Tracing
Distributed tracing enabled for all services to track request flow.

## Development Guidelines

1. **Code Style**: Follow PEP 8, use Black for formatting
2. **Type Hints**: Use type hints for all function parameters and returns
3. **Error Handling**: Use try-except blocks and log errors appropriately
4. **Validation**: Use Pydantic models for request/response validation
5. **Testing**: Write unit tests for all business logic
6. **Documentation**: Add docstrings to all functions and classes

## Troubleshooting

### Lambda Timeout
If Voice Service times out, increase timeout in `template.yaml`:
```yaml
Timeout: 300  # Increase if needed
```

### Memory Issues
If Lambda runs out of memory, increase MemorySize:
```yaml
MemorySize: 2048  # Increase if needed
```

### Cold Start
To reduce cold start times:
- Keep package size small
- Use arm64 architecture (Graviton2)
- Consider provisioned concurrency for critical paths

## License

Copyright © 2024 Voice for Bharat. All rights reserved.
