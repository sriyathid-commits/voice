# Voice for Bharat - Complete Verification Guide

## 🔍 **System Verification Checklist**

### **1. Backend API Verification**

#### **Check if Backend is Deployed**
```bash
# Test health endpoints
curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health
curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/user/health
curl https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/schemes/health
```

**Expected Response**: `{"status": "healthy", "service": "service-name"}`

#### **Test Authentication Flow**
```bash
# 1. Register/Send OTP
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/register \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "+919999999999", "language": "en"}'

# Expected: {"success": true, "message": "OTP sent", "user_id": "..."}

# 2. Verify OTP (use real OTP from SMS)
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phoneNumber": "+919999999999", "otp": "123456"}'

# Expected: {"success": true, "token": "...", "user": {...}}
```

#### **Test Schemes API**
```bash
# Get schemes (no auth required)
curl "https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/schemes?state=KA&limit=5"

# Expected: {"schemes": [...], "count": N}
```

---

### **2. Frontend Verification**

#### **Vercel Deployment Check**
1. Go to your **Vercel dashboard**: https://vercel.com/dashboard
2. Find your Voice for Bharat project
3. Check **Build Status**: Should be "Ready" ✅
4. Check **Domain**: Note your live URL (e.g., `voice-for-bharat-xyz.vercel.app`)

#### **Environment Variables Check**
In Vercel project settings → Environment Variables:
```bash
NEXT_PUBLIC_API_URL = https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL = wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL = https://d18s1aceaoasx3.cloudfront.net
NEXT_PUBLIC_COGNITO_REGION = ap-south-1
NEXT_PUBLIC_ENABLE_PWA = true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT = true
```

#### **Frontend Functionality Test**
1. **Landing Page**: https://your-app.vercel.app
   - [ ] Page loads without errors
   - [ ] "Get Started" button works
   
2. **Login Flow**: `/login`
   - [ ] Phone number input accepts Indian numbers
   - [ ] OTP request sends (check browser network tab)
   - [ ] OTP verification works (if backend is live)
   
3. **Dashboard**: `/dashboard` (after login)
   - [ ] Metrics cards display
   - [ ] Navigation tabs work
   - [ ] State selector functions

---

### **3. AWS Infrastructure Verification**

#### **Check if AWS Stack Exists**
```bash
# Install AWS CLI first (if not installed)
# Windows: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html

# Configure AWS credentials
aws configure
# Enter: Access Key, Secret Key, Region (ap-south-1), Output format (json)

# Check CloudFormation stack
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1

# Check API Gateway
aws apigateway get-rest-apis --region ap-south-1 | grep -i voice

# Check Lambda functions
aws lambda list-functions --region ap-south-1 | grep -i voice
```

#### **DynamoDB Tables Check**
```bash
# List all tables
aws dynamodb list-tables --region ap-south-1

# Check specific tables
aws dynamodb describe-table --table-name voice-for-bharat-dev-users --region ap-south-1
aws dynamodb describe-table --table-name voice-for-bharat-dev-schemes --region ap-south-1
```

#### **S3 Buckets Check**
```bash
# List buckets
aws s3 ls | grep voice-for-bharat

# Check bucket contents
aws s3 ls s3://voice-for-bharat-documents-dev-123456789/
aws s3 ls s3://voice-for-bharat-audio-dev-123456789/
```

---

### **4. End-to-End User Journey Test**

#### **Complete User Flow** (Manual Testing)
1. **Registration**:
   - [ ] Open frontend URL
   - [ ] Click "Get Started" → Login
   - [ ] Enter Indian phone number
   - [ ] Receive OTP via SMS
   - [ ] Enter OTP → Login success

2. **Profile Setup**:
   - [ ] Navigate to Profile tab
   - [ ] Fill out personal details
   - [ ] Save profile → Success toast
   - [ ] Profile strength increases

3. **Scheme Discovery**:
   - [ ] Navigate to Schemes tab
   - [ ] Browse schemes list
   - [ ] Filter by state/category
   - [ ] Click on a scheme → Detail page loads
   - [ ] Check eligibility → Score displayed
   - [ ] Save scheme → Success

4. **Voice Assistant**:
   - [ ] Navigate to Assistant tab
   - [ ] Allow microphone permission
   - [ ] Click record → Speak query
   - [ ] Stop recording → Processing indicator
   - [ ] AI response appears
   - [ ] TTS audio plays (if implemented)

5. **Application Submission**:
   - [ ] From scheme detail → "Apply Now"
   - [ ] Fill application form
   - [ ] Upload document (PDF/JPG)
   - [ ] Save as draft → Success
   - [ ] Submit application → Success
   - [ ] View application status

---

### **5. Performance & Error Verification**

#### **Network & Performance**
1. **Browser DevTools** (F12):
   - [ ] **Console**: No JavaScript errors
   - [ ] **Network**: All API calls return 200/201
   - [ ] **Performance**: Page loads < 3 seconds
   - [ ] **Application**: Service worker registered (PWA)

2. **Mobile Testing**:
   - [ ] Responsive design works on phone
   - [ ] Touch targets are >= 44px
   - [ ] Text is readable without zoom

#### **Error Handling**
1. **Network Offline**:
   - [ ] Disconnect internet
   - [ ] App shows "No internet" banner
   - [ ] Reconnect → Banner disappears

2. **API Errors**:
   - [ ] Invalid API calls show user-friendly errors
   - [ ] Loading states prevent duplicate clicks
   - [ ] Retry buttons work

---

### **6. Production Readiness Check**

#### **Security**
- [ ] HTTPS enforced on frontend
- [ ] API calls use HTTPS
- [ ] No sensitive data in localStorage (only tokens)
- [ ] CORS properly configured
- [ ] Input validation works

#### **SEO & Accessibility**
- [ ] Page titles are descriptive
- [ ] Meta descriptions present
- [ ] Alt text on images
- [ ] Proper heading hierarchy (h1, h2, h3)
- [ ] Keyboard navigation works

#### **PWA Features**
- [ ] App manifest.json loads
- [ ] Service worker active
- [ ] "Add to Home Screen" prompt (mobile)
- [ ] Works offline (basic functionality)

---

## 🚨 **Common Issues & Fixes**

### **Backend Not Responding**
```bash
# Check if stack is deployed
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1

# If stack doesn't exist, deploy it:
cd backend
sam build
sam deploy --guided
```

### **Frontend Build Fails**
```bash
# Check build locally
cd frontend/web
npm run build

# Common fixes:
npm install  # Install dependencies
rm -rf .next  # Clear Next.js cache
npm run build  # Try again
```

### **CORS Errors**
- Update API Gateway CORS settings to include your Vercel domain
- Check `allow_origins` in Lambda CORS middleware

### **Environment Variables Missing**
- Double-check Vercel project settings
- Redeploy after adding env vars

---

## ✅ **Quick Verification Commands**

```bash
# 1. Test backend health
curl -f https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/health || echo "Backend DOWN"

# 2. Test frontend build
cd frontend/web && npm run build && echo "Frontend BUILD OK"

# 3. Check AWS resources
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query 'Stacks[0].StackStatus'
```

---

## 📊 **Success Metrics**

**✅ Full System Working** when:
- All health endpoints return 200
- User can register/login end-to-end
- Schemes load and are searchable
- Documents can be uploaded
- Applications can be submitted
- Voice assistant responds (if backend supports it)
- Mobile responsive works
- No console errors

**🎯 Ready for Demo** when above + Performance audit passes + No accessibility blockers.

---

## 🔧 **Quick Deploy Commands**

### If you need to redeploy:

**Backend**:
```bash
cd backend
sam build && sam deploy
```

**Frontend**:
```bash
# Push to GitHub (auto-deploys to Vercel)
git add . && git commit -m "Fix" && git push origin main
```

This verification guide will help you systematically check every component of the Voice for Bharat system! 🇮🇳