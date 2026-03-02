# 🇮🇳 Voice for Bharat - Live Deployment Links

## 🚀 Production Deployment URLs

### 📋 GitHub Repository Setup
```
https://github.com/new
```

### 🌐 Vercel Deployment
```
https://vercel.com/new
```

### ☁️ AWS Console (Monitor Backend)
```
https://console.aws.amazon.com/
```

## 🔗 Your Live Backend APIs (Already Deployed)

### REST API Endpoint
```
https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
```

### WebSocket API Endpoint
```
wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
```

### CloudFront CDN
```
https://d18s1aceaoasx3.cloudfront.net
```

### API Health Check
```
https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health
```

## 🔧 AWS Management Console Links

### Lambda Functions
```
https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions
```

### DynamoDB Tables
```
https://ap-south-1.console.aws.amazon.com/dynamodbv2/home?region=ap-south-1#tables
```

### S3 Buckets
```
https://s3.console.aws.amazon.com/s3/home?region=ap-south-1
```

### CloudWatch Logs
```
https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups
```

### API Gateway
```
https://ap-south-1.console.aws.amazon.com/apigateway/main/apis?region=ap-south-1
```

### Cognito User Pools
```
https://ap-south-1.console.aws.amazon.com/cognito/v2/idp/user-pools?region=ap-south-1
```

## 📊 Monitoring & Analytics

### AWS CloudWatch Dashboard
```
https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#dashboards:
```

### AWS Cost Explorer
```
https://console.aws.amazon.com/cost-management/home#/cost-explorer
```

### Vercel Analytics (After Deployment)
```
https://vercel.com/dashboard/analytics
```

## 🛠️ Development Tools

### GitHub Desktop (Alternative to Git CLI)
```
https://desktop.github.com/
```

### VS Code (Code Editor)
```
https://code.visualstudio.com/
```

### Postman (API Testing)
```
https://www.postman.com/downloads/
```

## 📱 Your Frontend URLs (After Deployment)

### Local Development
```
http://localhost:3000
```

### Production (Will be available after Vercel deployment)
```
https://voice-for-bharat-[random].vercel.app
```

### Custom Domain (Optional - Configure in Vercel)
```
https://voiceforbharat.com
```

## 🔐 Environment Variables for Vercel

```
NEXT_PUBLIC_API_URL=https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL=https://d18s1aceaoasx3.cloudfront.net
NEXT_PUBLIC_COGNITO_USER_POOL_ID=ap-south-1_lbk6t80Qf
NEXT_PUBLIC_COGNITO_CLIENT_ID=78d8776ct03jlp6n5heqic32gn
NEXT_PUBLIC_COGNITO_REGION=ap-south-1
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=false
```

## 🧪 API Testing Commands

### Test Backend Health
```bash
curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health
```

### Test User Registration
```bash
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210", "language": "en"}'
```

### Test Schemes API
```bash
curl "https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/schemes?state=KA&category=agriculture"
```

## 📞 Support Links

### AWS Support
```
https://console.aws.amazon.com/support/
```

### Vercel Support
```
https://vercel.com/support
```

### GitHub Support
```
https://support.github.com/
```

### Next.js Documentation
```
https://nextjs.org/docs
```

## 🎯 Quick Deployment Steps

1. **Create GitHub Repository**: https://github.com/new
2. **Upload your project files** (drag & drop)
3. **Deploy to Vercel**: https://vercel.com/new
4. **Configure environment variables** (copy from above)
5. **Your app goes live** in 2-3 minutes!

## 🌟 Your Platform Impact

Once live, your Voice for Bharat platform will:
- Serve **millions of citizens** across India
- Support **6 Indian languages** for digital inclusion
- Provide **24/7 voice assistance** for government schemes
- Enable **real-time application tracking**
- Bridge the **digital divide** with voice-first interaction

---

**All systems ready for production deployment! 🚀**