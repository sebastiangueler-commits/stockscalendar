#!/bin/bash

echo "🚀 Deploying Magic Stocks Calendar to Production..."

# Build frontend for production
echo "📦 Building frontend..."
cd frontend
npm run build
cd ..

# Check if build was successful
if [ -d "frontend/build" ]; then
    echo "✅ Frontend build successful!"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

# Deploy to Vercel (Frontend)
echo "🌐 Deploying frontend to Vercel..."
npx vercel --prod

# Deploy to Heroku (Backend)
echo "🔧 Deploying backend to Heroku..."
git add .
git commit -m "Deploy to production"
git push heroku main

echo "🎉 Deployment complete!"
echo "Frontend: https://your-app.vercel.app"
echo "Backend: https://your-backend.herokuapp.com"
