# 🚀 Deployment Guide - Magic Stocks Calendar

## 📋 Prerequisites
- GitHub account
- Railway/Render account (for backend)
- PayPal Developer account (already configured)

## 🌐 Frontend Deployment (GitHub Pages)

### Step 1: Enable GitHub Pages
1. Go to your GitHub repository: `https://github.com/sebastiangueler-commits/stockscalendar`
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Select **gh-pages** branch
6. Click **Save**

### Step 2: Access Your Live Frontend
- Your frontend will be available at: `https://sebastiangueler-commits.github.io/stockscalendar/`

## ⚙️ Backend Deployment (Railway)

### Step 1: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your `stockscalendar` repository
5. Railway will automatically detect it's a Python app

### Step 2: Configure Environment Variables
In Railway dashboard, add these environment variables:
```
FLASK_ENV=production
PAYPAL_CLIENT_ID=AU92SQfA-D5YaqaArq7lSakdZmJI9e4CIcsZWYM2pnIEfYQ0dM1tAgd61QWOq1jBt_sbHdaXaHw9WK_-
PAYPAL_CLIENT_SECRET=ECHaorssV-zxllaXFJ14n14flrNDkvYS_Uqbk3mx0P6nwQzH2Vi0GApWCYGjTJTgnol4ahhcUL8WiiLg
```

### Step 3: Update Frontend URL
1. Get your Railway backend URL (e.g., `https://stockscalendar-production.up.railway.app`)
2. Update `index.html` line 1195:
```javascript
const API_BASE = 'https://your-railway-url.up.railway.app';
```

## 🔧 Alternative: Render.com

### Step 1: Deploy to Render
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub
3. Click **New** → **Web Service**
4. Connect your GitHub repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

### Step 2: Create requirements.txt
```bash
pip freeze > requirements.txt
```

## 📱 Testing Your Deployment

### Frontend Test
1. Visit: `https://sebastiangueler-commits.github.io/stockscalendar/`
2. Check if the loading screen appears
3. Try to login (use admin/admin)

### Backend Test
1. Visit: `https://your-backend-url.com/api/stats`
2. Should return JSON with signal counts

### PayPal Test
1. Try to register a new user
2. Select a plan
3. PayPal buttons should appear
4. Test payment flow (use PayPal sandbox for testing)

## 🚨 Important Notes

### Security
- Never commit real PayPal credentials to public repos
- Use environment variables for sensitive data
- Enable HTTPS for all production URLs

### CORS Configuration
If you get CORS errors, update `app.py`:
```python
CORS(app, origins=["https://sebastiangueler-commits.github.io"])
```

### Database
- Railway/Render will provide a persistent database
- Your local SQLite file won't be used in production

## 🔄 Updates

To update your deployment:
1. Make changes to your code
2. Commit and push to GitHub
3. Railway/Render will auto-deploy
4. GitHub Pages will auto-update

## 📞 Support

If you encounter issues:
1. Check Railway/Render logs
2. Check browser console for errors
3. Verify environment variables
4. Test API endpoints directly

---

**Your Magic Stocks Calendar will be live at:**
- Frontend: `https://sebastiangueler-commits.github.io/stockscalendar/`
- Backend: `https://your-backend-url.com`
