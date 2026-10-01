# Voice for Bharat - Complete AWS Deployment Guide

## 🎯 Overview
This guide will deploy the complete Voice for Bharat system:
- **Backend**: AWS Lambda (6 services) + DynamoDB + S3 + Cognito + Bedrock
- **Frontend**: Vercel (Next.js with PWA)
- **Total Time**: ~45 minutes

---

## 📋 Prerequisites

### 1. Install AWS CLI
```powershell
# Download AWS CLI v2 for Windows
# Visit: https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify installation
aws --version
# Expected: aws-cli/2.x.x
```

### 2. Install AWS SAM CLI
```powershell
# Download SAM CLI for Windows
# Visit: https://github.com/aws/aws-sam-cli/releases/latest

# Or use Chocolatey
choco install aws-sam-cli

# Verify installation
sam --version
# Expected: SAM CLI, version 1.x.x
```

### 3. Configure AWS Credentials
```powershell
# Configure AWS CLI with your credentials
aws configure

# Enter when prompted:
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]
# Default region name: ap-south-1
# Default output format: json

# Verify configuration
aws sts get-caller-identity
```

### 4. Install Python & Dependencies
```powershell
# Check Python version
python --version
# Required: Python 3.11 or higher

# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Part 1: Deploy Backend to AWS

### Step 1: Configure SAM Deployment
```powershell
cd backend

# Copy example config
Copy-Item samconfig.toml.example samconfig.toml

# Edit samconfig.toml with your details:
# - stack_name: voicebharatai
# - region: ap-south-1
# - s3_bucket: voice-for-bharat-sam-artifacts-[YOUR-ACCOUNT-ID]
```

### Step 2: Build Lambda Functions
```powershell
# Build all Lambda functions
sam build

# This will:
# ✓ Install Python dependencies for each Lambda
# ✓ Package code and dependencies
# ✓ Prepare for deployment
# Time: ~5 minutes
```

### Step 3: Deploy to AWS
```powershell
# Deploy the stack
sam deploy --guided

# Answer the prompts:
# Stack Name: voicebharatai
# AWS Region: ap-south-1
# Parameter Environment: dev
# Parameter TablePrefix: voice-for-bharat-dev
# Parameter WhatsAppApiKey: [Your WhatsApp API Key or leave blank]
# Confirm changes before deploy: Y
# Allow SAM CLI IAM role creation: Y
# Disable rollback: N
# Save arguments to configuration file: Y

# Deployment time: ~20-30 minutes
```

### Step 4: Get API Endpoints
```powershell
# Get API Gateway endpoints
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs"

# Note down these URLs:
# - VoiceForBharatApiUrl (REST API)
# - VoiceWebSocketApiUrl (WebSocket)
# - CloudFrontURL (CDN)
```

### Step 5: Verify Backend Deployment
```powershell
# Test health endpoint
curl https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev/health

# Expected: {"status": "healthy", "service": "api-gateway"}
```

---

## 🌐 Part 2: Deploy Frontend to Vercel

### Step 1: Push Code to GitHub
```powershell
# Navigate to project root
cd c:\Users\yathi\voice

# Check git status
git status

# Add all files
git add .

# Commit
git commit -m "Complete AWS integration - ready for deployment"

# Push to GitHub
git push origin main
```

### Step 2: Import to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Click **"Import Git Repository"**
4. Select your GitHub repository: `sriyathid-commits/voice`
5. Click **"Import"**

### Step 3: Configure Vercel Project
**Framework Preset**: Next.js (auto-detected)

**Root Directory**: 
```
frontend/web
```

**Build Command**: 
```bash
npm run build
```

**Output Directory**: 
```
.next
```

**Install Command**:
```bash
npm install
```

### Step 4: Add Environment Variables
In Vercel project settings, add these environment variables:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://[YOUR-WS-ID].execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL=https://[YOUR-CLOUDFRONT-ID].cloudfront.net

# AWS Cognito
NEXT_PUBLIC_COGNITO_USER_POOL_ID=[YOUR-USER-POOL-ID]
NEXT_PUBLIC_COGNITO_CLIENT_ID=[YOUR-CLIENT-ID]
NEXT_PUBLIC_COGNITO_REGION=ap-south-1

# Feature Flags
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=true
```

**How to get these values:**
```powershell
# Get Cognito User Pool ID
aws cognito-idp list-user-pools --max-results 10 --region ap-south-1

# Get Cognito Client ID
aws cognito-idp list-user-pool-clients --user-pool-id [YOUR-POOL-ID] --region ap-south-1
```

### Step 5: Deploy Frontend
1. Click **"Deploy"** in Vercel
2. Wait for build to complete (~3-5 minutes)
3. Once deployed, you'll get a URL like: `voice-for-bharat.vercel.app`

---

## ✅ Part 3: Verification & Testing

### 1. Test Backend APIs
```powershell
# Test user service
curl https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev/user/health

# Test schemes service
curl https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev/schemes?limit=5

# Test voice service
curl https://[YOUR-API-ID].execute-api.ap-south-1.amazonaws.com/dev/voice/health
```

### 2. Test Frontend
1. Open your Vercel URL: `https://voice-for-bharat.vercel.app`
2. Click **"Get Started"**
3. Try login flow (enter phone number)
4. Navigate through dashboard tabs
5. Test voice assistant (allow microphone access)

### 3. Test End-to-End Flow
1. **Register**: Enter Indian phone number (+919999999999)
2. **Verify OTP**: Check console for OTP (dev mode)
3. **Complete Profile**: Fill personal details
4. **Browse Schemes**: Filter by state (Karnataka)
5. **Voice Search**: Ask "What schemes are available for farmers?"
6. **Apply**: Submit an application with documents

### 4. Monitor AWS Resources
```powershell
# Check Lambda function logs
aws logs tail /aws/lambda/voicebharatai-UserServiceFunction --follow --region ap-south-1

# Check DynamoDB tables
aws dynamodb list-tables --region ap-south-1

# Check S3 buckets
aws s3 ls | findstr voice-for-bharat
```

---

## 🔧 Part 4: Post-Deployment Configuration

### 1. Enable Bedrock Models
```powershell
# Enable Claude 3 Sonnet
aws bedrock list-foundation-models --region us-east-1 --by-provider anthropic

# Enable Amazon Titan
aws bedrock list-foundation-models --region us-east-1 --by-provider amazon

# Request model access in AWS Console:
# https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess
```

### 2. Configure CORS for API Gateway
```powershell
# Update API Gateway CORS to include Vercel domain
# In AWS Console: API Gateway → voicebharatai-api → CORS settings
# Add: https://voice-for-bharat.vercel.app
```

### 3. Set up Custom Domain (Optional)
**For Frontend (Vercel)**:
1. Go to Vercel Project → Settings → Domains
2. Add your domain: `voiceforbharat.com`
3. Update DNS records as instructed

**For Backend (API Gateway)**:
1. Request SSL certificate in ACM
2. Create custom domain in API Gateway
3. Map to your API: `api.voiceforbharat.com`

### 4. Enable CloudWatch Monitoring
```powershell
# Create CloudWatch dashboard
aws cloudwatch put-dashboard --dashboard-name VoiceForBharat --dashboard-body file://cloudwatch-dashboard.json --region ap-south-1
```

---

## 📊 Cost Estimation

### AWS Monthly Costs (Estimated)
- **Lambda**: $5-20 (based on 100K requests/month)
- **DynamoDB**: $5-15 (On-Demand pricing)
- **S3**: $2-10 (based on storage)
- **API Gateway**: $3-10 (based on requests)
- **Cognito**: $0 (50K MAU free)
- **Bedrock**: $20-100 (based on usage)
- **CloudFront**: $1-5 (based on traffic)
- **ElastiCache**: $12-30 (t3.micro)

**Total**: ~$50-200/month (depending on usage)

### Vercel Costs
- **Hobby Plan**: $0 (free for personal projects)
- **Pro Plan**: $20/month (for production use)

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: SAM build fails**
```powershell
# Clear build cache
Remove-Item -Recurse -Force .aws-sam

# Rebuild
sam build --use-container
```

**Issue: Lambda timeout**
```powershell
# Increase timeout in template.yaml
# Change Timeout from 30 to 60 seconds
# Redeploy: sam build && sam deploy
```

**Issue: DynamoDB access denied**
```powershell
# Check Lambda execution role has DynamoDB permissions
aws iam get-role-policy --role-name voicebharatai-UserServiceRole --policy-name DynamoDBPolicy --region ap-south-1
```

### Frontend Issues

**Issue: Environment variables not working**
- Variables must start with `NEXT_PUBLIC_`
- Redeploy after adding variables
- Check Vercel deployment logs

**Issue: API calls failing (CORS)**
```powershell
# Update API Gateway CORS settings
# Add your Vercel domain to allowed origins
```

**Issue: Build fails on Vercel**
```powershell
# Test build locally
cd frontend/web
npm run build

# Check for TypeScript errors
npm run type-check
```

### Voice Service Issues

**Issue: Bedrock access denied**
- Enable model access in Bedrock console
- Check Lambda has Bedrock invoke permissions
- Verify region (Bedrock may not be in ap-south-1)

---

## 📱 Mobile Deployment (Future)

### React Native App
```powershell
# For iOS
cd frontend/mobile
npm install
npx pod-install
npm run ios

# For Android
npm run android
```

---

## 🔒 Security Checklist

- [ ] API Gateway has authentication enabled
- [ ] S3 buckets have encryption enabled
- [ ] DynamoDB has Point-in-Time Recovery enabled
- [ ] Lambda functions use IAM roles (not access keys)
- [ ] Cognito has MFA enabled
- [ ] CloudFront uses HTTPS only
- [ ] Environment variables are not committed to Git
- [ ] WhatsApp API key is stored in AWS Secrets Manager

---

## 🎉 Success Criteria

Your deployment is successful when:
1. ✅ All Lambda functions return 200 on health checks
2. ✅ Frontend loads on Vercel URL
3. ✅ User can register with OTP
4. ✅ Schemes are searchable and filterable
5. ✅ Voice assistant responds to queries
6. ✅ Documents can be uploaded
7. ✅ Applications can be submitted
8. ✅ No console errors in browser

---

## 📞 Support Resources

- **AWS Support**: https://console.aws.amazon.com/support/
- **Vercel Support**: https://vercel.com/support
- **Bedrock Documentation**: https://docs.aws.amazon.com/bedrock/
- **SAM Documentation**: https://docs.aws.amazon.com/serverless-application-model/

---

## 🚀 Quick Deploy Commands

```powershell
# Backend deployment (one command)
cd backend ; sam build ; sam deploy

# Frontend deployment (push to GitHub)
cd .. ; git add . ; git commit -m "Deploy" ; git push origin main

# Verification
curl https://[API-ID].execute-api.ap-south-1.amazonaws.com/dev/health
```

---

**Next Steps**: 
1. Follow Part 1 to deploy backend
2. Follow Part 2 to deploy frontend
3. Run verification tests
4. Share your live URL! 🎊
