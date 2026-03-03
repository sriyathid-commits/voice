# AWS Console - View Your Deployed Services

## 🔐 Login to AWS Console

**URL**: https://console.aws.amazon.com/

**Region**: Make sure you're in **ap-south-1 (Mumbai)** - Check top right corner!

---

## 📋 Quick Links to Your Services

### 1. CloudFormation Stack (Overview of Everything)
**URL**: https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks

**What to see:**
- Stack Name: `voicebharatai`
- Status: `CREATE_COMPLETE` ✅
- Click on stack → "Resources" tab to see all 50+ resources

---

### 2. Lambda Functions (7 Services)
**URL**: https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions

**Your Functions:**
```
voicebharatai-UserService-xxxxx
voicebharatai-VoiceService-xxxxx (2GB memory, 300s timeout)
voicebharatai-SchemeService-xxxxx
voicebharatai-ApplicationService-xxxxx
voicebharatai-DocumentService-xxxxx
voicebharatai-NotificationService-xxxxx
voicebharatai-SyncService-xxxxx
```

**What to check:**
- Click any function → "Configuration" tab
- See memory, timeout, environment variables
- "Monitor" tab → CloudWatch logs

---

### 3. API Gateway (REST + WebSocket)
**URL**: https://ap-south-1.console.aws.amazon.com/apigateway/main/apis?region=ap-south-1

**Your APIs:**
- **REST API**: `voicebharatai-api` 
  - ID: `2dbyh0kkna`
  - Stage: `dev`
  - Invoke URL: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev

- **WebSocket API**: `voicebharatai-websocket`
  - ID: `be6zdvjoy2`
  - Stage: `dev`
  - Invoke URL: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev

**What to check:**
- Click API → "Stages" → "dev"
- See all endpoints and methods
- "Logs" tab for request logs

---

### 4. DynamoDB Tables (8 Tables)
**URL**: https://ap-south-1.console.aws.amazon.com/dynamodbv2/home?region=ap-south-1#tables

**Your Tables:**
```
voicebharatai-users
voicebharatai-schemes
voicebharatai-applications
voicebharatai-activity_log (with TTL)
voicebharatai-user_profile
voicebharatai-documents
voicebharatai-notifications
voicebharatai-sync_status
```

**What to check:**
- Click any table → "Explore table items" to see data
- "Additional settings" → See encryption, PITR enabled
- "Indexes" tab → See GSIs (Global Secondary Indexes)

---

### 5. S3 Buckets (3 Buckets)
**URL**: https://s3.console.aws.amazon.com/s3/buckets?region=ap-south-1

**Your Buckets:**
```
voice-for-bharat-documents-xxxxx
voice-for-bharat-audio-xxxxx
voice-for-bharat-scheme-dumps-xxxxx
```

**What to check:**
- Click bucket → "Properties" tab
- See encryption (SSE-S3)
- "Management" tab → Lifecycle rules
- "Permissions" tab → Bucket policies

---

### 6. CloudFront Distribution
**URL**: https://console.aws.amazon.com/cloudfront/v3/home?region=ap-south-1#/distributions

**Your Distribution:**
- Domain: `d18s1aceaoasx3.cloudfront.net`
- Status: `Deployed` ✅
- Origin: S3 buckets

**What to check:**
- Click distribution → See origins
- "Behaviors" tab → Cache settings
- "Monitoring" tab → Request metrics

---

### 7. Cognito User Pool
**URL**: https://ap-south-1.console.aws.amazon.com/cognito/v2/idp/user-pools?region=ap-south-1

**Your User Pool:**
- Pool ID: `ap-south-1_lbk6t80Qf`
- App Client ID: `78d8776ct03jlp6n5heqic32gn`

**What to check:**
- Click pool → "Users" tab (see registered users)
- "App integration" → App clients
- "Sign-in experience" → Authentication flows

---

### 8. ElastiCache (Redis)
**URL**: https://ap-south-1.console.aws.amazon.com/elasticache/home?region=ap-south-1#/redis

**Your Cache:**
- Cluster: `voice-for-bharat-cache`
- Node Type: `cache.t3.micro`
- Engine: Redis

**What to check:**
- Click cluster → See endpoint
- "Metrics" tab → Cache hit/miss rates
- "Nodes" tab → Node status

---

### 9. EventBridge
**URL**: https://ap-south-1.console.aws.amazon.com/events/home?region=ap-south-1#/eventbuses

**What to check:**
- Default event bus
- Rules for application events
- Targets (Lambda functions, SNS)

---

### 10. SNS Topics
**URL**: https://ap-south-1.console.aws.amazon.com/sns/v3/home?region=ap-south-1#/topics

**Your Topics:**
- Notification topics for SMS, Email, Push

**What to check:**
- Click topic → "Subscriptions"
- See delivery status

---

### 11. SQS Queues
**URL**: https://ap-south-1.console.aws.amazon.com/sqs/v2/home?region=ap-south-1#/queues

**Your Queues:**
- Document processing queue
- Notification queue

**What to check:**
- Messages available
- Messages in flight
- Queue attributes

---

### 12. CloudWatch Logs
**URL**: https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups

**Your Log Groups:**
```
/aws/lambda/voicebharatai-UserService-xxxxx
/aws/lambda/voicebharatai-VoiceService-xxxxx
/aws/lambda/voicebharatai-SchemeService-xxxxx
... (one for each Lambda)
```

**What to check:**
- Click log group → "Log streams"
- See recent invocations
- Search logs for errors

---

### 13. IAM Roles
**URL**: https://console.aws.amazon.com/iam/home?region=ap-south-1#/roles

**Your Roles:**
- Lambda execution roles (one per function)
- API Gateway role
- CloudFormation role

**What to check:**
- Click role → "Permissions" tab
- See attached policies
- "Trust relationships" tab

---

## 🎯 Quick Verification Commands

### Test REST API
```bash
# In PowerShell
curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health
```

### List Lambda Functions
```bash
python -m awscli lambda list-functions --region ap-south-1 --query "Functions[?contains(FunctionName, 'voicebharatai')].FunctionName"
```

### List DynamoDB Tables
```bash
python -m awscli dynamodb list-tables --region ap-south-1 --query "TableNames[?contains(@, 'voicebharatai')]"
```

### List S3 Buckets
```bash
python -m awscli s3 ls | findstr voice-for-bharat
```

---

## 📊 Cost Monitoring

### View Current Costs
**URL**: https://console.aws.amazon.com/billing/home?region=ap-south-1#/bills

**What to check:**
- Current month charges
- Service breakdown
- Free tier usage

### Set Up Billing Alerts
**URL**: https://console.aws.amazon.com/billing/home?region=ap-south-1#/budgets

**Recommended:**
- Create budget alert for $10/month
- Get email when 80% threshold reached

---

## 🔍 Troubleshooting

### If You Don't See Resources:
1. **Check Region**: Must be in `ap-south-1 (Mumbai)`
2. **Check Stack Status**: CloudFormation → `voicebharatai` → Status
3. **Check Permissions**: Make sure you're logged in with correct AWS account

### Common Issues:
- **"Access Denied"**: IAM permissions issue
- **"Resource Not Found"**: Wrong region selected
- **"Stack Failed"**: Check CloudFormation events tab

---

## 📸 Screenshots for Hackathon

Take screenshots of:
1. ✅ CloudFormation stack (Resources tab)
2. ✅ Lambda functions list
3. ✅ DynamoDB tables list
4. ✅ API Gateway endpoints
5. ✅ S3 buckets
6. ✅ CloudWatch logs showing invocations

This proves your infrastructure is actually deployed! 🚀

---

## 🎓 For Presentation

**Show judges:**
1. CloudFormation stack with 50+ resources
2. Lambda functions with proper configuration
3. DynamoDB tables with data
4. API Gateway with live endpoints
5. CloudWatch logs showing activity

**This demonstrates:**
- Production-ready infrastructure
- Professional AWS architecture
- Scalable serverless design
- Real deployment (not just localhost)
