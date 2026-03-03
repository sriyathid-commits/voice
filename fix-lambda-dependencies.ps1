# Fix Lambda Dependencies - Package and Deploy

Write-Host "Fixing Lambda Dependencies..." -ForegroundColor Cyan
Write-Host ""

# Navigate to voice service directory
cd backend/lambdas/voice_service

# Create package directory
Write-Host "Creating package directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path package | Out-Null

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -t package/

# Copy Lambda code
Write-Host "Copying Lambda code..." -ForegroundColor Yellow
Copy-Item handler.py package/
Copy-Item service.py package/
Copy-Item models.py package/
Copy-Item __init__.py package/ -ErrorAction SilentlyContinue

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
cd package
Compress-Archive -Path * -DestinationPath ../voice_service_complete.zip -Force
cd ..

Write-Host ""
Write-Host "✅ Package created: voice_service_complete.zip" -ForegroundColor Green
Write-Host ""
Write-Host "Now upload this to Lambda:" -ForegroundColor Cyan
Write-Host "1. Go to: https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev" -ForegroundColor White
Write-Host "2. Click 'Upload from' → '.zip file'" -ForegroundColor White
Write-Host "3. Select: backend/lambdas/voice_service/voice_service_complete.zip" -ForegroundColor White
Write-Host "4. Click 'Save'" -ForegroundColor White
Write-Host "5. Wait for upload to complete" -ForegroundColor White
Write-Host "6. Test voice assistant again!" -ForegroundColor White
Write-Host ""

# Clean up
Remove-Item -Recurse -Force package

Write-Host "Package is ready at: backend/lambdas/voice_service/voice_service_complete.zip" -ForegroundColor Green
