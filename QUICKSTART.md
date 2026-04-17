# Getting Started - Quick Reference

## 🚀 Fast Track Deployment (5 minutes)

### Step 1: Get Gemini API Key (Free, 2 min)
```bash
# Visit: https://aistudio.google.com/app/apikeys
# Click "Create API Key"
# No credit card needed!
```

### Step 2: Deploy to Vercel (2 min)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel deploy

# Choose your settings when prompted
```

### Step 3: Configure API Key (1 min)
1. Go to https://vercel.com/dashboard
2. Click your "diagnoreport" project
3. Settings → Environment Variables
4. Add: `GEMINI_API_KEY` = `[your-key-from-step-1]`

### Step 4: Redeploy (1 min)
```bash
vercel deploy --prod
```

**Done!** Your DiagnoReport is live! 🎉

---

## 🧪 Local Testing (Before Deployment)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export GEMINI_API_KEY="your-gemini-api-key"

# 3. Run locally
python app.py

# 4. Open http://localhost:5000 in browser
# 5. Click "Load Sample Data"
# 6. Click "Generate DDR Report"
```

---

## 📦 Project Contents

**Backend (Python)**
- `backend/document_processor.py` - Parses inspection/thermal reports
- `backend/gemini_processor.py` - AI analysis & data merging
- `backend/ddr_generator.py` - Generates structured DDR

**Frontend**
- `frontend/index.html` - Complete web interface (no build needed!)

**API (Vercel)**
- `api/generate_ddr.py` - Main endpoint
- `api/health.py` - Health check
- `api/samples.py` - Sample data

**Samples**
- `sample_documents/inspection_report.json` - Example inspection
- `sample_documents/thermal_report.json` - Example thermal data

---

## 🎯 What It Does

**Input**: Two JSON documents
- Inspection Report (areas, issues, observations)
- Thermal Report (temperature findings, anomalies)

**Processing**:
- Extracts all observations and findings
- Uses Gemini AI to merge and correlate data
- Identifies conflicts and missing information
- Calculates severity ratings
- Generates actionable recommendations

**Output**: Professional DDR (Detailed Diagnostic Report)
```
1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing/Unclear Information
```

Available in JSON or HTML format with images embedded.

---

## 🎬 For Your Video (Key Points)

Show viewers:
1. **Upload** inspection and thermal reports (or use sample data)
2. **Click** "Generate DDR Report"
3. **See** professional report generated in 5-10 seconds
4. **Download** as JSON or HTML
5. **Explain**:
   - How it merges two data sources
   - Identifies correlations (e.g., thermal + physical issues)
   - Handles conflicts and missing data
   - Generates severity ratings
   - Makes it generalizable (not hardcoded)

---

## ❓ Troubleshooting

**Issue**: "GEMINI_API_KEY not configured"
- Make sure it's set in Vercel Environment Variables
- Redeploy after adding it: `vercel deploy --prod`

**Issue**: Slow response
- First request may take 10-15s due to cold start
- Subsequent requests are faster

**Issue**: Tests failing locally
- Run: `python test_system.py` to diagnose
- Check API key is valid

---

## 📊 Tech Stack

- **Backend**: Python 3.11
- **AI**: Google Gemini API (free tier)
- **Frontend**: HTML5 + Vanilla JavaScript (no build)
- **Deployment**: Vercel (serverless)
- **Data**: JSON format

---

## 🔗 Useful Links

- Gemini API: https://aistudio.google.com/app/apikeys
- Vercel Dashboard: https://vercel.com/dashboard
- Project Docs: See README.md
- Deployment Guide: See DEPLOYMENT.md

---

## 💡 Pro Tips

1. **Test locally first** with `python app.py` before deploying
2. **Use sample data** to demo without uploading files
3. **Check Vercel logs** if deployment fails: `vercel logs`
4. **API key not needed locally** if you just test the frontend structure
5. **Verify endpoint** works: `curl https://your-project.vercel.app/api/health`

---

**Ready?** Start with Step 1 above! 🚀
