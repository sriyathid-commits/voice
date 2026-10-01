# 🚀 Deploy Now - Console Only Method

## Step 1: Delete the Failed Stack

**In AWS Console (current page)**:
1. Click **"Delete stack"** button
2. Confirm deletion
3. Wait 5 minutes for deletion

---

## Step 2: Create Lambda Deployment Packages

**Open PowerShell in your project and run these commands**:

```powershell
# Navigate to project
cd C:\Users\yathi\voice\backend

# Create deployment packages for each Lambda
cd lambdas\user_service
Compress-Archive -Path * -DestinationPath ..\..\user_service.zip -Force

cd ..\voice_service
Compress-Archive -Path * -DestinationPath ..\..\voice_service.zip -Force

cd ..\scheme_service
Compress-Archive -Path * -DestinationPath ..\..\scheme_service.zip -Force

cd ..\application_service
Compress-Archive -Path * -DestinationPath ..\..\application_service.zip -Force

cd ..\document_service
Compress-Archive -Path * -DestinationPath ..\..\document_service.zip -Force

cd ..\notification_service
Compress-Archive -Path * -DestinationPath ..\..\notification_service.zip -Force

cd ..\sync_service
Compress-Archive -Path * -DestinationPath ..\..\sync_service.zip -Force

cd ..\..
```

This creates 7 zip files in the `backend` folder.

---

## Step 3: Upload Packages to S3

1. Go to S3 Console: https://s3.console.aws.amazon.com/s3/buckets?region=ap-south-1

2. Click on bucket: **aws-sam-cli-managed-default-samclisourcebucket-...**

3. Click **"Upload"**

4. Drag all 7 zip files from `C:\Users\yathi\voice\backend\`:
   - user_service.zip
   - voice_service.zip
   - scheme_service.zip
   - application_service.zip
   - document_service.zip
   - notification_service.zip
   - sync_service.zip

5. Click **"Upload"**

6. After upload completes, click on each file and copy the **S3 URI** (looks like: `s3://bucket-name/file.zip`)

---

## Step 4: Use Simplified Template

I'll create a simplified template that you can deploy directly from console.

**This template will create**:
- ✅ DynamoDB Tables
- ✅ S3 Buckets
- ✅ Cognito User Pool
- ✅ Lambda functions (using the zips you uploaded)
- ✅ API Gateway

---

## Alternative: Just Install SAM CLI (5 minutes)

Actually, the **FASTEST** way is to just install SAM CLI:

1. **Download**: https://github.com/aws/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi

2. **Run the installer** (click Next a few times)

3. **Restart PowerShell**

4. **Run these 2 commands**:
```powershell
cd C:\Users\yathi\voice\backend
sam build
sam deploy --guided
```

That's it! SAM will handle everything automatically.

---

## Which method do you prefer?

**Method A**: Install SAM CLI (5 min install + 1 command) - RECOMMENDED  
**Method B**: Manual console deployment (30 minutes of clicking)

I highly recommend Method A. It's much faster and less error-prone.

Want me to walk you through Method A?
