# Check CloudFormation Stack Status

Write-Host "Checking stack status..." -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is available
$awsCommand = Get-Command aws -ErrorAction SilentlyContinue

if (-not $awsCommand) {
    Write-Host "AWS CLI not found. Please check manually:" -ForegroundColor Yellow
    Write-Host "https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/stackinfo?stackId=voicebharatai" -ForegroundColor White
    Write-Host ""
    Write-Host "Look for status: UPDATE_COMPLETE" -ForegroundColor Green
    Write-Host ""
    Start-Process "https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/stackinfo?stackId=voicebharatai"
    exit 0
}

# Get stack status
$status = aws cloudformation describe-stacks --stack-name voicebharatai --region ap-south-1 --query "Stacks[0].StackStatus" --output text 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error checking stack status" -ForegroundColor Red
    exit 1
}

Write-Host "Current Status: $status" -ForegroundColor Yellow
Write-Host ""

if ($status -eq "UPDATE_COMPLETE") {
    Write-Host "✅ Stack update completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Voice Assistant is now ready!" -ForegroundColor Cyan
    Write-Host "Test it at: https://bharatvisionxai.vercel.app/assistant" -ForegroundColor White
    Write-Host ""
} elseif ($status -eq "UPDATE_IN_PROGRESS") {
    Write-Host "⏳ Stack update is still in progress..." -ForegroundColor Yellow
    Write-Host "This usually takes 5-10 minutes." -ForegroundColor White
    Write-Host ""
    Write-Host "Please wait and try the voice assistant again in a few minutes." -ForegroundColor Cyan
    Write-Host ""
} elseif ($status -like "*FAILED*" -or $status -like "*ROLLBACK*") {
    Write-Host "❌ Stack update failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the Events tab in CloudFormation console for details:" -ForegroundColor Yellow
    Write-Host "https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/stackinfo?stackId=voicebharatai" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Status: $status" -ForegroundColor White
    Write-Host ""
}
