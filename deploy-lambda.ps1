# Deploy Voice Service Lambda - PowerShell Script
# This script packages and deploys the updated voice service

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Voice for Bharat - Deploy Voice AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if we're in the right directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Yellow

if (-not (Test-Path "backend\lambdas\voice_service")) {
    Write-Host "ERROR: backend\lambdas\voice_service not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found voice_service directory" -ForegroundColor Green
Write-Host ""

# Step 2: Create zip package
Write-Host "Step 1: Creating Lambda deployment package..." -ForegroundColor Cyan

$sourceDir = "backend\lambdas\voice_service"
$zipFile = "voice_service_deployment.zip"

# Remove old zip if exists
if (Test-Path $zipFile) {
    Remove-Item $zipFile -Force
    Write-Host "  Removed old zip file" -ForegroundColor Yellow
}

# Create zip file
Write-Host "  Packaging files..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $sourceDir -File -Exclude "*.lnk","README.md"
Compress-Archive -Path $files.FullName -DestinationPath $zipFile -Force

if (Test-Path $zipFile) {
    $zipSize = (Get-Item $zipFile).Length / 1MB
    Write-Host "✅ Created deployment package: $zipFile ($([math]::Round($zipSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create zip file" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Check AWS CLI
Write-Host "Step 2: Checking AWS CLI..." -ForegroundColor Cyan

try {
    $awsVersion = aws --version 2>&1
    Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
    
    # Try to deploy via CLI
    Write-Host ""
    Write-Host "Step 3: Deploying to AWS Lambda..." -ForegroundColor Cyan
    Write-Host "  Function: voice-for-bharat-voice-service-dev" -ForegroundColor Yellow
    Write-Host "  Region: ap-south-1" -ForegroundColor Yellow
    Write-Host ""
    
    $deployChoice = Read-Host "Deploy now via AWS CLI? (y/n)"
    
    if ($deployChoice -eq "y" -or $deployChoice -eq "Y") {
        Write-Host "  Uploading to Lambda..." -ForegroundColor Yellow
        
        aws lambda update-function-code `
            --function-name voice-for-bharat-voice-service-dev `
            --zip-file fileb://$zipFile `
            --region ap-south-1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Lambda function updated successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Cyan
            Write-Host "1. Request Bedrock access: https://ap-south-1.console.aws.amazon.com/bedrock/" -ForegroundColor Yellow
            Write-Host "2. Test Polly: https://ap-south-1.console.aws.amazon.com/polly/" -ForegroundColor Yellow
            Write-Host "3. Test Transcribe: https://ap-south-1.console.aws.amazon.com/transcribe/" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Deployment failed. Check AWS credentials and permissions." -ForegroundColor Red
        }
    } else {
        Write-Host "Skipped CLI deployment" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "⚠️  AWS CLI not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual deployment steps:" -ForegroundColor Cyan
    Write-Host "1. Open AWS Lambda Console: https://ap-south-1.console.aws.amazon.com/lambda/" -ForegroundColor Yellow
    Write-Host "2. Find function: voice-for-bharat-voice-service-dev" -ForegroundColor Yellow
    Write-Host "3. Click 'Upload from' → '.zip file'" -ForegroundColor Yellow
    Write-Host "4. Upload: $zipFile" -ForegroundColor Yellow
    Write-Host "5. Click 'Save'" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment package ready: $zipFile" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 4: Open relevant AWS consoles
Write-Host "Open AWS consoles? (y/n)" -ForegroundColor Cyan
$openConsoles = Read-Host

if ($openConsoles -eq "y" -or $openConsoles -eq "Y") {
    Write-Host "Opening AWS consoles..." -ForegroundColor Yellow
    
    Start-Process "https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/functions/voice-for-bharat-voice-service-dev"
    Start-Sleep -Seconds 1
    Start-Process "https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess"
    Start-Sleep -Seconds 1
    Start-Process "https://ap-south-1.console.aws.amazon.com/polly/home?region=ap-south-1"
    
    Write-Host "✅ Opened AWS consoles in browser" -ForegroundColor Green
}

Write-Host ""
Write-Host "For detailed instructions, see: deploy-voice-ai.md" -ForegroundColor Cyan
Write-Host ""
