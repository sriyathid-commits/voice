# Deploy Frontend to Vercel
# This script commits and pushes changes to GitHub, triggering Vercel deployment

Write-Host "🚀 Deploying Voice for Bharat Frontend..." -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location -Path "frontend/web"

# Check git status
Write-Host "📋 Checking changes..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "📦 Adding all changes..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update: Add location detection and state filtering"
}
git commit -m $commitMessage

Write-Host ""
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push

Write-Host ""
Write-Host "✅ Deployment initiated!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Next steps:" -ForegroundColor Cyan
Write-Host "1. GitHub will receive the push"
Write-Host "2. Vercel will auto-detect changes"
Write-Host "3. Build will start (~2 minutes)"
Write-Host "4. Live at: https://bharatvisionxai.vercel.app"
Write-Host ""
Write-Host "🔗 Monitor deployment at: https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host ""

# Return to root
Set-Location -Path "../.."
