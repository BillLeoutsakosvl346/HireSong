# 🚀 Deployment Checklist

## What Was Changed for Deployment

### ✅ Files Modified:

1. **`backend/main.py`**
   - Updated CORS to allow all origins (`allow_origins=["*"]`)
   - This lets your frontend (on any domain) talk to your backend

2. **`frontend/src/App.jsx`**
   - Added `API_URL` constant that reads from environment variable
   - Changed `/api/generate` to `${API_URL}/api/generate`
   - Now works with both local and deployed backend

3. **`README.md`**
   - Added deployment section with quick overview
   - Links to full deployment guide

### ✅ Files Created:

1. **`DEPLOYMENT.md`**
   - Complete step-by-step deployment guide
   - Railway + Vercel instructions
   - Troubleshooting section
   - Cost breakdown

2. **`backend/Procfile`**
   - Tells Railway how to start the backend server

3. **`backend/nixpacks.toml`**
   - Specifies Python version and ffmpeg dependency
   - Railway uses this for building

4. **`frontend/vercel.json`**
   - Configures Vercel build and routing
   - Handles SPA navigation

---

## Quick Deployment Steps

### Prerequisites Checklist:
- [ ] GitHub account
- [ ] Railway account (https://railway.app)
- [ ] Vercel account (https://vercel.com)
- [ ] All API keys ready:
  - [ ] `OPENAI_API_KEY`
  - [ ] `FAL_KEY`
  - [ ] `ELEVENLABS_KEY`
  - [ ] `GOOGLE_SHEET_ID`
- [ ] `hiresong-key.json` file

---

## Deploy Backend (Railway)

### Option 1: Railway Dashboard (Easiest)

1. Go to https://railway.app
2. New Project → Deploy from GitHub repo
3. Select HireSong repo
4. Set Root Directory: `backend`
5. Add environment variables:
   ```
   OPENAI_API_KEY=xxx
   FAL_KEY=xxx
   ELEVENLABS_KEY=xxx
   GOOGLE_SHEET_ID=xxx
   ```
6. Upload `hiresong-key.json` (or set as env variable)
7. Deploy! (auto-detects Python)
8. Copy your backend URL (e.g., `https://hiresong-production.railway.app`)

### Option 2: Railway CLI (Fastest)

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway init
railway up

# Add environment variables via dashboard or CLI
railway variables set OPENAI_API_KEY=xxx
railway variables set FAL_KEY=xxx
railway variables set ELEVENLABS_KEY=xxx
railway variables set GOOGLE_SHEET_ID=xxx
```

---

## Deploy Frontend (Vercel)

### Option 1: Vercel Dashboard

1. Go to https://vercel.com
2. New Project → Import HireSong repo
3. Root Directory: `frontend`
4. Build settings (auto-detected):
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add environment variable:
   - `VITE_API_URL` = `https://your-railway-url.railway.app`
6. Deploy!

### Option 2: Vercel CLI

```bash
# Install CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Add environment variable
vercel env add VITE_API_URL

# Enter your Railway backend URL when prompted

# Deploy to production
vercel --prod
```

---

## Verify Deployment

### Test Backend:
```bash
# Health check
curl https://your-backend.railway.app/api/health

# API docs
open https://your-backend.railway.app/docs
```

### Test Frontend:
1. Open your Vercel URL
2. Upload selfie and CV
3. Enter company URL
4. Generate video
5. Check Google Sheet for logged data

---

## Post-Deployment

### Commit Your Changes:

```bash
git add .
git commit -m "Add deployment configuration for Railway and Vercel"
git push origin main
```

### Update Your Frontend Environment Variable:

If you deploy frontend before backend, you'll need to update:
- Vercel Dashboard → Your Project → Settings → Environment Variables
- Update `VITE_API_URL` to your Railway backend URL
- Redeploy frontend

---

## Troubleshooting

### Backend Issues:

**"Build failed"**
- Check Railway logs
- Verify `requirements.txt` has all dependencies
- Make sure root directory is set to `backend`

**"Google Sheets error"**
- Verify `hiresong-key.json` is uploaded
- Check `GOOGLE_SHEET_ID` is correct
- Make sure sheet is shared with service account email

**"ffmpeg not found"**
- This should be handled by `nixpacks.toml`
- Check Railway build logs

### Frontend Issues:

**"Failed to fetch" or CORS error**
- Verify `VITE_API_URL` is set correctly in Vercel
- Make sure it starts with `https://` and has no trailing slash
- Check backend CORS is allowing all origins

**"404 on refresh"**
- `vercel.json` should handle this
- Verify `vercel.json` is in frontend root

---

## Important Notes

1. **API Keys**: Never commit API keys to GitHub
   - They're in `.env` which is gitignored
   - Add them directly in Railway/Vercel dashboards

2. **Google Service Account**: 
   - `hiresong-key.json` is gitignored (`.gitignore` has `*.json`)
   - Upload it separately to Railway
   - Don't commit it to GitHub

3. **Results Folder**:
   - Local `backend/results/` is gitignored
   - On Railway, files are temporary
   - Videos are generated on-demand and returned immediately
   - Image/video URLs from Fal.ai are saved to Google Sheets

4. **Cost**:
   - Railway free tier: $5 credit/month (~25-50 videos)
   - Vercel free tier: Unlimited (for frontend)
   - Main cost: API calls (~$2.60 per video)

---

## Success Checklist

- [ ] Backend deployed to Railway
- [ ] Backend health check works (`/api/health`)
- [ ] Frontend deployed to Vercel
- [ ] Frontend can reach backend (check browser console)
- [ ] Full pipeline works end-to-end
- [ ] Google Sheet logs data correctly
- [ ] Share your awesome project! 🎉

---

## Next Steps

1. **Test thoroughly** - Generate a few videos to make sure everything works
2. **Share your project** - Post to Twitter, LinkedIn, your hackathon
3. **Monitor costs** - Check Railway usage and API spending
4. **Iterate** - Get feedback and improve!

**Good luck! 🚀🎵**

