# AWS Development Guide - Voice for Bharat

Quick start guide for developing and deploying Voice for Bharat on AWS.

## 🚀 Quick Start (5 Minutes)

### Prerequisites

```bash
# Install AWS CLI
pip install awscli

# Install SAM CLI
pip install aws-sam-cli

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (ap-south-1), Output format (json)
```

### Deploy Backend

```bash
cd backend

# Build
sam build

# Deploy (first time)
sam deploy --guided

# Follow prompts:
# Stack Name: voice-for-bharat-dev
# Region: ap-south-1
# Environment: dev
# Confirm changes: Y
# Allow IAM role creation: Y
# Save config: Y

# Subsequent deploys
sam deploy
```

### Get API Endpoint

```bash
aws cloudformation describe-stacks \
  --stack-name voice-for-bharat-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text
```

## 📋 Development Workflow

### 1. Local Development

```bash
# Backend - Test Lambda locally
cd backend
sam local start-api --port 3001

# Frontend - Run Next.js dev server
cd frontend/web
npm run dev
```

### 2. Test Endpoints Locally

```bash
# User Service
curl http://localhost:3001/health

# Register user
curl -X POST http://localhost:3001/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210", "language": "en"}'
```

### 3. Deploy Changes

```bash
# Build and deploy
cd backend
sam build && sam deploy

# Or deploy specific function
sam build UserServiceFunction
sam deploy --no-confirm-changeset
```

### 4. View Logs

```bash
# Tail logs in real-time
sam logs -n UserServiceFunction --stack-name voice-for-bharat-dev --tail

# Or use AWS CLI
aws logs tail /aws/lambda/voice-for-bharat-user-service-dev --follow
```

## 🔧 AWS Services Setup

### 1. DynamoDB Tables

```bash
# Create tables using script
cd backend/scripts
python manage_tables.py --action create --environment dev

# Or deploy via SAM (recommended)
sam deploy
```

### 2. S3 Buckets

```bash
# Setup S3 buckets
cd backend/scripts
python setup_s3_buckets.py --environment dev

# Verify
python setup_s3_buckets.py --environment dev --verify-only
```

### 3. Cognito User Pool

```bash
# Get Cognito User Pool ID from CloudFormation
aws cloudformation describe-stacks \
  --stack-name voice-for-bharat-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`CognitoUserPoolId`].OutputValue' \
  --output text
```

### 4. Bedrock Access

```bash
# Request Bedrock model access (one-time)
# Go to AWS Console → Bedrock → Model access
# Request access to:
# - Amazon Titan (Text, Embeddings, Multimodal)
# - Anthropic Claude 3 Sonnet

# Verify access
aws bedrock list-foundation-models --region ap-south-1
```

## 🧪 Testing

### Unit Tests

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend/web
npm test
```

### Integration Tests

```bash
# Test deployed API
export API_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name voice-for-bharat-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text)

# Test user registration
curl -X POST $API_ENDPOINT/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210", "language": "en"}'

# Test scheme search
curl "$API_ENDPOINT/schemes?state=KA&category=agriculture&language=en"
```

### Load Testing

```bash
# Install artillery
npm install -g artillery

# Run load test
artillery quick --count 100 --num 10 $API_ENDPOINT/health
```

## 📊 Monitoring

### CloudWatch Dashboard

```bash
# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name voice-for-bharat-dev \
  --dashboard-body file://cloudwatch-dashboard.json
```

### View Metrics

```bash
# Lambda invocations
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=voice-for-bharat-user-service-dev \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum

# Error rate
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=voice-for-bharat-user-service-dev \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## 🔐 Security

### IAM Roles

```bash
# View Lambda execution role
aws iam get-role \
  --role-name voice-for-bharat-lambda-role-dev

# List attached policies
aws iam list-attached-role-policies \
  --role-name voice-for-bharat-lambda-role-dev
```

### Secrets Management

```bash
# Store WhatsApp API key
aws secretsmanager create-secret \
  --name voice-for-bharat/whatsapp-api-key \
  --secret-string "your-api-key"

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id voice-for-bharat/whatsapp-api-key \
  --query SecretString \
  --output text
```

## 💰 Cost Management

### View Costs

```bash
# Get cost for last 30 days
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --filter file://cost-filter.json
```

### Set Budget Alerts

```bash
# Create budget
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## 🐛 Debugging

### Common Issues

**1. Lambda Timeout**
```bash
# Increase timeout
aws lambda update-function-configuration \
  --function-name voice-for-bharat-voice-service-dev \
  --timeout 300
```

**2. Memory Issues**
```bash
# Increase memory
aws lambda update-function-configuration \
  --function-name voice-for-bharat-voice-service-dev \
  --memory-size 2048
```

**3. Permission Errors**
```bash
# Check CloudWatch Logs
aws logs tail /aws/lambda/voice-for-bharat-user-service-dev --follow

# Check IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT_ID:role/voice-for-bharat-lambda-role-dev \
  --action-names dynamodb:PutItem \
  --resource-arns arn:aws:dynamodb:ap-south-1:ACCOUNT_ID:table/voice-for-bharat-dev-users
```

**4. Cold Start Issues**
```bash
# Enable provisioned concurrency
aws lambda put-provisioned-concurrency-config \
  --function-name voice-for-bharat-voice-service-dev \
  --provisioned-concurrent-executions 2 \
  --qualifier $LATEST
```

## 🔄 CI/CD

### GitHub Actions Setup

1. Add AWS credentials to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

2. Push to trigger deployment:
```bash
git add .
git commit -m "Deploy to AWS"
git push origin main
```

### Manual Deployment

```bash
# Build
sam build

# Deploy to dev
sam deploy --config-env dev

# Deploy to staging
sam deploy --config-env staging

# Deploy to production
sam deploy --config-env production
```

## 📚 Useful Commands

### Lambda

```bash
# List functions
aws lambda list-functions --query 'Functions[].FunctionName'

# Invoke function
aws lambda invoke \
  --function-name voice-for-bharat-user-service-dev \
  --payload '{"httpMethod": "GET", "path": "/health"}' \
  response.json

# Update environment variables
aws lambda update-function-configuration \
  --function-name voice-for-bharat-user-service-dev \
  --environment Variables={KEY=VALUE}
```

### DynamoDB

```bash
# List tables
aws dynamodb list-tables

# Describe table
aws dynamodb describe-table --table-name voice-for-bharat-dev-users

# Query table
aws dynamodb query \
  --table-name voice-for-bharat-dev-users \
  --key-condition-expression "userId = :id" \
  --expression-attribute-values '{":id":{"S":"user-123"}}'
```

### S3

```bash
# List buckets
aws s3 ls

# Upload file
aws s3 cp document.pdf s3://voice-for-bharat-documents-dev/users/user-123/aadhaar/

# Generate presigned URL
aws s3 presign s3://voice-for-bharat-documents-dev/users/user-123/aadhaar/doc.pdf --expires-in 900
```

### API Gateway

```bash
# Get API ID
aws apigateway get-rest-apis --query 'items[?name==`voice-for-bharat-api-dev`].id' --output text

# Get stages
aws apigateway get-stages --rest-api-id <api-id>

# Enable logging
aws apigateway update-stage \
  --rest-api-id <api-id> \
  --stage-name prod \
  --patch-operations op=replace,path=/accessLogSettings/destinationArn,value=<log-group-arn>
```

## 🎯 Next Steps

1. **Deploy Infrastructure**: `sam deploy --guided`
2. **Verify Deployment**: Check all Lambda functions and API endpoints
3. **Test APIs**: Use Postman or curl to test endpoints
4. **Setup Monitoring**: Create CloudWatch dashboards and alarms
5. **Configure Frontend**: Update frontend with API endpoints
6. **Load Test**: Run load tests to verify performance
7. **Go Live**: Deploy to production environment

## 📞 Support

- AWS Documentation: https://docs.aws.amazon.com/
- SAM CLI Docs: https://docs.aws.amazon.com/serverless-application-model/
- Bedrock Docs: https://docs.aws.amazon.com/bedrock/
- Project Issues: Check CloudWatch Logs and X-Ray traces

## 🔗 Quick Links

- [Backend README](backend/README.md)
- [Deployment Guide](backend/DEPLOYMENT.md)
- [Infrastructure Guide](backend/INFRASTRUCTURE.md)
- [DynamoDB Schemas](backend/docs/DYNAMODB_SCHEMAS.md)
- [S3 Bucket Guide](backend/docs/S3_BUCKET_GUIDE.md)
