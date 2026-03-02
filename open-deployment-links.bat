@echo off
echo 🇮🇳 Voice for Bharat - Opening Deployment Links
echo =============================================
echo.
echo Opening GitHub and Vercel in your browser...
echo.

REM Open GitHub to create new repository
start https://github.com/new

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Open Vercel for deployment
start https://vercel.com/new

echo.
echo 📋 Quick Instructions:
echo.
echo 1. GITHUB (first tab):
echo    - Repository name: voice-for-bharat
echo    - Description: Voice-first AI platform for government welfare schemes in India
echo    - Public repository
echo    - Add README file
echo    - Create repository
echo.
echo 2. VERCEL (second tab):
echo    - Import your GitHub repository
echo    - Framework: Next.js
echo    - Root Directory: frontend/web
echo    - Add environment variables from .env.local
echo    - Deploy
echo.
echo 🎯 Your platform will be live in 5 minutes!
echo.
pause