"""
API Usage Examples - Use these to test the deployed system
"""

# Example 1: Using Python requests
# Run: pip install requests

import json
import requests

# Your Vercel deployment URL
BASE_URL = "https://your-project.vercel.app"

# Load sample data
response = requests.get(f"{BASE_URL}/api/samples")
data = response.json()

inspection_report = data["inspection_report"]
thermal_report = data["thermal_report"]

# Generate DDR
payload = {
    "inspection_report": inspection_report,
    "thermal_report": thermal_report,
    "property_address": "2547 Maple Street, Denver, CO 80205",
    "inspection_date": "2026-04-10",
    "output_format": "json"
}

response = requests.post(
    f"{BASE_URL}/api/generate_ddr",
    json=payload,
    headers={"Content-Type": "application/json"}
)

result = response.json()
ddr_report = result["ddr_report"]

# Print report
print(json.dumps(ddr_report, indent=2))

---

# Example 2: Using cURL (command line)

curl -X POST https://your-project.vercel.app/api/generate_ddr \
  -H "Content-Type: application/json" \
  -d '{
    "inspection_report": {
      "type": "inspection_report",
      "property_address": "2547 Maple Street, Denver, CO 80205",
      "inspection_date": "2026-04-10",
      "areas": [
        {
          "name": "Roof",
          "observations": ["Missing shingles", "Water damage signs"],
          "issues": ["Potential water infiltration"]
        }
      ]
    },
    "thermal_report": {
      "type": "thermal_report",
      "findings": [
        {
          "area": "Roof",
          "temperature_range": "35-42°C",
          "anomalies": ["Hot spots at roof edges"]
        }
      ]
    },
    "property_address": "2547 Maple Street, Denver, CO 80205",
    "inspection_date": "2026-04-10",
    "output_format": "json"
  }'

---

# Example 3: JavaScript/Frontend

async function generateDDR() {
    const inspection = {
        "type": "inspection_report",
        "property_address": "123 Main St",
        "inspection_date": "2026-04-10",
        "areas": [...]
    };
    
    const thermal = {
        "type": "thermal_report",
        "findings": [...]
    };
    
    const response = await fetch('/api/generate_ddr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            inspection_report: inspection,
            thermal_report: thermal,
            property_address: "123 Main St",
            inspection_date: "2026-04-10",
            output_format: "json"
        })
    });
    
    const result = await response.json();
    console.log(result.ddr_report);
}

---

# Example 4: Getting Sample Data

# Using Python
import requests
response = requests.get('https://your-project.vercel.app/api/samples')
samples = response.json()
print(samples["inspection_report"])
print(samples["thermal_report"])

# Using cURL
curl https://your-project.vercel.app/api/samples | jq .

# Using JavaScript
fetch('/api/samples')
    .then(r => r.json())
    .then(data => console.log(data))

---

# Example 5: Health Check

# Python
import requests
response = requests.get('https://your-project.vercel.app/api/health')
print(response.json())
# Output: {"status": "healthy", "service": "DiagnoReport", "version": "1.0.0"}

# cURL
curl https://your-project.vercel.app/api/health

---

# Example 6: HTML Output

payload = {
    "inspection_report": {...},
    "thermal_report": {...},
    "output_format": "html"  # Instead of "json"
}

response = requests.post(
    'https://your-project.vercel.app/api/generate_ddr',
    json=payload
)

result = response.json()
html_content = result["html"]

# Save to file
with open('report.html', 'w') as f:
    f.write(html_content)

# Open in browser
import webbrowser
webbrowser.open('report.html')

---

# Input Format Reference

Inspection Report Structure:
{
  "type": "inspection_report",
  "property_address": "string",
  "inspection_date": "YYYY-MM-DD",
  "inspector_name": "string",
  "areas": [
    {
      "name": "Area Name",
      "observations": ["obs1", "obs2"],
      "issues": ["issue1", "issue2"]
    }
  ],
  "images": [
    {
      "area": "Area Name",
      "url": "path/to/image.jpg",
      "description": "Description"
    }
  ]
}

Thermal Report Structure:
{
  "type": "thermal_report",
  "property_address": "string",
  "inspection_date": "YYYY-MM-DD",
  "findings": [
    {
      "area": "Area Name",
      "temperature_range": "15-45°C",
      "analysis": "Description",
      "anomalies": ["anomaly1", "anomaly2"],
      "severity": "HIGH"
    }
  ],
  "images": [
    {
      "area": "Area Name",
      "url": "path/to/image.jpg",
      "temperature": "42°C"
    }
  ]
}

---

# Output Format Reference

DDR Report Structure:
{
  "metadata": {
    "generated_date": "ISO timestamp",
    "property_address": "string",
    "inspection_date": "string",
    "report_type": "DDR"
  },
  "sections": {
    "property_issue_summary": "text",
    "area_wise_observations": "text",
    "probable_root_cause": "text",
    "severity_assessment": "text",
    "recommended_actions": "text",
    "additional_notes": "text",
    "missing_or_unclear": "text"
  },
  "images": [
    {
      "source": "inspection|thermal",
      "url": "string",
      "description": "string",
      "area": "string"
    }
  ],
  "data_quality": {
    "contradictions": [],
    "gaps": [],
    "unexplained_findings": []
  }
}

---

# Testing with Postman

1. Create new POST request
2. URL: https://your-project.vercel.app/api/generate_ddr
3. Headers:
   - Content-Type: application/json
4. Body (raw JSON):
   {
     "inspection_report": {...},
     "thermal_report": {...},
     "property_address": "...",
     "inspection_date": "...",
     "output_format": "json"
   }
5. Send and see response

---

# Troubleshooting API Calls

Error: 400 - Bad Request
→ Check JSON is valid and has inspection_report + thermal_report

Error: 500 - Server Error
→ Check GEMINI_API_KEY is set in Vercel environment variables

Error: 401 - Unauthorized
→ API key might be invalid, regenerate at https://aistudio.google.com/app/apikeys

Error: 503 - Service Unavailable
→ Vercel function is cold starting, try again in 10-15 seconds

Slow Response (10+ seconds)
→ First request is slow due to cold start, subsequent requests faster
→ Free Gemini tier has 60 requests/minute limit

---

# Load Testing

# Using Apache Bench (ab)
ab -n 10 -c 1 -p payload.json -T application/json \
  https://your-project.vercel.app/api/generate_ddr

# Using hey (faster, modern)
hey -n 10 -m POST -H "Content-Type: application/json" \
  -d @payload.json \
  https://your-project.vercel.app/api/generate_ddr

---

Ready to test? Use the examples above! 🚀
