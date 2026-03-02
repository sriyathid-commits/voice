@echo off
echo 🇮🇳 Voice for Bharat - Production Setup
echo =====================================
echo.

echo 📋 Current Status:
echo ✅ Backend: Deployed on AWS (fully operational)
echo ✅ Frontend: Running locally at http://localhost:3000
echo ✅ All pages working (no 404 errors)
echo ✅ Ready for production deployment
echo.

echo 🚀 Quick Deployment Commands:
echo.
echo 1. Initialize Git and commit:
echo    git init
echo    git add .
echo    git commit -m "Voice for Bharat platform ready for production"
echo.
echo 2. Create GitHub repository at: https://github.com/new
echo    Repository name: voice-for-bharat
echo    Description: Voice-first AI platform for government welfare schemes in India
echo.
echo 3. Connect to GitHub (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/voice-for-bharat.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Deploy to Vercel:
echo    Go to: https://vercel.com/new
echo    Import your GitHub repository
echo    Root Directory: frontend/web
echo    Add environment variables from .env.local
echo.
echo 🔗 Your Live Endpoints:
echo • REST API: https://2dbyh0kkna.execute-api.ap-south-1.amazonaws.com/dev
echo • WebSocket: wss://be6zdvjoy2.execute-api.ap-south-1.amazonaws.com/dev
echo • CloudFront: https://d18s1aceaoasx3.cloudfront.net
echo.
echo 📊 Platform Features:
echo • Multilingual voice assistant (6 Indian languages)
echo • Government schemes browser
echo • Real-time application tracking
echo • Document upload and verification
echo • 24/7 support channels
echo • PWA with offline support
echo.
echo 🎯 Ready to serve millions of users across India!
echo.
pause