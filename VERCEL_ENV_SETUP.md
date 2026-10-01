# Vercel Environment Variables Setup

## 🎯 Quick Copy-Paste for Vercel

After deploying backend to AWS, copy these environment variables to your Vercel project.

---

## 📋 Step-by-Step Instructions

### 1. Get Values from AWS
Run this command after backend deployment:
```powershell
cd backend
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs"
```

### 2. Go to Vercel Dashboard
1. Open [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project: **voice-for-bharat**
3. Go to **Settings** → **Environment Variables**

### 3. Add These Variables

#### API Configuration
| Variable Name | Value | Where to Get |
|--------------|--------|--------------|
| `NEXT_PUBLIC_API_URL` | `https://[API-ID].execute-api.ap-south-1.amazonaws.com/dev` | CloudFormation Output: `VoiceForBharatApiUrl` |
| `NEXT_PUBLIC_WS_URL` | `wss://[WS-ID].execute-api.ap-south-1.amazonaws.com/dev` | CloudFormation Output: `VoiceWebSocketApiUrl` |
| `NEXT_PUBLIC_CLOUDFRONT_URL` | `https://[CF-ID].cloudfront.net` | CloudFormation Output: `CloudFrontURL` |

#### AWS Cognito
| Variable Name | Value | Where to Get |
|--------------|--------|--------------|
| `NEXT_PUBLIC_COGNITO_USER_POOL_ID` | `ap-south-1_XXXXXXXXX` | CloudFormation Output: `CognitoUserPoolId` |
| `NEXT_PUBLIC_COGNITO_CLIENT_ID` | `xxxxxxxxxxxxxxxxxxxxxxxxxx` | CloudFormation Output: `CognitoUserPoolClientId` |
| `NEXT_PUBLIC_COGNITO_REGION` | `ap-south-1` | Fixed value |

#### Feature Flags
| Variable Name | Value |
|--------------|--------|
| `NEXT_PUBLIC_ENABLE_PWA` | `true` |
| `NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT` | `true` |
| `NEXT_PUBLIC_ENABLE_OFFLINE_MODE` | `true` |

---

## 🚀 Quick Commands to Get Values

### Get API Gateway URL
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs[?OutputKey=='VoiceForBharatApiUrl'].OutputValue" --output text
```

### Get WebSocket URL
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs[?OutputKey=='VoiceWebSocketApiUrl'].OutputValue" --output text
```

### Get CloudFront URL
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs[?OutputKey=='CloudFrontURL'].OutputValue" --output text
```

### Get Cognito User Pool ID
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs[?OutputKey=='CognitoUserPoolId'].OutputValue" --output text
```

### Get Cognito Client ID
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].Outputs[?OutputKey=='CognitoUserPoolClientId'].OutputValue" --output text
```

---

## 📝 Example Values (Replace with Your Own)

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_WS_URL=wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
NEXT_PUBLIC_CLOUDFRONT_URL=https://d18s1aceaoasx3.cloudfront.net

# AWS Cognito
NEXT_PUBLIC_COGNITO_USER_POOL_ID=ap-south-1_abc123xyz
NEXT_PUBLIC_COGNITO_CLIENT_ID=abcdefghijklmnopqrstuvwxyz123456
NEXT_PUBLIC_COGNITO_REGION=ap-south-1

# Feature Flags
NEXT_PUBLIC_ENABLE_PWA=true
NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=true
```

---

## ✅ Verification

After adding environment variables:

1. **Redeploy** your Vercel project (it should auto-deploy)
2. **Check Build Logs** for any errors
3. **Test the deployed site**:
   - Open your Vercel URL
   - Open Browser Console (F12)
   - Check that API calls go to your AWS endpoint
   - Try logging in with a phone number

### Test API Connection
```javascript
// Open browser console on your Vercel site and run:
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);
fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
  .then(r => r.json())
  .then(d => console.log('Backend Status:', d));
```

---

## 🔧 Troubleshooting

### Issue: Variables not showing in build
**Solution**: Make sure all variables start with `NEXT_PUBLIC_`

### Issue: API calls failing
**Solution**: Check CORS settings in API Gateway allow your Vercel domain

### Issue: Cognito authentication fails
**Solution**: Verify User Pool ID and Client ID are correct

### Issue: Build fails
**Solution**: Check build logs in Vercel dashboard for specific errors

---

## 📱 For Production

### Additional Variables (Optional)
```bash
# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Sentry Error Tracking
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# Environment
NEXT_PUBLIC_ENV=production
```

---

## 🔐 Security Notes

- Never commit `.env.local` to Git (it's in `.gitignore`)
- Only `NEXT_PUBLIC_*` variables are exposed to browser
- Backend secrets stay in AWS (not in Vercel)
- Rotate Cognito Client ID if accidentally exposed

---

## 📞 Need Help?

If you get stuck:
1. Check Vercel build logs
2. Test backend endpoints directly: `curl [YOUR-API-URL]/health`
3. Verify AWS CloudFormation stack is complete
4. Check browser console for specific errors

---

**Ready?** Add these variables to Vercel and click Deploy! 🚀
