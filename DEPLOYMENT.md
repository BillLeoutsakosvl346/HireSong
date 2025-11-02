# 🚀 HireSong Deployment Guide

## Fastest Deployment Method (Railway + Vercel)

### Prerequisites
- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- Your API keys ready (OpenAI, Fal, ElevenLabs)

---

## Part 1: Deploy Backend to Railway (5 minutes)

### Option A: Deploy via Railway Dashboard (Easiest)

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your HireSong repository
   - Railway will automatically detect it's a Python app

3. **Configure Root Directory**
   - In project settings, set "Root Directory" to `backend`
   - Railway will auto-detect `requirements.txt` and install dependencies

4. **Add Environment Variables**
   - Go to your project → Variables
   - Add these variables:
     ```
     OPENAI_API_KEY=your_key_here
     FAL_KEY=your_key_here
     ELEVENLABS_KEY=your_key_here
     GOOGLE_SHEET_ID=your_sheet_id_here
     ```

5. **Upload Google Service Account Key**
   - You have two options:
   
   **Option 1: Upload as file**
   - In Railway dashboard, go to your service
   - Click "Settings" → "Volumes"
   - Upload `hiresong-key.json` to `/app/backend/`
   
   **Option 2: Set as environment variable**
   - Copy the entire content of `hiresong-key.json`
   - Add a new variable: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - Paste the JSON content as the value
   - Update `backend/api/services/database.py` to read from this variable if file doesn't exist

6. **Deploy**
   - Railway will automatically deploy
   - Wait 2-3 minutes for build to complete
   - Copy your backend URL (e.g., `https://hiresong-production.up.railway.app`)

### Option B: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend
cd backend

# Initialize Railway project
railway init

# Deploy
railway up

# Add environment variables
railway variables set OPENAI_API_KEY=your_key
railway variables set FAL_KEY=your_key
railway variables set ELEVENLABS_KEY=your_key
railway variables set GOOGLE_SHEET_ID=your_sheet_id
```

---

## Part 2: Deploy Frontend to Vercel (3 minutes)

### Option A: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your HireSong repository
   - Vercel will auto-detect it's a Vite app

3. **Configure Build Settings**
   - Root Directory: `frontend`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `dist` (auto-detected)

4. **Add Environment Variable**
   - In project settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-railway-backend-url.railway.app`
   - Example: `VITE_API_URL=https://hiresong-production.up.railway.app`

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your app is live! 🎉

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: hiresong
# - Directory: ./ (current)
# - Build command: npm run build (auto-detected)
# - Output directory: dist (auto-detected)

# Add environment variable
vercel env add VITE_API_URL

# Paste your Railway backend URL when prompted
# Example: https://hiresong-production.up.railway.app

# Deploy to production
vercel --prod
```

---

## Part 3: Verify Deployment

1. **Test Backend**
   - Visit `https://your-railway-url.railway.app/docs`
   - You should see the FastAPI docs
   - Test the `/api/health` endpoint

2. **Test Frontend**
   - Visit your Vercel URL (e.g., `https://hiresong.vercel.app`)
   - Upload a selfie and CV
   - Enter a company URL
   - Click "Generate Your HireSong!"
   - Wait 2-3 minutes for the video

3. **Check Database**
   - Open your Google Sheet
   - You should see a new row for each pipeline run
   - Verify image URLs and video URLs are saved

---

## Troubleshooting

### Backend Issues

**Problem: Build fails with "missing dependencies"**
- Solution: Check that `requirements.txt` has all packages
- Run `pip freeze > requirements.txt` locally and commit

**Problem: "ModuleNotFoundError" in logs**
- Solution: Make sure Railway's root directory is set to `backend`

**Problem: "Google Sheets authentication failed"**
- Solution: Verify `hiresong-key.json` is uploaded or set as env variable

**Problem: Videos are taking too long**
- Solution: This is normal - the pipeline takes 2-3 minutes
- Railway has no timeout limits (unlike Vercel)

### Frontend Issues

**Problem: "Failed to fetch" or CORS errors**
- Solution: Verify `VITE_API_URL` environment variable is set correctly
- Make sure backend CORS allows all origins (already configured)

**Problem: Video player doesn't work**
- Solution: Check browser console for errors
- Verify the video URL is being returned from backend

**Problem: Build fails with "npm install" errors**
- Solution: Delete `node_modules` and `package-lock.json`, then commit
- Let Vercel rebuild from scratch

---

## Cost Breakdown

**Railway:**
- Free tier: $5 credit/month
- Your app will use ~$0.10-0.20 per video generation
- Approximately 25-50 videos/month on free tier

**Vercel:**
- Hobby (free): Unlimited bandwidth for frontend
- No usage limits for static sites

**API Costs:**
- OpenAI (GPT-5): ~$0.50 per video
- Fal.ai (images + videos): ~$2.00 per video
- ElevenLabs (music): ~$0.10 per video
- **Total per video: ~$2.60**

---

## Optional: Custom Domain

### Add Custom Domain to Vercel

1. Go to Vercel project → Settings → Domains
2. Add your domain (e.g., `hiresong.com`)
3. Update DNS records at your domain provider:
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```
4. Wait 5-10 minutes for DNS propagation

### Add Custom Domain to Railway

1. Go to Railway project → Settings → Domains
2. Click "Generate Domain" or "Custom Domain"
3. If using custom domain, add CNAME record:
   ```
   Type: CNAME
   Name: api
   Value: your-service.railway.app
   ```

---

## Production Checklist

- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] All environment variables set
- [ ] Google Sheets integration working
- [ ] Test video generation end-to-end
- [ ] Check Google Sheet for logged data
- [ ] (Optional) Custom domain configured
- [ ] Share your awesome hackathon project! 🎉

---

## Alternative: Single Platform Deployment

If you prefer deploying everything on one platform:

### Railway Only (Backend + Frontend)
- Deploy backend as a web service
- Deploy frontend as a separate web service
- Set `VITE_API_URL` to point to backend service

### Render Only (Backend + Frontend)
- Create backend web service
- Create frontend static site
- Both have generous free tiers

---

## Support

If you run into issues:
1. Check Railway logs: `railway logs`
2. Check Vercel logs: In dashboard → Deployments → Logs
3. Check browser console for frontend errors
4. Verify all API keys are correct
5. Make sure `hiresong-key.json` is accessible

**Good luck with your hackathon! 🚀**

