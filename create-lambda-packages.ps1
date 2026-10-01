# Create Lambda Deployment Packages
# This script creates zip files for all Lambda functions

Write-Host "Creating Lambda deployment packages..." -ForegroundColor Cyan
Write-Host ""

# Navigate to backend
Set-Location backend

# Create packages directory
if (-not (Test-Path "packages")) {
    New-Item -ItemType Directory -Path "packages" | Out-Null
}

$services = @(
    "user_service",
    "voice_service", 
    "scheme_service",
    "application_service",
    "document_service",
    "notification_service",
    "sync_service"
)

foreach ($service in $services) {
    Write-Host "Packaging $service..." -ForegroundColor Yellow
    
    $sourcePath = "lambdas\$service"
    $zipPath = "packages\$service.zip"
    
    if (Test-Path $sourcePath) {
        # Remove old zip if exists
        if (Test-Path $zipPath) {
            Remove-Item $zipPath -Force
        }
        
        # Create zip
        Compress-Archive -Path "$sourcePath\*" -DestinationPath $zipPath -Force
        
        if (Test-Path $zipPath) {
            $size = (Get-Item $zipPath).Length / 1MB
            Write-Host "  [SUCCESS] Created $zipPath ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
        } else {
            Write-Host "  [ERROR] Failed to create $zipPath" -ForegroundColor Red
        }
    } else {
        Write-Host "  [SKIP] $sourcePath not found" -ForegroundColor Yellow
    }
}

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Packages created successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "All packages are in: backend\packages\" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. These packages are LOCAL only (not for direct CloudFormation upload)" -ForegroundColor White
Write-Host "2. You need SAM CLI to deploy them properly" -ForegroundColor White
Write-Host ""
Write-Host "RECOMMENDED: Install SAM CLI and run:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  sam build" -ForegroundColor White
Write-Host "  sam deploy --guided" -ForegroundColor White
Write-Host ""
Write-Host "Download SAM CLI:" -ForegroundColor Cyan
Write-Host "https://github.com/aws/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi" -ForegroundColor White
Write-Host ""
