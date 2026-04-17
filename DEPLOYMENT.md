# DiagnoReport - Vercel Deployment Instructions

## Quick Start

### 1. Get Free Gemini API Key
- Visit: https://aistudio.google.com/app/apikeys
- Click "Create API Key"
- Copy the key (free tier, no credit card needed)

### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to project
cd diagnoreport

# Deploy
vercel deploy

# Follow prompts and choose your settings
```

### 3. Configure Environment Variable

**Option A: Via Vercel Dashboard**
1. Go to https://vercel.com/dashboard
2. Select your "diagnoreport" project
3. Go to Settings → Environment Variables
4. Add: `GEMINI_API_KEY` = `your-api-key-here`
5. Redeploy: `vercel deploy --prod`

**Option B: Via CLI**
```bash
vercel env add GEMINI_API_KEY
# Paste your API key when prompted

vercel deploy --prod
```

### 4. Test Live Deployment

```bash
# Test health check
curl https://your-project.vercel.app/api/health

# Generate report (replace with your URL)
curl -X POST https://your-project.vercel.app/api/generate_ddr \
  -H "Content-Type: application/json" \
  -d @sample_payload.json
```

## Local Testing

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key"

# Run locally
python app.py

# Visit http://localhost:5000
```

### Test with Sample Data
1. Open http://localhost:5000
2. Click "Load Sample Data"
3. Click "Generate Report"
4. View results in Report, JSON, or HTML tabs

## Repository Structure

```
ddr-report-system/
├── backend/                  # Core processing modules
│   ├── document_processor.py # Parse inspection/thermal reports
│   ├── gemini_processor.py  # AI-powered data analysis
│   └── ddr_generator.py      # Generate DDR structure
├── api/                      # Vercel serverless functions
│   ├── generate_ddr.py      # Main endpoint
│   ├── health.py             # Health check
│   └── samples.py            # Sample data endpoint
├── frontend/                 # Web interface
│   └── index.html            # Complete web app
├── sample_documents/         # Test data
│   ├── inspection_report.json
│   └── thermal_report.json
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── app.py                   # Local development server
└── README.md                # Documentation
```

## Key Features

✅ **No Frontend Build Step**: Pure HTML/JavaScript, no build needed
✅ **Serverless Compatible**: Works on Vercel's free tier
✅ **Free AI**: Google Gemini API free tier
✅ **CORS Enabled**: Works with cross-origin requests
✅ **Environment Variables**: Secure API key handling
✅ **Two Output Formats**: JSON and HTML

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"
**Solution**: 
1. Verify environment variable is set in Vercel dashboard
2. Redeploy after setting it: `vercel deploy --prod`
3. Check with: `vercel env ls`

### Issue: "Module not found" error
**Solution**:
1. Ensure requirements.txt is in project root
2. Vercel runs `pip install -r requirements.txt` automatically
3. Check Vercel build logs for errors

### Issue: Reports not generating
**Solution**:
1. Check Gemini API key is valid
2. Verify sample data loads: GET /api/samples
3. Check request format matches documentation
4. Review Vercel function logs

## API Endpoints

### POST /api/generate_ddr
Generate a DDR report

**Request:**
```json
{
  "inspection_report": {...},
  "thermal_report": {...},
  "property_address": "string",
  "inspection_date": "YYYY-MM-DD",
  "output_format": "json" or "html"
}
```

**Response:**
```json
{
  "status": "success",
  "ddr_report": {...}
}
```

### GET /api/health
Check service status

### GET /api/samples
Get sample inspection and thermal reports

## Performance Notes

- Free Gemini tier: 60 requests/minute
- Serverless cold starts: ~5-10 seconds
- Report generation: ~3-5 seconds (with AI processing)
- Frontend loads instantly

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Set GEMINI_API_KEY
3. ✅ Test with sample data
4. ✅ Upload custom inspection/thermal reports
5. ✅ Download generated reports
6. 🎥 Record Loom video
7. 📁 Create Google Drive folder with links

## Support

For issues:
1. Check Vercel build logs: `vercel logs`
2. Check function logs: Vercel Dashboard → Deployments → Runtime Logs
3. Test locally first: `python app.py`
4. Verify API key is valid at https://aistudio.google.com/app/apikeys

---

**Ready to deploy!** 🚀
