# Stack Update Failed - How to Fix

## Current Situation
The CloudFormation stack update failed with template validation errors. The stack is in `UPDATE_FAILED` state.

## Immediate Action Required

### Step 1: Roll Back to Previous Working State
1. In the CloudFormation console (where you are now), click the **"Roll back"** button
2. This will restore the stack to its previous working state
3. Wait for status to change to `UPDATE_ROLLBACK_COMPLETE` (2-3 minutes)

### Step 2: Alternative Solution - Make API Public via Console

Instead of updating the entire template, we can make the API endpoint public directly through API Gateway console:

#### Option A: Remove Auth from API Gateway (Simpler)

1. Go to API Gateway console:
   ```
   https://ap-south-1.console.aws.amazon.com/apigateway/main/apis?region=ap-south-1
   ```

2. Find and click on: **voice-for-bharat-api-dev**

3. Click on **Resources** in left menu

4. Find the `/voice/query` POST method

5. Click on **Method Request**

6. Click **Edit** next to Authorization

7. Change from **Cognito User Pool** to **NONE**

8. Click **Save**

9. Click **Actions** → **Deploy API**

10. Select Stage: **dev**

11. Click **Deploy**

12. Test the voice assistant!

#### Option B: Create New API Resource (If above doesn't work)

1. In API Gateway console, click **Create Resource**
2. Resource Name: `voice-public`
3. Create Method: POST
4. Integration type: Lambda Function
5. Lambda: `voice-for-bharat-voice-service-dev`
6. Authorization: NONE
7. Deploy API

Then update frontend to use new endpoint: `/voice-public/query`

## Why the Template Update Failed

The SAM template has validation errors. The `Auth: Authorizer: NONE` syntax might not be correct for SAM templates. The correct syntax should be:

```yaml
Events:
  ProcessVoiceQuery:
    Type: Api
    Properties:
      RestApiId: !Ref VoiceForBharatApi
      Path: /voice/query
      Method: POST
      Auth:
        Authorizer: NONE  # This might need to be 'AWS_IAM' or removed entirely
```

## Recommended Approach

**Use Option A above** - it's faster and doesn't require template changes. You can modify the API Gateway settings directly through the console.

## After Fixing

Test the voice assistant at: https://bharatvisionxai.vercel.app/assistant

The error should be gone!
