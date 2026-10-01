# Install Prerequisites for Voice for Bharat Deployment

## 🎯 What You Need to Install

Before deploying, you need these tools installed on your Windows machine:
1. AWS CLI
2. AWS SAM CLI  
3. Python 3.11+ (you already have this ✓)
4. Node.js 18+ (you already have this ✓)

---

## 📥 Step 1: Install AWS CLI

### Option A: Download Installer (Recommended)
1. Download AWS CLI v2 for Windows:
   https://awscli.amazonaws.com/AWSCLIV2.msi

2. Run the installer
3. Click through the installation wizard
4. Restart PowerShell after installation

### Option B: Using Chocolatey
```powershell
choco install awscli
```

### Verify Installation
```powershell
aws --version
# Should show: aws-cli/2.x.x Python/3.x.x Windows/10
```

---

## 📥 Step 2: Configure AWS Credentials

After installing AWS CLI, configure your credentials:

```powershell
aws configure
```

You'll be prompted to enter:
1. **AWS Access Key ID**: [Your Access Key from AWS Console]
2. **AWS Secret Access Key**: [Your Secret Key]
3. **Default region name**: `ap-south-1`
4. **Default output format**: `json`

### Where to Get AWS Credentials

1. Go to AWS Console: https://console.aws.amazon.com/
2. Click your name (top right) → Security credentials
3. Scroll to "Access keys"
4. Click "Create access key"
5. Download and save the credentials
6. Use them in `aws configure`

### Verify AWS Configuration
```powershell
aws sts get-caller-identity
```

Should return your AWS account information.

---

## 📥 Step 3: Install AWS SAM CLI

### Option A: Download Installer (Recommended)
1. Download AWS SAM CLI for Windows:
   https://github.com/aws/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi

2. Run the installer
3. Click through the installation wizard
4. Restart PowerShell after installation

### Option B: Using Chocolatey
```powershell
choco install aws-sam-cli
```

### Verify Installation
```powershell
sam --version
# Should show: SAM CLI, version 1.x.x
```

---

## ✅ Verify All Prerequisites

Run this command to check everything:

```powershell
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check AWS CLI
try {
    $awsVersion = aws --version 2>&1
    Write-Host "[OK] AWS CLI: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] AWS CLI" -ForegroundColor Red
}

# Check SAM CLI
try {
    $samVersion = sam --version 2>&1
    Write-Host "[OK] SAM CLI: $samVersion" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] SAM CLI" -ForegroundColor Red
}

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] Python" -ForegroundColor Red
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] Node.js" -ForegroundColor Red
}

# Check Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "[OK] Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] Git" -ForegroundColor Red
}

# Check AWS credentials
try {
    $awsIdentity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "[OK] AWS Credentials configured for Account: $($awsIdentity.Account)" -ForegroundColor Green
} catch {
    Write-Host "[MISSING] AWS credentials not configured" -ForegroundColor Red
    Write-Host "Run: aws configure" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "If all checks passed, you're ready to deploy!" -ForegroundColor Green
```

---

## 🚀 After Installing Prerequisites

Once all tools are installed, run the deployment:

```powershell
.\deploy-simple.ps1
```

This will:
1. ✅ Build all Lambda functions
2. ✅ Deploy backend to AWS (20-30 minutes)
3. ✅ Generate environment variables
4. ✅ Build frontend locally to verify
5. ✅ Prepare for Vercel deployment

---

## 🆘 Troubleshooting

### "aws : The term 'aws' is not recognized"
**Solution**: Restart PowerShell after installing AWS CLI, or add to PATH manually

### "Cannot find AWS credentials"
**Solution**: Run `aws configure` and enter your credentials

### "SAM CLI not found"
**Solution**: Download from https://github.com/aws/aws-sam-cli/releases/latest

### "Access Denied" when running AWS commands
**Solution**: Check your IAM user has AdministratorAccess policy

---

## 📞 AWS Account Setup

If you don't have an AWS account:

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the signup process
4. You'll get 12 months of Free Tier
5. Create an IAM user with admin access
6. Use those credentials in `aws configure`

---

## 💡 Quick Install Script

Copy and paste this into PowerShell (as Administrator):

```powershell
# Install Chocolatey (if not installed)
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install AWS CLI and SAM CLI
choco install awscli aws-sam-cli -y

Write-Host ""
Write-Host "Installation complete! Please:" -ForegroundColor Green
Write-Host "1. Restart PowerShell" -ForegroundColor Yellow
Write-Host "2. Run: aws configure" -ForegroundColor Yellow
Write-Host "3. Run: .\deploy-simple.ps1" -ForegroundColor Yellow
```

---

## ✅ You're Ready When...

All these commands work:
- ✅ `aws --version`
- ✅ `sam --version`
- ✅ `python --version`
- ✅ `node --version`
- ✅ `aws sts get-caller-identity`

Then run: `.\deploy-simple.ps1`

---

**Estimated Time**: 15-20 minutes to install and configure everything
**Then**: 30-40 minutes for actual deployment
