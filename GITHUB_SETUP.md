# GitHub Repository Setup Guide

## Step 1: Install Git (if not already installed)

Download and install Git from: https://git-scm.com/download/win

After installation, restart your terminal.

## Step 2: Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Repository

```bash
# Navigate to project root
cd C:\Users\yathi\voice

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Voice for Bharat platform with AWS backend and Next.js frontend"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `voice-for-bharat`
3. Description: `Voice-first AI platform for government welfare schemes in India`
4. Choose: Public or Private
5. DO NOT initialize with README (we already have one)
6. Click "Create repository"

## Step 5: Connect and Push to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/voice-for-bharat.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 6: Verify Upload

Visit: `https://github.com/YOUR_USERNAME/voice-for-bharat`

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. Click "Add" → "Add Existing Repository"
4. Select: `C:\Users\yathi\voice`
5. Click "Publish repository"
6. Choose name: `voice-for-bharat`
7. Click "Publish Repository"

## Troubleshooting

### Repository Too Large

If you get errors about repository size:

```bash
# Check repository size
git count-objects -vH

# Remove large files from history (if needed)
git filter-branch --tree-filter 'rm -rf node_modules' HEAD
```

### Authentication Issues

Use Personal Access Token instead of password:

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy token
5. Use token as password when pushing

## What Gets Uploaded

Based on `.gitignore`, these are EXCLUDED:
- `node_modules/`
- `.next/`
- `.venv/`
- `.aws-sam/`
- `.env.local`
- `__pycache__/`

These are INCLUDED:
- All source code (`frontend/`, `backend/`)
- Documentation (`.md` files)
- Configuration files
- Public assets

## Repository Size Estimate

Expected size: ~5-10 MB (without node_modules and build artifacts)

## After Pushing

Update `PRODUCTION_LINKS.md` with your GitHub URL:

```markdown
## GitHub Repository
- **URL**: https://github.com/YOUR_USERNAME/voice-for-bharat
```

## Quick Commands Reference

```bash
# Check status
git status

# Add specific files
git add filename

# Commit changes
git commit -m "Your message"

# Push changes
git push

# Pull latest changes
git pull

# View commit history
git log --oneline
```
