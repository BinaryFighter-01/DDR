# GitHub Repository Setup

## Initial Setup

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: DDR Report Generation system with Vercel deployment"

# 4. Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/ddr-report-system.git

# 5. Push to GitHub
git branch -M main
git push -u origin main
```

## GitHub Repository Description

```
AI-powered Detailed Diagnostic Report (DDR) generator that intelligently merges 
inspection and thermal imaging data to create professional client-ready reports.

Uses Google Gemini API (free) + Python backend + Vercel deployment.
```

## GitHub Topics

Add these topics to your repository:
- `ai`
- `generativeai`
- `gemini`
- `python`
- `vercel`
- `api`
- `inspection`
- `diagnostic`
- `building-inspection`
- `thermal-imaging`

## GitHub Actions Workflow (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_system.py
```

## README Badges

Add these to your GitHub README:

```markdown
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)
![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel-black)
[![Test Status](https://github.com/YOUR_USERNAME/ddr-report-system/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/ddr-report-system/actions)
```

## Deployment Shield

```markdown
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?logo=vercel)](https://vercel.com)
```

---

## For Submission

Include these links in your Google Drive folder:

1. **GitHub Repository**: `https://github.com/YOUR_USERNAME/ddr-report-system`
2. **Live Demo**: `https://your-project.vercel.app`
3. **Loom Video**: `https://loom.com/your-video-link`

---

## Keep Repository Clean

Files tracked by `.gitignore`:
- `.env` files
- `__pycache__/`
- `.venv/`, `venv/`
- `*.log`
- `.vercel/`

No environment variables or secrets in repo! ✅
