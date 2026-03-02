# Voice for Bharat - AWS Infrastructure Guide

This document provides detailed information about the AWS infrastructure setup for Voice for Bharat.

## Overview

The infrastructure is defined using AWS SAM (Serverless Application Model) and includes:
- 8 DynamoDB tables with On-Demand billing and Point-in-Time Recovery
- 3 S3 buckets with encryption and lifecycle policies
- API Gateway (REST + WebSocket)
- AWS Cognito User Pool for phone number authentication
- ElastiCache Redis cluster for session management
- CloudFront distribution for CDN
- EventBridge event bus for application events
- SNS topics for notifications
- 7 Lambda functions with appropriate IAM roles

## Prerequisites

1. AWS CLI installed and configured
2. AWS SAM CLI installed
3. Python 3.11 installed
4. Valid AWS account with appropriate permissions
5. WhatsApp Business API key (for notifications)

## Infrastructure Components

### DynamoDB Tables (8 tables)

All tables use On-Demand billing, AWS-managed encryption, and Point-in-Time Recovery.

1. **users** - User authentication and profile data
   - Primary Key: userId
   - GSI: phoneNumber-index, state-category-index, cognitoId-index
   - Expected capacity: 10M users

2. **schemes** - Government welfare scheme information
   - Primary Key: schemeId
   - GSI: state-category-index, isActive-lastSyncedAt-index, category-viewCount-index
   - Expected capacity: 5000 schemes

3. **applications** - User applications to schemes
   - Primary Key: applicationId
   - GSI: userId-status-index, schemeId-submittedAt-index, status-updatedAt-index
   - Expected capacity: 50M applications

4. **activity_log** - User activity tracking with 90-day TTL
   - Primary Key: activityId
   - GSI: userId-timestamp-index, type-timestamp-index, schemeId-timestamp-index
   - TTL: 90 days from timestamp

5. **user_profile** - Extended user profile for eligibility matching
   - Primary Key: userId
   - GSI: state-profileStrength-index, educationLevel-annualIncome-index
   - Expected capacity: 10M profiles

6. **helplines** - State-specific helpline information
   - Primary Key: helplineId
   - GSI: state-category-index, isActive-state-index
   - Expected capacity: 500 helplines

7. **guide_content** - FAQ and quick guide content
   - Primary Key: contentId
   - GSI: category-state-priority-index, state-lastUpdatedAt-index, category-viewCount-index
   - Expected capacity: 10,000 content items

8. **suggested_queries** - Suggested voice queries for Assistant tab
   - Primary Key: queryId
   - GSI: state-displayOrder-index, category-popularity-index, isActive-state-index
   - Expected capacity: 1,000 queries

### S3 Buckets (3 buckets)

All buckets use SSE-S3 encryption and block public access.

1. **voice-for-bharat-documents-{env}-{account-id}**
   - Purpose: User-uploaded documents (Aadhaar, PAN, certificates)
   - Encryption: AES-256
   - Versioning: Enabled
   - Lifecycle:
     - Transition to S3-IA after 90 days
     - Transition to Glacier after 365 days
     - Delete after 7 years (2555 days)
   - Structure:
     ```
     users/{userId}/aadhaar/{documentId}.pdf
     users/{userId}/pan/{documentId}.pdf
     applications/{applicationId}/{documentType}/{documentId}.pdf
     ```

2. **voice-for-bharat-audio-{env}-{account-id}**
   - Purpose: Voice recordings and TTS audio files
   - Encryption: AES-256
   - Lifecycle:
     - Delete conversations/ after 30 days
     - Delete tts-cache/ after 90 days
     - Delete stt-recordings/ after 7 days
   - Structure:
     ```
     conversations/{sessionId}/user/{messageId}.wav
     conversations/{sessionId}/assistant/{messageId}.mp3
     tts-cache/{language}/{textHash}.mp3
     stt-recordings/{userId}/{timestamp}.wav
     ```

3. **voice-for-bharat-scheme-dumps-{env}-{account-id}**
   - Purpose: Scheme data backups and dumps
   - Encryption: AES-256
   - Versioning: Enabled
   - Lifecycle:
     - Delete daily/ after 30 days
     - Delete weekly/ after 365 days
     - Archive sources/ to Glacier after 90 days
   - Structure:
     ```
     daily/{date}/schemes.json
     weekly/{week}/schemes-full.json
     sources/{source-name}/{timestamp}.json
     ```

### Cognito User Pool

- **Authentication Method**: Phone number with OTP
- **MFA**: Optional SMS MFA
- **Username Attributes**: phone_number
- **Auto-verified Attributes**: phone_number
- **Custom Attributes**: name, preferred_language
- **Token Validity**:
  - Access Token: 1 hour
  - ID Token: 1 hour
  - Refresh Token: 30 days

### ElastiCache Redis Cluster

- **Engine**: Redis
- **Node Type**: cache.t3.micro (can be scaled up for production)
- **Number of Nodes**: 1
- **Purpose**: Session management for voice conversations
- **VPC**: Private subnets with security group
- **Access**: Lambda functions only (via VPC)

### CloudFront Distribution

- **Purpose**: CDN for audio content delivery
- **Origin**: S3 audio bucket
- **Viewer Protocol**: HTTPS redirect
- **Caching**: Default TTL 24 hours, Max TTL 1 year
- **Compression**: Enabled
- **Price Class**: All edge locations

### API Gateway

1. **REST API** (voice-for-bharat-api-{env})
   - CORS enabled
   - Cognito authorizer (except /register and /verify-otp)
   - Endpoints: User, Scheme, Application, Document, Notification services

2. **WebSocket API** (voice-for-bharat-ws-{env})
   - Real-time voice streaming
   - Route selection: $request.body.action
   - Connected to Voice Service Lambda

### EventBridge

- **Event Bus**: voice-for-bharat-events-{env}
- **Rules**:
  1. ApplicationSubmitted → Notification Service
  2. ApplicationStatusChanged → Notification Service
  3. DocumentVerified → Notification Service

### SNS Topics

1. **voice-for-bharat-notifications-{env}** - Main notification topic
2. **voice-for-bharat-sms-{env}** - SMS notifications
3. **voice-for-bharat-email-{env}** - Email notifications

### Lambda Functions (7 functions)

All functions use Python 3.11 on arm64 (Graviton2) architecture.

1. **UserServiceFunction** (512MB, 30s)
   - Endpoints: /register, /verify-otp, /profile
   - VPC: Yes (for Redis access)

2. **VoiceServiceFunction** (2GB, 300s) - Critical path
   - Endpoints: /voice/query, /voice/session/{id}
   - VPC: Yes (for Redis access)
   - Integrations: Bedrock (Titan STT/TTS, Claude), ElastiCache

3. **SchemeServiceFunction** (1GB, 60s)
   - Endpoints: /schemes, /schemes/{id}, /schemes/{id}/check-eligibility
   - VPC: Yes (for Redis caching)
   - Integrations: Bedrock (embeddings), DynamoDB

4. **ApplicationServiceFunction** (512MB, 60s)
   - Endpoints: /applications, /applications/{id}, /applications/{id}/submit
   - VPC: Yes
   - Integrations: DynamoDB, EventBridge

5. **DocumentServiceFunction** (1GB, 60s)
   - Endpoints: /documents/upload, /documents/{id}
   - VPC: No
   - Integrations: S3, Textract, DynamoDB

6. **NotificationServiceFunction** (512MB, 30s)
   - Endpoints: /notifications/send, /notifications/history
   - VPC: No
   - Integrations: SNS, WhatsApp Business API

7. **SyncServiceFunction** (1GB, 300s)
   - Trigger: Scheduled (daily at 2 AM UTC)
   - VPC: No
   - Integrations: Government APIs, DynamoDB, S3

### VPC and Networking

- **VPC CIDR**: 10.0.0.0/16
- **Private Subnets**:
  - Subnet 1: 10.0.1.0/24 (AZ 1)
  - Subnet 2: 10.0.2.0/24 (AZ 2)
- **Security Groups**:
  - Lambda SG: Allows outbound to Redis
  - Redis SG: Allows inbound from Lambda SG on port 6379

## Deployment Instructions

### Step 1: Set Parameters

Create a `samconfig.toml` file or use command-line parameters:

```toml
version = 0.1
[default.deploy.parameters]
stack_name = "voice-for-bharat-dev"
s3_bucket = "your-sam-deployment-bucket"
s3_prefix = "voice-for-bharat"
region = "us-east-1"
capabilities = "CAPABILITY_NAMED_IAM"
parameter_overrides = [
  "Environment=dev",
  "TablePrefix=voice-for-bharat-dev",
  "WhatsAppApiKey=your-whatsapp-api-key"
]
```

### Step 2: Build the Application

```bash
cd backend
sam build
```

### Step 3: Deploy the Stack

```bash
sam deploy --guided
```

Follow the prompts:
- Stack Name: voice-for-bharat-dev
- AWS Region: us-east-1 (or your preferred region)
- Parameter Environment: dev
- Parameter TablePrefix: voice-for-bharat-dev
- Parameter WhatsAppApiKey: [your-api-key]
- Confirm changes before deploy: Y
- Allow SAM CLI IAM role creation: Y
- Save arguments to configuration file: Y

### Step 4: Verify Deployment

Check the CloudFormation stack status:

```bash
aws cloudformation describe-stacks --stack-name voice-for-bharat-dev
```

Get the outputs:

```bash
aws cloudformation describe-stacks --stack-name voice-for-bharat-dev --query 'Stacks[0].Outputs'
```

### Step 5: Initialize Data

After deployment, you'll need to populate initial data:

1. **Schemes**: Run the sync service manually or wait for scheduled execution
2. **Helplines**: Import helpline data using a script
3. **Guide Content**: Import FAQ and guide content
4. **Suggested Queries**: Import suggested voice queries

## Environment Variables

The following environment variables are automatically set for all Lambda functions:

- `AWS_REGION` - AWS region
- `DYNAMODB_TABLE_PREFIX` - Table name prefix
- `S3_DOCUMENTS_BUCKET` - Documents bucket name
- `S3_AUDIO_BUCKET` - Audio bucket name
- `S3_SCHEME_DUMPS_BUCKET` - Scheme dumps bucket name
- `COGNITO_USER_POOL_ID` - Cognito User Pool ID
- `BEDROCK_REGION` - Bedrock service region
- `WHATSAPP_API_KEY` - WhatsApp Business API key
- `REDIS_ENDPOINT` - Redis cluster endpoint
- `REDIS_PORT` - Redis cluster port
- `CLOUDFRONT_URL` - CloudFront distribution URL
- `SNS_TOPIC_ARN` - Main SNS topic ARN

## Cost Estimation

### Development Environment (Low Traffic)

- DynamoDB: ~$5-10/month (On-Demand)
- S3: ~$5-10/month (storage + requests)
- Lambda: ~$10-20/month (with free tier)
- ElastiCache: ~$15/month (t3.micro)
- API Gateway: ~$5/month (with free tier)
- CloudFront: ~$5/month (with free tier)
- Cognito: Free (up to 50,000 MAUs)
- **Total: ~$45-75/month**

### Production Environment (High Traffic)

- DynamoDB: ~$500-1000/month (On-Demand, 10M users)
- S3: ~$100-200/month (storage + requests)
- Lambda: ~$500-1000/month (millions of invocations)
- ElastiCache: ~$100/month (cache.r6g.large)
- API Gateway: ~$200/month
- CloudFront: ~$100/month
- Cognito: ~$500/month (1M MAUs)
- Bedrock: ~$1000-2000/month (STT/TTS/LLM usage)
- **Total: ~$3000-5000/month**

## Security Best Practices

1. **Encryption**:
   - All DynamoDB tables use AWS-managed encryption
   - All S3 buckets use SSE-S3 encryption
   - All data in transit uses HTTPS/TLS

2. **Access Control**:
   - IAM roles follow least privilege principle
   - S3 buckets block public access
   - API Gateway uses Cognito authorizer
   - VPC security groups restrict Redis access

3. **Data Privacy**:
   - PII fields (Aadhaar, PAN) should be encrypted at application level
   - Activity logs auto-delete after 90 days
   - Audio recordings auto-delete after 7-30 days

4. **Monitoring**:
   - Enable CloudWatch Logs for all Lambda functions
   - Set up CloudWatch Alarms for error rates
   - Enable AWS X-Ray for distributed tracing
   - Monitor DynamoDB throttling and capacity

## Troubleshooting

### Common Issues

1. **Lambda VPC Timeout**:
   - Ensure NAT Gateway is configured for internet access
   - Check security group rules
   - Verify Redis endpoint is accessible

2. **DynamoDB Throttling**:
   - On-Demand mode should auto-scale
   - Check for hot partitions
   - Consider using DAX for caching

3. **S3 Access Denied**:
   - Verify IAM role permissions
   - Check bucket policies
   - Ensure presigned URLs are not expired

4. **Cognito Authentication Errors**:
   - Verify phone number format
   - Check SMS configuration
   - Ensure SNS role is properly configured

## Monitoring and Maintenance

### Daily Tasks
- Monitor Lambda error rates
- Check DynamoDB capacity metrics
- Review CloudWatch Logs for errors

### Weekly Tasks
- Review S3 storage costs
- Check ElastiCache hit rates
- Analyze API Gateway usage patterns

### Monthly Tasks
- Review and optimize Lambda memory allocation
- Analyze DynamoDB access patterns
- Review and update lifecycle policies
- Security audit and compliance check

## Cleanup

To delete the entire stack:

```bash
sam delete --stack-name voice-for-bharat-dev
```

**Warning**: This will delete all resources including data in DynamoDB and S3. Ensure you have backups before proceeding.

## Support

For issues or questions:
1. Check CloudWatch Logs for error details
2. Review AWS CloudFormation events
3. Consult AWS documentation for specific services
4. Contact the development team

## References

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
- [CloudFront with S3](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

## Additional Documentation

- [S3 Bucket Structure and Usage Guide](./S3_BUCKET_GUIDE.md) - Comprehensive guide to S3 bucket structure, policies, and usage
- [S3 Quick Reference](./S3_QUICK_REFERENCE.md) - Quick reference for common S3 operations
- [DynamoDB Schemas](./DYNAMODB_SCHEMAS.md) - Complete DynamoDB table schemas
- [Schema Verification](./SCHEMA_VERIFICATION.md) - Schema validation and verification guide
