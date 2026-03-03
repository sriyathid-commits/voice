# Fix "Failed to process voice query" Error

## Problem
The voice assistant shows: **"Failed to process voice query. Please try again."**

## Cause
The API endpoint requires authentication, but we need to make it public for the voice assistant to work.

## Solution: Update CloudFormation Stack (5 Minutes)

### Option 1: Automated Script (If AWS CLI Available)

Run this command:
```powershell
.\update-stack.ps1
```

Wait 5-10 minutes for completion, then test the voice assistant again.

---

### Option 2: Manual Update via AWS Console (Recommended)

#### Step 1: Open CloudFormation Console
Click this link or copy to browser:
```
https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1
```

#### Step 2: Select Stack
- Find and click on stack: **voicebharatai**
- Current status should show: `CREATE_COMPLETE` or `UPDATE_COMPLETE`

#### Step 3: Update Stack
1. Click the **"Update"** button (top right)
2. Select **"Replace current template"**
3. Click **"Upload a template file"**
4. Click **"Choose file"**
5. Navigate to your project folder
6. Select file: **backend/template.yaml**
7. Click **"Next"**

#### Step 4: Keep Parameters
- Don't change anything
- Just click **"Next"**

#### Step 5: Configure Options
- Don't change anything
- Just click **"Next"**

#### Step 6: Review and Acknowledge
1. Scroll to bottom
2. Check the box: ☑️ **"I acknowledge that AWS CloudFormation might create IAM resources with custom names"**
3. Click **"Submit"**

#### Step 7: Wait for Completion
- Status will change to: `UPDATE_IN_PROGRESS`
- Wait 5-10 minutes
- Status will change to: `UPDATE_COMPLETE` ✅
- You can close the browser tab

#### Step 8: Test Voice Assistant
1. Go to: https://bharatvisionxai.vercel.app/assistant
2. Click microphone button
3. Speak in Telugu or any language
4. Should work now! ✅

---

## What This Update Does

The template change allows public access to the voice API:

**Before:**
```yaml
Events:
  ProcessVoiceQuery:
    Type: Api
    Properties:
      Path: /voice/query
      Method: POST
      # Uses default Cognito authentication
```

**After:**
```yaml
Events:
  ProcessVoiceQuery:
    Type: Api
    Properties:
      Path: /voice/query
      Method: POST
      Auth:
        Authorizer: NONE  # <-- Allows public access
```

---

## Verification

After the update completes, test the API directly:

```bash
# Test if API is accessible (should return 400 or 500, not 401)
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/voice/query
```

If you get `{"message":"Missing Authentication Token"}` - the update didn't work yet.

If you get a different error (like missing parameters) - the update worked! ✅

---

## Still Not Working?

### Check Stack Status
```
https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1
```
- Stack: `voicebharatai`
- Status must be: `UPDATE_COMPLETE`

### Check Lambda Logs
```
https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fvoice-for-bharat-voice-service-dev
```
- Look for recent invocations
- Check for errors

### Check Browser Console
1. Open voice assistant page
2. Press F12
3. Click "Console" tab
4. Try recording again
5. Look for error messages

### Common Errors

**"Missing Authentication Token"**
- Stack update not complete yet
- Wait a few more minutes

**"Could not access microphone"**
- Browser needs microphone permission
- Click lock icon in address bar
- Allow microphone access

**"Network error"**
- Check internet connection
- Try different browser

**"Internal server error"**
- Check Lambda logs in CloudWatch
- VoiceService Lambda may have errors

---

## Quick Test Commands

### Test API Endpoint
```powershell
# Should NOT return "Missing Authentication Token"
curl -X POST https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev/voice/query
```

### Check Stack Status
```powershell
aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].StackStatus"
```

Should return: `"UPDATE_COMPLETE"`

---

## Timeline

- **Stack update**: 5-10 minutes
- **API Gateway propagation**: 1-2 minutes
- **Total time**: ~10 minutes

After this, the voice assistant will work perfectly! 🎉
