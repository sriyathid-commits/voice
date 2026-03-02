# Deployment Guide - Voice for Bharat Backend

This guide covers the deployment process for the Voice for Bharat backend Lambda services.

## Prerequisites

Before deploying, ensure you have:

- [ ] AWS Account with appropriate permissions
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] SAM CLI installed (`pip install aws-sam-cli`)
- [ ] Python 3.11 installed
- [ ] Access to the following AWS services:
  - Lambda
  - API Gateway
  - DynamoDB
  - S3
  - Cognito
  - Bedrock
  - CloudWatch
  - IAM

## Pre-Deployment Checklist

### 1. Infrastructure Setup

Ensure the following resources are created before deploying Lambda functions:

- [ ] DynamoDB tables (8 tables):
  - `{prefix}-users`
  - `{prefix}-schemes`
  - `{prefix}-applications`
  - `{prefix}-activity_log`
  - `{prefix}-user_profile`
  - `{prefix}-helplines`
  - `{prefix}-guide_content`
  - `{prefix}-suggested_queries`

- [ ] S3 buckets (3 buckets):
  - `voice-for-bharat-documents-{env}`
  - `voice-for-bharat-audio-{env}`
  - `voice-for-bharat-scheme-dumps-{env}`

- [ ] Cognito User Pool configured with:
  - Phone number authentication
  - OTP verification
  - Custom Lambda triggers (optional)

- [ ] ElastiCache Redis cluster (optional, for session management)

- [ ] CloudFront distribution (for CDN)

### 2. Environment Configuration

Create a `samconfig.toml` file from the example:

```bash
cp samconfig.toml.example samconfig.toml
```

Update the following parameters:
- `CognitoUserPoolId`: Your Cognito User Pool ID
- `DocumentsBucket`: S3 bucket name for documents
- `AudioBucket`: S3 bucket name for audio files
- `SchemeDumpsBucket`: S3 bucket name for scheme dumps
- `TablePrefix`: DynamoDB table prefix

### 3. Dependencies

Install all dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Deployment Steps

### Step 1: Build the Application

Build all Lambda functions:

```bash
sam build
```

This will:
- Package each Lambda function
- Install dependencies
- Prepare deployment artifacts

### Step 2: Validate the Template

Validate the SAM template:

```bash
sam validate
```

### Step 3: Deploy to Development

For first-time deployment:

```bash
sam deploy --guided
```

Follow the prompts:
1. Stack Name: `voice-for-bharat-backend-dev`
2. AWS Region: `ap-south-1`
3. Parameter Environment: `dev`
4. Confirm changes before deploy: `Y`
5. Allow SAM CLI IAM role creation: `Y`
6. Save arguments to configuration file: `Y`

For subsequent deployments:

```bash
sam deploy
```

### Step 4: Deploy to Staging

```bash
sam deploy --config-env staging
```

### Step 5: Deploy to Production

```bash
sam deploy --config-env production
```

## Post-Deployment Verification

### 1. Check Lambda Functions

Verify all 7 Lambda functions are deployed:

```bash
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `voice-for-bharat`)].FunctionName'
```

Expected output:
- `voice-for-bharat-user-service-{env}`
- `voice-for-bharat-voice-service-{env}`
- `voice-for-bharat-scheme-service-{env}`
- `voice-for-bharat-application-service-{env}`
- `voice-for-bharat-document-service-{env}`
- `voice-for-bharat-notification-service-{env}`
- `voice-for-bharat-sync-service-{env}`

### 2. Test API Endpoints

Get the API Gateway endpoint:

```bash
aws cloudformation describe-stacks \
  --stack-name voice-for-bharat-backend-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text
```

Test health endpoints:

```bash
API_ENDPOINT="<your-api-endpoint>"

# User Service
curl $API_ENDPOINT/health

# Scheme Service
curl $API_ENDPOINT/health

# Voice Service
curl $API_ENDPOINT/health
```

### 3. Check CloudWatch Logs

Verify logs are being created:

```bash
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/voice-for-bharat
```

### 4. Test WebSocket Connection

Get the WebSocket endpoint:

```bash
aws cloudformation describe-stacks \
  --stack-name voice-for-bharat-backend-dev \
  --query 'Stacks[0].Outputs[?OutputKey==`WebSocketEndpoint`].OutputValue' \
  --output text
```

## Monitoring

### CloudWatch Dashboards

Create a CloudWatch dashboard to monitor:
- Lambda invocations
- Error rates
- Duration metrics
- Throttles
- Concurrent executions

### CloudWatch Alarms

Set up alarms for:
- High error rate (> 5%)
- High duration (> 80% of timeout)
- Throttling events
- DynamoDB throttling

### X-Ray Tracing

Enable X-Ray tracing for distributed tracing:

```bash
aws lambda update-function-configuration \
  --function-name voice-for-bharat-voice-service-dev \
  --tracing-config Mode=Active
```

## Rollback

If deployment fails or issues are detected:

### Option 1: Rollback via CloudFormation

```bash
aws cloudformation cancel-update-stack \
  --stack-name voice-for-bharat-backend-dev
```

### Option 2: Deploy Previous Version

```bash
# Get previous version
aws lambda list-versions-by-function \
  --function-name voice-for-bharat-user-service-dev

# Update alias to previous version
aws lambda update-alias \
  --function-name voice-for-bharat-user-service-dev \
  --name live \
  --function-version <previous-version>
```

## Troubleshooting

### Issue: Lambda Timeout

**Solution**: Increase timeout in `template.yaml`:

```yaml
Timeout: 300  # Increase as needed
```

### Issue: Memory Limit Exceeded

**Solution**: Increase memory in `template.yaml`:

```yaml
MemorySize: 2048  # Increase as needed
```

### Issue: Permission Denied

**Solution**: Check IAM role has required permissions:

```bash
aws iam get-role-policy \
  --role-name voice-for-bharat-lambda-role-dev \
  --policy-name DynamoDBAccess
```

### Issue: Cold Start Latency

**Solutions**:
- Use arm64 architecture (already configured)
- Reduce package size
- Enable provisioned concurrency for critical functions:

```bash
aws lambda put-provisioned-concurrency-config \
  --function-name voice-for-bharat-voice-service-dev \
  --provisioned-concurrent-executions 5 \
  --qualifier live
```

### Issue: API Gateway 502 Error

**Causes**:
- Lambda timeout
- Lambda error
- Integration timeout

**Solution**: Check CloudWatch Logs:

```bash
aws logs tail /aws/lambda/voice-for-bharat-user-service-dev --follow
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy-backend.yml`:

```yaml
name: Deploy Backend

on:
  push:
    branches:
      - main
      - staging
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Setup SAM CLI
        uses: aws-actions/setup-sam@v2
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
      
      - name: SAM Build
        run: sam build
      
      - name: SAM Deploy
        run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

## Security Best Practices

1. **Secrets Management**: Use AWS Secrets Manager for sensitive data
2. **Encryption**: Enable encryption at rest for all data
3. **IAM Roles**: Follow least privilege principle
4. **API Keys**: Rotate API keys regularly
5. **VPC**: Deploy Lambda functions in VPC for sensitive operations
6. **WAF**: Enable AWS WAF for API Gateway

## Cost Optimization

1. **Right-size Memory**: Monitor and adjust Lambda memory allocation
2. **Reserved Concurrency**: Set limits to prevent runaway costs
3. **S3 Lifecycle**: Configure lifecycle policies for old data
4. **DynamoDB**: Use On-Demand billing for variable workloads
5. **CloudWatch Logs**: Set retention periods appropriately

## Support

For deployment issues:
1. Check CloudWatch Logs
2. Review SAM CLI output
3. Verify IAM permissions
4. Check AWS service quotas
5. Contact AWS Support if needed

## Next Steps

After successful deployment:
1. Configure frontend to use API endpoints
2. Set up monitoring and alerting
3. Perform load testing
4. Configure auto-scaling policies
5. Set up backup and disaster recovery
