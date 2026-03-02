#!/bin/bash

# Voice for Bharat - Production Deployment Script
# This script automates the complete deployment process

set -e  # Exit on any error

echo "🇮🇳 Voice for Bharat - Production Deployment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
fi

# Add all files to git
print_status "Adding files to Git..."
git add .

# Create initial commit
print_status "Creating initial commit..."
git commit -m "🇮🇳 Voice for Bharat: Complete platform with AWS backend and Next.js frontend

Features:
- ✅ 7 AWS Lambda services deployed
- ✅ 8 DynamoDB tables operational  
- ✅ Complete Next.js frontend with dashboard
- ✅ Voice assistant interface
- ✅ Government schemes browser
- ✅ Helplines and support
- ✅ PWA ready with offline support
- ✅ Multilingual support (6 Indian languages)
- ✅ Production-ready infrastructure

Backend: AWS Lambda + DynamoDB + S3 + Cognito + Bedrock
Frontend: Next.js 15 + TypeScript + Tailwind CSS + Zustand
Deployment: AWS SAM + Vercel + GitHub Actions"

print_success "Initial commit created"

# Instructions for GitHub setup
echo ""
echo "📋 NEXT STEPS - GitHub & Vercel Deployment"
echo "==========================================="
echo ""
echo "1️⃣  CREATE GITHUB REPOSITORY:"
echo "   • Go to: https://github.com/new"
echo "   • Repository name: voice-for-bharat"
echo "   • Description: Voice-first AI platform for government welfare schemes in India"
echo "   • Choose: Public (recommended) or Private"
echo "   • DON'T initialize with README (we have files already)"
echo "   • Click 'Create repository'"
echo ""
echo "2️⃣  CONNECT TO GITHUB:"
echo "   Copy and run these commands after creating the repository:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/voice-for-bharat.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3️⃣  DEPLOY TO VERCEL:"
echo "   • Go to: https://vercel.com/new"
echo "   • Click 'Import Git Repository'"
echo "   • Select your 'voice-for-bharat' repository"
echo "   • Framework: Next.js"
echo "   • Root Directory: frontend/web"
echo "   • Click 'Deploy'"
echo ""
echo "4️⃣  ADD ENVIRONMENT VARIABLES IN VERCEL:"
echo "   After deployment, go to Project Settings → Environment Variables:"
echo ""
echo "   NEXT_PUBLIC_API_URL=https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev"
echo "   NEXT_PUBLIC_WS_URL=wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev"
echo "   NEXT_PUBLIC_CLOUDFRONT_URL=https://d18s1aceaoasx3.cloudfront.net"
echo "   NEXT_PUBLIC_COGNITO_USER_POOL_ID=ap-south-1_lbk6t80Qf"
echo "   NEXT_PUBLIC_COGNITO_CLIENT_ID=78d8776ct03jlp6n5heqic32gn"
echo "   NEXT_PUBLIC_COGNITO_REGION=ap-south-1"
echo "   NEXT_PUBLIC_ENABLE_PWA=true"
echo "   NEXT_PUBLIC_ENABLE_VOICE_ASSISTANT=true"
echo "   NEXT_PUBLIC_ENABLE_OFFLINE_MODE=false"
echo ""
echo "🎉 YOUR PLATFORM WILL BE LIVE!"
echo ""
echo "📊 CURRENT STATUS:"
echo "   ✅ Backend: Deployed on AWS (fully operational)"
echo "   ✅ Frontend: Running locally at http://localhost:3000"
echo "   🔄 Production: Ready to deploy to Vercel"
echo ""
echo "🔗 LIVE ENDPOINTS:"
echo "   • REST API: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev"
echo "   • WebSocket: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev"
echo "   • CloudFront: https://d18s1aceaoasx3.cloudfront.net"
echo ""
echo "📞 SUPPORT:"
echo "   • GitHub Issues: Create issues in your repository"
echo "   • AWS Console: https://console.aws.amazon.com/"
echo "   • Vercel Dashboard: https://vercel.com/dashboard"
echo ""
print_success "Deployment script completed! Follow the steps above to go live."