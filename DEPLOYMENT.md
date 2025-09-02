# 🚀 Deployment Guide - Magic Stocks Calendar

## 📋 Prerequisites

1. **Git** installed and configured
2. **Node.js 16+** installed
3. **Python 3.8+** installed
4. **Vercel CLI** installed (`npm i -g vercel`)
5. **Heroku CLI** installed
6. **GitHub account** for repository hosting

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Repository
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/magic-stocks-calendar.git
git push -u origin main
```

### Step 2: Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name: magic-stocks-calendar
# - Directory: ./frontend/build
# - Override settings? N
```

### Step 3: Configure Environment Variables
In Vercel dashboard:
1. Go to your project settings
2. Add environment variable:
   - `REACT_APP_API_URL` = `https://your-backend-url.herokuapp.com`

## 🔧 Backend Deployment (Heroku)

### Step 1: Prepare Backend
```bash
# Create requirements.txt if not exists
pip freeze > requirements.txt

# Create Procfile
echo "web: python app.py" > Procfile

# Create runtime.txt
echo "python-3.9.18" > runtime.txt
```

### Step 2: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create magic-stocks-backend

# Add Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git add .
git commit -m "Deploy backend"
git push heroku main
```

### Step 3: Configure Environment Variables
```bash
# Set environment variables
heroku config:set API_BASE_URL=https://magic-stocks-backend.herokuapp.com
heroku config:set PYTHONPATH=/app
```

## 🔄 Automated Deployment

### Using the Deploy Script
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Build
        run: |
          cd frontend
          npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "magic-stocks-backend"
          heroku_email: "your-email@example.com"
```

## 🔧 Configuration

### Frontend Environment Variables
```bash
REACT_APP_API_URL=https://your-backend-url.herokuapp.com
REACT_APP_PAYPAL_EMAIL=malukelbasics@gmail.com
```

### Backend Environment Variables
```bash
API_BASE_URL=https://your-backend-url.herokuapp.com
PYTHONPATH=/app
PORT=8001
```

## 📊 Monitoring

### Vercel Analytics
- Enable in Vercel dashboard
- Monitor performance and user behavior
- Track conversion rates

### Heroku Monitoring
```bash
# View logs
heroku logs --tail

# Monitor performance
heroku ps:scale web=1

# Check app status
heroku ps
```

## 🔒 Security

### SSL Certificates
- Vercel provides automatic SSL
- Heroku provides automatic SSL
- Both use Let's Encrypt

### Environment Variables
- Never commit sensitive data
- Use platform-specific secret management
- Rotate keys regularly

## 📈 Performance Optimization

### Frontend
- Enable Vercel's Edge Network
- Use CDN for static assets
- Implement lazy loading
- Optimize images

### Backend
- Use Heroku's performance dynos
- Implement caching
- Database connection pooling
- API rate limiting

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check Node.js version
   node --version
   
   # Clear npm cache
   npm cache clean --force
   
   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Backend Deployment Issues**
   ```bash
   # Check Python version
   python --version
   
   # Verify requirements.txt
   pip install -r requirements.txt
   
   # Check Heroku logs
   heroku logs --tail
   ```

3. **Environment Variables**
   ```bash
   # Verify Vercel env vars
   vercel env ls
   
   # Verify Heroku env vars
   heroku config
   ```

## 📞 Support

- **Vercel Support**: https://vercel.com/support
- **Heroku Support**: https://help.heroku.com
- **Documentation**: See README.md

---

**Ready to deploy!** 🚀 Your Magic Stocks Calendar will be live and ready to generate revenue!
