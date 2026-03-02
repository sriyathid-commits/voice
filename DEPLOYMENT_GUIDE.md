# Voice for Bharat - Deployment Guide

## 🚀 Complete Deployment Instructions

### Prerequisites
- Git installed
- GitHub account
- Vercel account (free tier works)
- AWS account (already configured)

---

## 📦 Step 1: Push to GitHub

### Initialize Git Repository (if not already done)
```bash
# Initialize git in your project root
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Voice for Bharat platform with AWS backend and Next.js frontend"
```

### Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `voice-for-bharat`
3. Description: `Voice-first AI platform for government welfare schemes in India`
4. Choose Public or Private
5. Don't initialize with README (we already have files)
6. Click "Create repository"

### Push to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/voice-for-bharat.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy Frontend to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)
1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your `voice-for-bharat` repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/web`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

5. Add Environment Variables:
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

6. Click "Deploy"
7. Wait 2-3 minutes for deployment
8. Your app will be live at: `https://voice-for-bharat-xxx.vercel.app`

### Option B: Deploy via Vercel CLI
```bash
# Navigate to frontend directory
cd frontend/web

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name? voice-for-bharat
# - Directory? ./
# - Override settings? N

# Deploy to production
vercel --prod
```

---

## ☁️ Step 3: Backend is Already Deployed!

Your AWS backend is already live:
- ✅ REST API: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
- ✅ WebSocket: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
- ✅ All Lambda functions operational
- ✅ DynamoDB tables created
- ✅ S3 buckets configured
- ✅ Cognito authentication ready

---

## 🔄 Continuous Deployment

### Automatic Deployments
Once connected to GitHub, Vercel will automatically:
- Deploy on every push to `main` branch
- Create preview deployments for pull requests
- Run builds and tests

### Update Backend
```bash
# Make changes to backend code
cd backend

# Build
python -m samcli build

# Deploy
python -m samcli deploy
```

---

## 📋 Post-Deployment Checklist

### Frontend
- [ ] Visit your Vercel URL
- [ ] Test landing page loads
- [ ] Navigate to Dashboard
- [ ] Try Voice Assistant
- [ ] Check Guide page
- [ ] Test on mobile device

### Backend
- [ ] Test API endpoint: `curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health`
- [ ] Check Lambda logs in AWS CloudWatch
- [ ] Verify DynamoDB tables in AWS Console
- [ ] Test S3 bucket access

### Integration
- [ ] Frontend connects to backend API
- [ ] Environment variables are correct
- [ ] CORS is configured properly
- [ ] WebSocket connection works

---

## 🔗 Your Live URLs

After deployment, you'll have:

**Frontend (Vercel)**
- Production: `https://voice-for-bharat-xxx.vercel.app`
- Preview: Auto-generated for each PR

**Backend (AWS)**
- REST API: `https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev`
- WebSocket: `wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev`
- CloudFront: `https://d18s1aceaoasx3.cloudfront.net`

**Development**
- Local: `http://localhost:3000`

---

## 🛠️ Troubleshooting

### Vercel Build Fails
- Check build logs in Vercel dashboard
- Verify all dependencies in package.json
- Ensure environment variables are set

### API Connection Issues
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings in API Gateway
- Test API endpoint directly with curl

### AWS Lambda Errors
- Check CloudWatch Logs: `python -m awscli logs tail /aws/lambda/voice-for-bharat-user-service-dev --follow`
- Verify IAM permissions
- Check environment variables in Lambda

---

## 📊 Monitoring

### Vercel Analytics
- Visit: https://vercel.com/dashboard/analytics
- Monitor page views, performance, and errors

### AWS CloudWatch
```bash
# View Lambda logs
python -m awscli logs tail /aws/lambda/voice-for-bharat-voice-service-dev --follow

# View API Gateway logs
python -m awscli logs tail /aws/apigateway/voice-for-bharat-api-dev --follow
```

### Cost Monitoring
```bash
# Check AWS costs
python -m awscli ce get-cost-and-usage \
  --time-period Start=2026-03-01,End=2026-03-02 \
  --granularity DAILY \
  --metrics BlendedCost
```

---

## 🎉 Success!

Your Voice for Bharat platform is now:
- ✅ Deployed to production
- ✅ Accessible worldwide
- ✅ Automatically deploying updates
- ✅ Monitored and scalable

**Share your app**: Send your Vercel URL to users!

---

## 📞 Support

- **GitHub Issues**: Create issues in your repository
- **Vercel Support**: https://vercel.com/support
- **AWS Support**: https://console.aws.amazon.com/support/

---

## 🔐 Security Notes

1. **Never commit sensitive data**:
   - AWS credentials
   - API keys
   - Database passwords

2. **Use environment variables** for all secrets

3. **Enable HTTPS** (Vercel does this automatically)

4. **Set up monitoring** for unusual activity

5. **Regular updates**: Keep dependencies updated
   ```bash
   npm audit fix
   ```

---

## 📈 Next Steps

1. **Custom Domain**: Add your own domain in Vercel settings
2. **Analytics**: Set up Google Analytics or Vercel Analytics
3. **Error Tracking**: Integrate Sentry for error monitoring
4. **Performance**: Enable Vercel Edge Functions for faster response
5. **SEO**: Add meta tags and sitemap
6. **Testing**: Set up automated E2E tests with Playwright

---

**Congratulations! Your Voice for Bharat platform is live! 🇮🇳**