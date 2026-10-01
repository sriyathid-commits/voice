# Deploy Voice for Bharat Without AWS CLI

## 🎯 Overview

If you can't install AWS CLI or SAM CLI, you can still deploy using:
1. **AWS Console** (web browser) for backend
2. **Vercel** (web dashboard) for frontend

This method takes longer but doesn't require any local tools.

---

## 📋 Prerequisites

- ✅ AWS Account (free tier available)
- ✅ GitHub account with your code pushed
- ✅ Vercel account (free)
- ✅ Web browser

---

## 🚀 Part 1: Deploy Backend Using AWS Console

### Step 1: Package Lambda Functions Locally

First, create zip files for each Lambda function:

```powershell
# Navigate to backend
cd backend

# Create deployment packages
cd lambdas\user_service
Compress-Archive -Path handler.py,service.py,requirements.txt -DestinationPath user_service.zip -Force

cd ..\voice_service
Compress-Archive -Path handler.py,service.py,models.py,requirements.txt -DestinationPath voice_service.zip -Force

cd ..\scheme_service  
Compress-Archive -Path handler.py,service.py,requirements.txt -DestinationPath scheme_service.zip -Force

cd ..\application_service
Compress-Archive -Path handler.py,requirements.txt -DestinationPath application_service.zip -Force

cd ..\document_service
Compress-Archive -Path handler.py,requirements.txt -DestinationPath document_service.zip -Force

cd ..\notification_service
Compress-Archive -Path handler.py,requirements.txt -DestinationPath notification_service.zip -Force

cd ..\..\..\
```

### Step 2: Create S3 Buckets

1. Go to **S3 Console**: https://console.aws.amazon.com/s3/
2. Click "Create bucket"
3. Create these 3 buckets (replace `123456789` with your AWS account ID):
   - `voice-for-bharat-documents-dev-123456789`
   - `voice-for-bharat-audio-dev-123456789`
   - `voice-for-bharat-scheme-dumps-dev-123456789`
4. For each bucket:
   - Region: `ap-south-1`
   - Enable "Bucket Versioning"
   - Enable "Server-side encryption"
   - Keep "Block all public access" enabled

### Step 3: Create DynamoDB Tables

1. Go to **DynamoDB Console**: https://console.aws.amazon.com/dynamodb/
2. Click "Create table"
3. Create these 8 tables:

**Table 1: users**
- Table name: `voice-for-bharat-dev-users`
- Partition key: `userId` (String)
- Click "Create table"
- After created, go to Indexes → Create Index:
  - Index name: `phoneNumber-index`
  - Partition key: `phoneNumber` (String)

**Table 2: schemes**
- Table name: `voice-for-bharat-dev-schemes`
- Partition key: `schemeId` (String)

**Table 3: applications**
- Table name: `voice-for-bharat-dev-applications`
- Partition key: `applicationId` (String)

**Table 4: activity-log**
- Table name: `voice-for-bharat-dev-activity-log`
- Partition key: `activityId` (String)
- Enable TTL on `ttl` attribute

**Table 5: user-profile**
- Table name: `voice-for-bharat-dev-user-profile`
- Partition key: `userId` (String)

**Table 6: helplines**
- Table name: `voice-for-bharat-dev-helplines`
- Partition key: `helplineId` (String)

**Table 7: guide-content**
- Table name: `voice-for-bharat-dev-guide-content`
- Partition key: `contentId` (String)

**Table 8: suggested-queries**
- Table name: `voice-for-bharat-dev-suggested-queries`
- Partition key: `queryId` (String)

### Step 4: Create Cognito User Pool

1. Go to **Cognito Console**: https://console.aws.amazon.com/cognito/
2. Click "Create user pool"
3. Configure:
   - Sign-in options: Phone number
   - MFA: Optional
   - Auto-verified attributes: Phone number
   - User pool name: `voice-for-bharat-users-dev`
4. Create app client:
   - App client name: `voice-for-bharat-client-dev`
   - Auth flows: ALLOW_USER_SRP_AUTH, ALLOW_REFRESH_TOKEN_AUTH
5. Note the **User Pool ID** and **App Client ID**

### Step 5: Create Lambda Functions

For each Lambda function:

1. Go to **Lambda Console**: https://console.aws.amazon.com/lambda/
2. Click "Create function"
3. Choose "Author from scratch"
4. Function name: `voicebharatai-UserServiceFunction` (repeat for each service)
5. Runtime: Python 3.11
6. Architecture: arm64
7. Click "Create function"
8. Upload the zip file created in Step 1
9. Set Environment Variables:
   ```
   DYNAMODB_TABLE_PREFIX=voice-for-bharat-dev
   S3_DOCUMENTS_BUCKET=voice-for-bharat-documents-dev-123456789
   S3_AUDIO_BUCKET=voice-for-bharat-audio-dev-123456789
   COGNITO_USER_POOL_ID=[Your User Pool ID]
   BEDROCK_REGION=us-east-1
   ```
10. Set Memory: 512 MB (2048 MB for voice_service)
11. Set Timeout: 30 seconds (300 seconds for voice_service)
12. Add IAM permissions:
    - AWSLambdaBasicExecutionRole
    - AmazonDynamoDBFullAccess
    - AmazonS3FullAccess
    - AmazonBedrockFullAccess

Repeat for all 6 Lambda functions:
- UserServiceFunction
- VoiceServiceFunction  
- SchemeServiceFunction
- ApplicationServiceFunction
- DocumentServiceFunction
- NotificationServiceFunction

### Step 6: Create API Gateway

1. Go to **API Gateway Console**: https://console.aws.amazon.com/apigateway/
2. Click "Create API"
3. Choose "REST API" → "Build"
4. API name: `voice-for-bharat-api-dev`
5. Create resources and methods:

**Create /user resource:**
- Click "Create Resource"
- Resource name: `user`
- Create GET method → Link to UserServiceFunction

**Create /schemes resource:**
- Resource name: `schemes`
- Create GET method → Link to SchemeServiceFunction

**Create /voice resource:**
- Resource name: `voice`
- Create POST method → Link to VoiceServiceFunction

**Repeat for:**
- /applications
- /documents
- /notifications

6. Enable CORS on each resource
7. Deploy API:
   - Click "Deploy API"
   - Stage: `dev`
   - Note the **Invoke URL**

---

## 🌐 Part 2: Deploy Frontend to Vercel

This is much easier!

### Step 1: Push Code to GitHub

```powershell
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Import to Vercel

1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Click "Import Git Repository"
4. Select your GitHub repo: `sriyathid-commits/voice`
5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 3: Add Environment Variables

Click "Environment Variables" and add:

```bash
NEXT_PUBLIC_API_URL=https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://[YOUR-WS-ID].execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_COGNITO_USER_POOL_ID=[Your User Pool ID]
NEXT_PUBLIC_COGNITO_CLIENT_ID=[Your App Client ID]
NEXT_PUBLIC_COGNITO_REGION=ap-south-1
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=true
```

Get these values from AWS Console in Step 1.

### Step 4: Deploy

Click "Deploy" and wait 3-5 minutes.

---

## ✅ Verification

### Test Backend

```powershell
# Replace with your API Gateway URL
curl https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev/user/health
```

### Test Frontend

Open your Vercel URL in browser and test:
1. Landing page loads
2. Login flow works
3. Dashboard displays

---

## 💡 Alternative: Use AWS CloudFormation Console

Instead of manually creating resources, you can upload the template.yaml:

1. Go to **CloudFormation Console**: https://console.aws.amazon.com/cloudformation/
2. Click "Create stack" → "With new resources"
3. Choose "Upload a template file"
4. Upload `backend/template.yaml`
5. Follow the wizard
6. This will create ALL resources automatically!

**Recommended!** This is much faster than manual setup.

---

## 🆘 Troubleshooting

### Lambda function times out
- Increase timeout to 60 seconds
- Increase memory to 1024 MB

### API Gateway returns 403
- Check Lambda permissions
- Verify API Gateway resource policies

### Frontend can't connect to backend
- Check CORS settings in API Gateway
- Verify environment variables in Vercel

---

## ⏱️ Time Estimate

**Manual Console Method**: 2-3 hours  
**CloudFormation Upload Method**: 30-40 minutes  
**With AWS CLI (recommended)**: 20-30 minutes

---

## 🎯 Recommendation

If possible, install AWS CLI and SAM CLI. It's much faster and less error-prone.

But if you must use console, follow this guide step by step!
