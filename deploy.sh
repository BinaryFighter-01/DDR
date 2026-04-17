#!/bin/bash
# Quick deployment script

echo "🚀 Deploying DiagnoReport to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

# Deploy
vercel deploy

echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Visit https://vercel.com/dashboard"
echo "2. Go to your project → Settings → Environment Variables"
echo "3. Add GEMINI_API_KEY with your Google Gemini API key"
echo "4. Redeploy: vercel deploy --prod"
echo ""
echo "💡 Get your API key: https://aistudio.google.com/app/apikeys"
