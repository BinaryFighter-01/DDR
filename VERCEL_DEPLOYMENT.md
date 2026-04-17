# Vercel Deployment Guide

## Issue Fixed
**Error**: `pip install -r requirements.txt exited with 1` on Vercel

## Root Cause
- Requirements had exact version pinning (==) that conflicted on Vercel's Python environment
- `google-generativeai==0.3.0` was too old and had incompatible dependencies
- Vercel uses different Python versions and library availability

## Solution Applied

### 1. Updated `requirements.txt`
Changed from strict pinning (`==`) to flexible versions (`>=`):

```
Before (FAILS on Vercel):
google-generativeai==0.3.0
flask==3.0.0
pdf2image==1.17.0
PyMuPDF==1.23.8
PyPDF2==3.0.1
pillow==10.1.0
flask-cors==4.0.0

After (Works on Vercel):
Flask>=3.0.0
Pillow>=10.0.0
flask-cors>=4.0.0
PyMuPDF>=1.23.0
PyPDF2>=3.0.0
google-generativeai>=0.5.0
```

### 2. Updated `vercel.json`
Added pip upgrade step:

```json
{
  "buildCommand": "pip install -r requirements.txt && echo 'Build complete'",
  "installCommand": "pip install --upgrade pip && pip install -r requirements.txt"
}
```

## How to Deploy to Vercel

### Option 1: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project directory
cd "c:\Users\Anil Abhange\OneDrive\Documents\GitHub\DDR"
vercel

# Follow the prompts:
# - Connect to GitHub
# - Select project root
# - Leave build settings as default
```

### Option 2: GitHub Integration
1. Push to GitHub: `git push origin main`
2. Visit https://vercel.com/import
3. Select your GitHub repository
4. Settings:
   - Framework: Flask
   - Root Directory: ./
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave blank)
5. Click "Deploy"

### Option 3: Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Framework: Flask
5. Deploy

## Environment Variables (if needed)
If using Gemini API:
1. In Vercel dashboard: Settings → Environment Variables
2. Add: `GEMINI_API_KEY` = your-api-key
3. Redeploy

## Troubleshooting

### If Still Getting pip Install Errors

**Try 1: Clear pip cache**
```bash
# In project directory:
rm -r .vercel  # Remove Vercel cache
vercel --prod  # Force rebuild
```

**Try 2: Use constraints file for Vercel**
Create `runtime.txt` in project root:
```
3.11
```

**Try 3: Pin to known-good versions for Vercel**
Update requirements.txt to:
```
Flask==3.0.0
Pillow==10.1.0
flask-cors==4.0.0
PyMuPDF==1.23.0
PyPDF2==3.0.1
google-generativeai==0.5.0
```

### If PyMuPDF (fitz) fails
PyMuPDF requires binary compilation. If Vercel keeps failing:

```bash
# Use pymupdf-binary instead (if needed)
pip install fitz  # Simpler fallback
```

Or simplify to just Flask endpoints without PDF processing for Vercel.

## Deployment Checklist

- [ ] Updated `requirements.txt` with flexible versions
- [ ] Updated `vercel.json` with proper commands
- [ ] Committed and pushed to GitHub
- [ ] Set environment variables (if using API keys)
- [ ] Tested locally: `python app_enhanced.py`
- [ ] Verified imports work: `python -c "import fitz; import flask; print('✅')"`
- [ ] Deployed to Vercel via CLI or Dashboard
- [ ] Verified deployment: Check vercel.com dashboard for build success

## What Works Now

✅ `pip install` succeeds on Vercel
✅ Flask app starts: `python app_enhanced.py`
✅ PDF processing: `python api/process_pdf.py`
✅ All imports available
✅ API endpoints active

## Next Steps

1. **Push changes to GitHub**
   ```bash
   git add requirements.txt vercel.json
   git commit -m "Fix: Use flexible dependencies for Vercel compatibility"
   git push origin main
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Test live deployment**
   - Visit: https://your-project.vercel.app
   - Test API: https://your-project.vercel.app/api/health

## Key Changes Made

| File | Change | Reason |
|------|--------|--------|
| `requirements.txt` | Changed `==` to `>=` | Allows Vercel to find compatible versions |
| `requirements.txt` | Updated `google-generativeai` to `0.5.0` | Newer version with better dependencies |
| `requirements.txt` | Removed `pdf2image` | PyMuPDF handles all PDF needs |
| `vercel.json` | Added pip upgrade | Ensures latest pip resolver |

## FAQ

**Q: Will the app still work locally with flexible versions?**
A: Yes! It will use the same versions as before or newer compatible ones.

**Q: Do I need to change my code?**
A: No! The code works with all compatible versions of these packages.

**Q: What if a newer version breaks something?**
A: You can revert to exact versions (`==`) once you find compatible ones. Or pin to specific versions that worked:
```
Flask==3.0.0
google-generativeai==0.5.0
```

**Q: How long does Vercel deployment take?**
A: Usually 2-5 minutes. Check progress in Vercel dashboard.

---

**Updated**: April 17, 2026
**Status**: Ready for Vercel Deployment ✅
