# Fix Voice API - Simple API Gateway Method (5 Minutes)

## Step 1: Roll Back CloudFormation (2 minutes)

1. In CloudFormation console, click **"Roll back"** button
2. Wait for status: `UPDATE_ROLLBACK_COMPLETE`

## Step 2: Open API Gateway Console

Click this link:
```
https://ap-south-1.console.aws.amazon.com/apigateway/main/apis?region=ap-south-1
```

## Step 3: Find Your API

1. Look for API named: **voice-for-bharat-api-dev**
2. Click on it

## Step 4: Navigate to the Voice Endpoint

1. In left sidebar, click **"Resources"**
2. You'll see a tree structure of endpoints
3. Find: **POST /voice/query**
4. Click on **POST** under `/voice/query`

## Step 5: Remove Authorization

1. Click on **"Method Request"** (top box)
2. Look for **"Authorization"** setting
3. Click **"Edit"** (pencil icon)
4. Change from **"Cognito User Pool Authorizer"** to **"NONE"**
5. Click **"Save"** (checkmark icon)

## Step 6: Deploy the Changes

1. Click **"Actions"** dropdown (top of page)
2. Select **"Deploy API"**
3. Deployment stage: Select **"dev"**
4. Click **"Deploy"**

## Step 7: Test Voice Assistant

1. Go to: https://bharatvisionxai.vercel.app/assistant
2. Click microphone button
3. Speak in Hindi or any language
4. Should work now! ✅

## Visual Guide

```
API Gateway Console
├── APIs
│   └── voice-for-bharat-api-dev (click this)
│       └── Resources (left sidebar)
│           └── /voice
│               └── /query
│                   └── POST (click this)
│                       └── Method Request (click this)
│                           └── Authorization: Edit → NONE → Save
│                           
└── Actions → Deploy API → Stage: dev → Deploy
```

## If You Can't Find the Endpoint

The endpoint might be at the root level:
- Look for: **POST /voice/query** directly under Resources
- Or: **ANY /voice/query**
- Or: **/{proxy+}** (catch-all route)

If you see `/{proxy+}`, the Lambda is handling all routes, so authorization is set at the API level:

1. Click on the API name (top breadcrumb)
2. Click **"Authorizers"** in left sidebar
3. Find the Cognito authorizer
4. Note its name
5. Go back to Resources
6. Click on the method
7. Remove the authorizer reference

## Alternative: Create New Public Endpoint

If the above is too complex:

1. In Resources, click **"Actions"** → **"Create Resource"**
2. Resource Name: `public-voice`
3. Click **"Create Resource"**
4. Select the new resource
5. Click **"Actions"** → **"Create Method"** → **"POST"**
6. Integration type: **Lambda Function**
7. Lambda Function: `voice-for-bharat-voice-service-dev`
8. Authorization: **NONE**
9. Click **"Save"**
10. Click **"Actions"** → **"Deploy API"** → Stage: **dev**

Then update frontend URL to: `/public-voice/query`

## Troubleshooting

**Can't find the API?**
- Make sure region is **ap-south-1** (Mumbai)
- Check CloudFormation outputs for API Gateway ID

**Can't edit authorization?**
- You might need to click "Edit" button first
- Look for pencil icon next to Authorization field

**Changes not working?**
- Make sure you clicked "Deploy API" after making changes
- Wait 30 seconds for propagation
- Clear browser cache and try again

## Success Indicator

When it works, you'll see:
- Transcript of what you said
- AI response text
- Audio playing (for Hindi/English)

No more "Failed to process voice query" error!
