# Update CloudFormation Stack to Allow Public Voice API Access

Write-Host "Updating CloudFormation Stack: voicebharatai" -ForegroundColor Cyan
Write-Host "Region: ap-south-1" -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is available
$awsCommand = Get-Command aws -ErrorAction SilentlyContinue

if (-not $awsCommand) {
    Write-Host "ERROR: AWS CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please update the stack manually via AWS Console:" -ForegroundColor Yellow
    Write-Host "1. Open: https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1" -ForegroundColor White
    Write-Host "2. Click on stack 'voicebharatai'" -ForegroundColor White
    Write-Host "3. Click 'Update' button" -ForegroundColor White
    Write-Host "4. Select 'Replace current template'" -ForegroundColor White
    Write-Host "5. Upload file: backend/template.yaml" -ForegroundColor White
    Write-Host "6. Click 'Next' through all screens" -ForegroundColor White
    Write-Host "7. Check 'I acknowledge that AWS CloudFormation might create IAM resources'" -ForegroundColor White
    Write-Host "8. Click 'Submit'" -ForegroundColor White
    Write-Host ""
    Write-Host "Opening AWS Console..." -ForegroundColor Cyan
    Start-Process "https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/stackinfo?stackId=voicebharatai"
    exit 1
}

Write-Host "AWS CLI found. Updating stack..." -ForegroundColor Green
Write-Host ""

# Update the stack
try {
    aws cloudformation update-stack `
        --stack-name voicebharatai `
        --template-body file://backend/template.yaml `
        --capabilities CAPABILITY_NAMED_IAM `
        --region ap-south-1

    Write-Host ""
    Write-Host "Stack update initiated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitoring stack update status..." -ForegroundColor Cyan
    Write-Host "This will take 5-10 minutes. Press Ctrl+C to stop monitoring (update will continue)." -ForegroundColor Yellow
    Write-Host ""

    # Wait for stack update to complete
    aws cloudformation wait stack-update-complete `
        --stack-name voicebharatai `
        --region ap-south-1

    Write-Host ""
    Write-Host "✅ Stack update completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Voice Assistant is now ready to use!" -ForegroundColor Cyan
    Write-Host "Test it at: https://bharatvisionxai.vercel.app/assistant" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to update stack" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Please update manually via AWS Console (see instructions above)" -ForegroundColor Yellow
    exit 1
}
