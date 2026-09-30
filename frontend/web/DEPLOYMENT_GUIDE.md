# Voice for Bharat - Frontend Deployment Guide

## Deployment Options

### Option 1: Vercel (Recommended for Quick Deploy)

#### Prerequisites
- GitHub account with repository access
- Vercel account (free tier works)

#### Steps

1. **Push code to GitHub** (if not already done):
```bash
git add .
git commit -m "Complete frontend integration for Voice for Bharat"
git push origin main
```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Select `frontend/web` as the root directory

3. **Configure Environment Variables** in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL=https://d18s1aceaoasx3.cloudfront.net
NEXT_PUBLIC_COGNITO_USER_POOL_ID=your_cognito_pool_id
NEXT_PUBLIC_COGNITO_CLIENT_ID=your_cognito_client_id
NEXT_PUBLIC_COGNITO_REGION=ap-south-1
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=false
```

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete (3-5 minutes)
   - Access your live site at the provided URL

5. **Configure Custom Domain** (Optional):
   - Go to Project Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

#### Auto-Deploy on Push
Vercel automatically deploys on every push to main branch.

---

### Option 2: AWS Amplify

#### Prerequisites
- AWS account
- GitHub repository
- AWS CLI configured

#### Steps

1. **Create Amplify App**:
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Configure Amplify
amplify configure

# Initialize Amplify project
cd frontend/web
amplify init
```

2. **Add Hosting**:
```bash
amplify add hosting
# Choose: Hosting with Amplify Console (Managed hosting with custom domains, Continuous deployment)
```

3. **Connect Repository**:
   - Go to AWS Amplify Console
   - Click "Connect app"
   - Choose GitHub
   - Select repository and branch
   - Build settings auto-detected for Next.js

4. **Configure Build Settings**:
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend/web
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/web/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/web/node_modules/**/*
```

5. **Set Environment Variables** in Amplify Console:
   - Go to App settings → Environment variables
   - Add all NEXT_PUBLIC_* variables

6. **Deploy**:
```bash
amplify publish
```

---

### Option 3: Netlify

#### Steps

1. **Install Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **Login and Initialize**:
```bash
netlify login
cd frontend/web
netlify init
```

3. **Configure Build**:
   - Build command: `npm run build`
   - Publish directory: `.next`
   - Base directory: `frontend/web`

4. **Set Environment Variables**:
```bash
netlify env:set NEXT_PUBLIC_API_URL "https://your-api-url.com"
# Repeat for all environment variables
```

5. **Deploy**:
```bash
netlify deploy --prod
```

---

## Post-Deployment Steps

### 1. Update CORS on Backend
Add your frontend domain to allowed origins:
```python
# In your API Gateway or Lambda CORS config
ALLOWED_ORIGINS = [
    'https://your-app.vercel.app',
    'https://your-custom-domain.com',
    'http://localhost:3000'  # Keep for local dev
]
```

### 2. Test Critical Flows
- [ ] Authentication (login/logout)
- [ ] Scheme browsing and search
- [ ] Voice assistant (if enabled)
- [ ] Profile editing
- [ ] Application submission

### 3. Configure Cognito Callback URLs
In AWS Cognito User Pool:
- Add your deployment URL to Allowed Callback URLs
- Add your deployment URL to Allowed Sign-out URLs

### 4. Update DNS (if using custom domain)
Point your domain to deployment platform:
- **Vercel**: Add CNAME to `cname.vercel-dns.com`
- **Amplify**: Follow Amplify Console instructions
- **Netlify**: Add CNAME to Netlify URL

### 5. Enable HTTPS
All platforms provide free SSL certificates. Ensure:
- [ ] HTTPS is enforced
- [ ] HTTP redirects to HTTPS
- [ ] Mixed content warnings resolved

### 6. Set up Monitoring
- [ ] Enable error tracking (Sentry, LogRocket, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure alerting for critical errors

---

## Environment Variables Reference

### Required Variables
```bash
# Backend API
NEXT_PUBLIC_API_URL=          # Your REST API endpoint
NEXT_PUBLIC_WS_URL=           # Your WebSocket endpoint
NEXT_PUBLIC_CLOUDFRONT_URL=   # CDN for media files

# AWS Cognito (if using)
NEXT_PUBLIC_COGNITO_USER_POOL_ID=
NEXT_PUBLIC_COGNITO_CLIENT_ID=
NEXT_PUBLIC_COGNITO_REGION=

# Feature Flags
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=false
```

### Optional Variables
```bash
# Analytics
NEXT_PUBLIC_GA_TRACKING_ID=
NEXT_PUBLIC_HOTJAR_ID=

# Error Tracking
NEXT_PUBLIC_SENTRY_DSN=

# App Configuration
NEXT_PUBLIC_APP_NAME="Voice for Bharat"
NEXT_PUBLIC_SUPPORT_EMAIL=support@voiceforbharat.in
NEXT_PUBLIC_SUPPORT_PHONE=+91-1800-XXX-XXXX
```

---

## Troubleshooting

### Build Fails
1. Check Node.js version (requires Node 18+)
2. Clear cache: `rm -rf .next node_modules && npm install`
3. Check for TypeScript errors: `npm run type-check`
4. Check environment variables are set

### API Requests Fail
1. Verify API_URL is correct and accessible
2. Check CORS configuration on backend
3. Verify authentication token is being sent
4. Check network tab in browser DevTools

### Authentication Doesn't Work
1. Verify Cognito configuration
2. Check callback URLs in Cognito
3. Verify COGNITO_CLIENT_ID is correct
4. Check browser console for auth errors

### Voice Assistant Issues
1. Verify WS_URL is correct
2. Check microphone permissions
3. Verify Bedrock is configured on backend
4. Test with ENABLE_VOICE_ASSISTANT=false to isolate issue

---

## Performance Optimization

### Recommended Settings

1. **Enable Image Optimization**:
```js
// next.config.js
images: {
  domains: ['d18s1aceaoasx3.cloudfront.net'],
  formats: ['image/webp', 'image/avif'],
}
```

2. **Enable Compression**:
Most platforms enable gzip/brotli by default.

3. **Configure Caching**:
```js
// next.config.js
headers: async () => [
  {
    source: '/:all*(svg|jpg|png|gif|webp)',
    headers: [
      {
        key: 'Cache-Control',
        value: 'public, max-age=31536000, immutable',
      },
    ],
  },
]
```

4. **Bundle Analysis**:
```bash
npm install --save-dev @next/bundle-analyzer
```

---

## Rollback Procedure

### Vercel
1. Go to Project → Deployments
2. Find previous working deployment
3. Click three dots → "Promote to Production"

### Amplify
1. Go to App → Hosting
2. Find previous build
3. Click "Redeploy this version"

### Netlify
1. Go to Deploys tab
2. Find previous deploy
3. Click "Publish deploy"

---

## Monitoring & Maintenance

### Weekly Checks
- [ ] Review error logs
- [ ] Check API response times
- [ ] Verify authentication working
- [ ] Test critical user flows

### Monthly
- [ ] Update dependencies (`npm outdated`)
- [ ] Review performance metrics
- [ ] Check SSL certificate expiry
- [ ] Test on latest browser versions

### Security
- [ ] Keep dependencies updated
- [ ] Review access logs for anomalies
- [ ] Rotate API keys if needed
- [ ] Audit user permissions

---

## Quick Deploy Commands

### Vercel (from CLI)
```bash
cd frontend/web
npx vercel --prod
```

### Amplify
```bash
cd frontend/web
amplify publish
```

### Netlify
```bash
cd frontend/web
netlify deploy --prod
```

---

## Support

For deployment issues, contact:
- **Platform Issues**: Check platform status page
- **Code Issues**: Review GitHub issues
- **API Issues**: Check backend logs in CloudWatch

**Documentation**: See `/docs` folder for detailed guides
**API Docs**: See backend `README.md` for API endpoints
