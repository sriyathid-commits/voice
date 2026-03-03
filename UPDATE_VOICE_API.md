# Update Voice API to Allow Public Access

## What Changed

The `/voice/query` endpoint now allows public access (no authentication required) so the frontend can call it directly.

## Option 1: Update via AWS Console (Recommended)

1. Open AWS CloudFormation Console:
   ```
   https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1
   ```

2. Select the `voicebharatai` stack

3. Click "Update" → "Replace current template"

4. Upload the updated `backend/template.yaml` file

5. Click "Next" through all screens (keep existing parameters)

6. Check "I acknowledge that AWS CloudFormation might create IAM resources"

7. Click "Submit"

8. Wait for stack update to complete (5-10 minutes)

## Option 2: Update via AWS CLI (If Available)

```bash
cd backend
aws cloudformation update-stack \
  --stack-name voicebharatai \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region ap-south-1
```

## What This Does

The template now includes:

```yaml
Events:
  ProcessVoiceQuery:
    Type: Api
    Properties:
      RestApiId: !Ref VoiceForBharatApi
      Path: /voice/query
      Method: POST
      Auth:
        Authorizer: NONE  # <-- This allows public access
```

This removes the Cognito authentication requirement for the voice endpoint, allowing the frontend to call it without a token.

## After Update

The voice assistant on the frontend will work immediately:
- https://bharatvisionxai.vercel.app/assistant

## Testing

1. Go to the Assistant page
2. Select a language (Hindi recommended)
3. Click the microphone button
4. Speak your query
5. Wait for AI response

The full flow will work:
- Audio recording → Amazon Transcribe (STT)
- Text processing → Amazon Bedrock Claude (AI)
- Response generation → Amazon Polly (TTS)
- Audio playback in browser
