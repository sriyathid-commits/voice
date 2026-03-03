# Complete Final Setup - Step by Step

## Issue 1: Check CloudWatch Logs (Find the Real Error)

### Step 1: Open CloudWatch Logs
Click this link:
```
https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fvoice-for-bharat-voice-service-dev
```

### Step 2: Look for Recent Logs
- Check if there are ANY log streams
- If YES: Click on the most recent one and look for errors
- If NO: Lambda is not being invoked at all

### What to Look For:
- ✅ "START RequestId" = Lambda is being invoked
- ❌ "Missing module" = Dependencies not installed
- ❌ "Access Denied" = IAM permissions issue
- ❌ "Timeout" = Lambda taking too long
- ❌ No logs = Lambda not being invoked

---

## Issue 2: Verify Bedrock Access

### Step 1: Open Bedrock Console
```
https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/models
```

### Step 2: Check Model Access
Look for these models:
- ✅ Claude 3 Sonnet (anthropic.claude-3-sonnet-20240229-v1:0)
- ✅ Titan Embeddings (amazon.titan-embed-text-v1)

### Step 3: Test Bedrock
1. Click on "Playgrounds" in left sidebar
2. Click "Chat"
3. Select "Claude 3 Sonnet"
4. Type a test message
5. If it works = Bedrock is accessible ✅
6. If error = Need to request access ❌

---

## Issue 3: Test Lambda Function Directly

### Step 1: Open Lambda Console
```
https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev
```

### Step 2: Create Test Event
1. Click "Test" tab
2. Click "Create new event"
3. Event name: `test-voice-query`
4. Use this test data:

```json
{
  "httpMethod": "POST",
  "path": "/voice/query",
  "headers": {
    "Content-Type": "multipart/form-data"
  },
  "body": "",
  "isBase64Encoded": false
}
```

5. Click "Save"
6. Click "Test" button

### Step 3: Check Results
- ✅ Success = Lambda works
- ❌ Error = Check error message

---

## Issue 4: Check VPC Configuration

### Step 1: Check if Lambda is in VPC
1. In Lambda console, go to "Configuration" tab
2. Click "VPC" in left menu
3. Check if VPC is configured

### Step 2: If Lambda is in VPC
**Problem**: Lambda in VPC can't reach internet services (Bedrock, Transcribe, Polly)

**Solution A - Remove VPC** (Easiest):
1. Click "Edit" on VPC section
2. Select "No VPC"
3. Click "Save"
4. Wait 1 minute
5. Test voice assistant again

**Solution B - Add NAT Gateway** (Complex):
- Requires creating NAT Gateway in VPC
- Costs ~$32/month
- Not recommended for testing

**Solution C - Add VPC Endpoints** (Medium):
- Create VPC endpoints for Bedrock, Transcribe, Polly
- Free but complex setup

---

## Issue 5: Verify API Gateway Integration

### Step 1: Test API Gateway
1. Go to API Gateway console
2. Select `voice-for-bharat-api-dev`
3. Click "Resources"
4. Click `/voice/query` → `POST`
5. Click "Test" button (lightning icon)
6. Add test data in "Request Body"
7. Click "Test"

### Step 2: Check Response
- ✅ 200 OK = Integration works
- ❌ 500 Error = Lambda error
- ❌ 502 Bad Gateway = Lambda timeout or crash

---

## Quick Fix: Use Lambda Function URL (Bypass API Gateway)

This is the FASTEST way to get it working:

### Step 1: Create Function URL
1. Go to Lambda console: `voice-for-bharat-voice-service-dev`
2. Click "Configuration" tab
3. Click "Function URL" in left menu
4. Click "Create function URL"
5. Auth type: **NONE**
6. Configure CORS: **Check the box**
7. Click "Save"
8. Copy the Function URL (e.g., `https://abc123.lambda-url.ap-south-1.on.aws/`)

### Step 2: Update Frontend
Update `frontend/web/src/lib/constants.ts`:

```typescript
export const API_URL = 'https://YOUR-FUNCTION-URL-HERE'
```

### Step 3: Redeploy Frontend
```bash
cd frontend/web
vercel --prod
```

This bypasses API Gateway completely and should work immediately!

---

## Diagnostic Script

Run this to check everything:

```powershell
# Check Lambda exists
aws lambda get-function --function-name voice-for-bharat-voice-service-dev --region ap-south-1

# Check recent logs
aws logs tail /aws/lambda/voice-for-bharat-voice-service-dev --region ap-south-1 --since 10m

# Test API endpoint
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/voice/query
```

---

## Most Likely Issues & Fixes

### Issue: Lambda in VPC without internet
**Fix**: Remove VPC configuration from Lambda

### Issue: Missing dependencies in Lambda
**Fix**: Redeploy Lambda with dependencies

### Issue: Bedrock not accessible
**Fix**: Request Bedrock access (though it should be auto-enabled)

### Issue: IAM permissions missing
**Fix**: Add Bedrock/Transcribe/Polly permissions to Lambda role

---

## Step-by-Step Completion Plan

### Phase 1: Diagnose (10 minutes)
1. ✅ Check CloudWatch Logs
2. ✅ Check Bedrock access
3. ✅ Test Lambda directly
4. ✅ Check VPC configuration

### Phase 2: Fix (15 minutes)
1. Remove VPC if configured
2. Add missing IAM permissions if needed
3. Request Bedrock access if needed
4. Redeploy Lambda if needed

### Phase 3: Test (5 minutes)
1. Test Lambda directly
2. Test API Gateway
3. Test voice assistant
4. Verify end-to-end flow

---

## What I Need You to Do

Please do these in order:

1. **Check CloudWatch Logs** (link above)
   - Tell me if you see any logs
   - If yes, copy the error message

2. **Check Bedrock Console** (link above)
   - Tell me if Claude 3 Sonnet is listed
   - Try the playground test

3. **Check Lambda VPC** (Lambda console → Configuration → VPC)
   - Tell me if VPC is configured
   - If yes, we'll remove it

Once you tell me what you find, I'll give you the exact fix!

---

## Expected Results After Fix

✅ Voice assistant works
✅ Can record audio
✅ Gets transcript from Transcribe
✅ Gets AI response from Bedrock
✅ Plays audio from Polly
✅ No errors

---

## Emergency Fallback

If nothing works, we can:
1. Create a simple Lambda Function URL
2. Update frontend to use it
3. Bypass all the API Gateway complexity
4. Get it working in 5 minutes

Let me know what you find in CloudWatch Logs and we'll fix it!
