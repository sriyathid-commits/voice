# Quick GitHub Setup - Voice for Bharat

## Option 1: Using GitHub Desktop (Easiest - No Git Installation Needed)

### Step 1: Download GitHub Desktop
Visit: https://desktop.github.com/
Download and install.

### Step 2: Sign In
Open GitHub Desktop and sign in with your GitHub account.

### Step 3: Add Repository
1. Click "File" → "Add local repository"
2. Click "Choose..." and select: `C:\Users\yathi\voice`
3. Click "Add Repository"

### Step 4: Create Repository on GitHub
1. Click "Publish repository" button
2. Name: `voice-for-bharat`
3. Description: `Voice-first AI platform for government welfare schemes in India`
4. Uncheck "Keep this code private" (or keep checked if you want it private)
5. Click "Publish Repository"

### Step 5: Done!
Your repository is now on GitHub. GitHub Desktop will show you the URL.

---

## Option 2: Using Git Command Line

### Step 1: Install Git
Download from: https://git-scm.com/download/win
Install with default settings.
Restart your terminal after installation.

### Step 2: Open PowerShell in Project Directory
```powershell
cd C:\Users\yathi\voice
```

### Step 3: Configure Git (First Time Only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Initialize and Commit
```powershell
git init
git add .
git commit -m "Initial commit: Voice for Bharat platform"
```

### Step 5: Create Repository on GitHub
1. Go to: https://github.com/new
2. Repository name: `voice-for-bharat`
3. Description: `Voice-first AI platform for government welfare schemes in India`
4. Choose Public or Private
5. DO NOT check "Initialize with README"
6. Click "Create repository"

### Step 6: Push to GitHub
Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/voice-for-bharat.git
git branch -M main
git push -u origin main
```

---

## Option 3: Manual Upload (If Repository is Too Large)

### Create a Lightweight Version

1. Create a new folder: `voice-for-bharat-lite`
2. Copy only these folders/files:
   - `frontend/web/src/` (source code only)
   - `backend/lambdas/` (Lambda functions)
   - `backend/shared/` (shared utilities)
   - `backend/template.yaml`
   - All `.md` documentation files
   - `README.md`
   - `.gitignore`

3. Upload this lighter version to GitHub

---

## What to Include in GitHub

✅ **Include:**
- Source code (`src/`, `lambdas/`)
- Configuration files (`.yaml`, `.json`, `.config.js`)
- Documentation (`.md` files)
- Public assets (`public/`)

❌ **Exclude (already in .gitignore):**
- `node_modules/`
- `.next/`
- `.venv/`
- `.aws-sam/`
- `.env.local`
- `__pycache__/`

---

## After GitHub Setup

Once your repository is on GitHub, you'll have a URL like:
`https://github.com/YOUR_USERNAME/voice-for-bharat`

Add this to your submission along with:
- **Vercel URL**: https://bharatvisionxai.vercel.app
- **GitHub URL**: https://github.com/YOUR_USERNAME/voice-for-bharat

---

## Need Help?

If you encounter issues:
1. Check that `.gitignore` is excluding large folders
2. Use GitHub Desktop for easier setup
3. Consider uploading a lightweight version with just source code

## Repository Size Check

Expected size without excluded folders: ~5-10 MB
If larger, you may need to exclude additional build artifacts.
