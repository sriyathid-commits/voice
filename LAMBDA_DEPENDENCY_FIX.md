# Lambda Dependency Fix - Simple Solution

## Problem Identified ✅
The Lambda code is there but Python dependencies are missing. CloudWatch shows:
```
Runtime.ImportModuleError: Unable to import module 'handler'
```

## Simplest Solution: Use AWS SAM to Deploy

SAM automatically handles dependencies. Here's how:

### Step 1: Build with SAM
```powershell
cd backend
sam build --use-container
```

This builds the Lambda with all dependencies in a Docker container (works on Windows).

### Step 2: Deploy
```powershell
sam deploy --stack-name voicebharatai --region ap-south-1 --capabilities CAPABILITY_NAMED_IAM --no-confirm-changeset
```

This updates just the Lambda code with dependencies.

## Alternative: Manual Upload (If SAM doesn't work)

### Option A: Use Lambda Layers
1. Create a layer with dependencies
2. Attach to Lambda
3. Upload just the code

### Option B: Use Pre-built Package
Download pre-built package with dependencies from AWS or use Docker to build.

## Fastest Fix Right Now

Since we're having dependency issues on Windows, let's use a different approach:

### Create Lambda Function URL (Bypass Everything)

1. Go to Lambda Console:
   ```
   https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev
   ```

2. Click "Configuration" tab

3. Click "Function URL" in left menu

4. Click "Create function URL"

5. Settings:
   - Auth type: **NONE**
   - Configure cross-origin resource sharing (CORS): **CHECK THIS BOX**
   - Click "Save"

6. Copy the Function URL (e.g., `https://abc123.lambda-url.ap-south-1.on.aws/`)

7. Update frontend `frontend/web/src/lib/constants.ts`:
   ```typescript
   export const API_URL = 'https://YOUR-FUNCTION-URL-HERE'
   ```

8. Redeploy frontend:
   ```powershell
   cd frontend/web
   vercel --prod
   ```

But wait - the Lambda still needs dependencies! So we need to fix that first.

## Real Fix: Deploy with Docker

Since Windows has issues building Python packages with Rust dependencies, use Docker:

### Step 1: Install Docker Desktop
Download from: https://www.docker.com/products/docker-desktop/

### Step 2: Build with SAM using Docker
```powershell
cd backend
sam build --use-container
sam deploy --stack-name voicebharatai --region ap-south-1 --capabilities CAPABILITY_NAMED_IAM
```

The `--use-container` flag uses Docker to build, which works perfectly on Windows.

## Quick Workaround: Simplify Dependencies

Remove problematic dependencies and use only boto3 (which is pre-installed in Lambda):

### Update `requirements.txt` to minimal:
```
boto3>=1.34.0
```

### Update handler to not use FastAPI:
Use simple Lambda handler without FastAPI/Mangum.

This is less ideal but will work immediately.

## Recommended Action

1. **Install Docker Desktop** (if not installed)
2. **Run SAM build with container**:
   ```powershell
   cd backend
   sam build --use-container
   sam deploy --stack-name voicebharatai --region ap-south-1 --capabilities CAPABILITY_NAMED_IAM
   ```
3. **Wait 5-10 minutes** for deployment
4. **Test voice assistant**

This will properly package all dependencies and deploy them.

## Status

- ✅ Lambda exists
- ✅ Lambda is being invoked
- ❌ Lambda dependencies missing
- ❌ Need to redeploy with dependencies

The good news: We know exactly what's wrong and how to fix it!
