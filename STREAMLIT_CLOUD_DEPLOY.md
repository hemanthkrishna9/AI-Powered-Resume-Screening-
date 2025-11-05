# Deploy to Streamlit Community Cloud (100% FREE!)

## 🎉 Why Streamlit Cloud?

- ✅ **Completely FREE** - No credit card required
- ✅ **Unlimited public apps** - Deploy as many as you want
- ✅ **Built for Streamlit** - Zero configuration needed
- ✅ **GitHub integration** - Auto-deploy on push
- ✅ **Free SSL** - Automatic HTTPS
- ✅ **Custom domains** - Use your own domain (optional)
- ✅ **Secrets management** - Secure environment variables
- ✅ **Fast deployment** - 2-3 minutes from push to live

---

## 📋 Prerequisites

1. ✅ GitHub account (you already have this!)
2. ✅ Your code is on GitHub (already done!)
3. ⏱️ **5 minutes** to deploy

---

## 🚀 Step-by-Step Deployment Guide

### Step 1: Sign Up for Streamlit Community Cloud

1. Go to: **https://share.streamlit.io/**
2. Click **"Sign up"** or **"Continue with GitHub"**
3. Authorize Streamlit to access your GitHub account
4. That's it! No credit card needed.

---

### Step 2: Deploy Your App

1. After signing in, click **"New app"** button (top right)

2. Fill in the deployment form:

   **Repository:** `hemanthkrishna9/AI-Powered-Resume-Screening-`

   **Branch:** `claude/ai-resume-screening-setup-011CUowYAu6PHatSAwMYjdeF`

   **Main file path:** `frontend/streamlit_app.py`

   **App URL (optional):** Choose a custom name like `itc-ai-resume-screener`

3. Click **"Advanced settings..."** at the bottom

---

### Step 3: Configure Secrets (Azure OpenAI Credentials)

In the **Advanced settings** section:

1. Find the **"Secrets"** text area

2. Copy and paste this EXACTLY:

```toml
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "https://itcmentor.openai.azure.com/"
AZURE_OPENAI_API_KEY = "4FuAkN0MCCjWTv2zGuwvOw622IjmsnwWbh0SCo7U2xuNhP3rY3AoJQQJ99BlACYeBjFXj3w3AAABACOGrcAG"
AZURE_EMBEDDING_DEPLOYMENT = "text-embedding-3-large"
AZURE_GPT_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_EMBEDDING_DIMENSION = "3072"

# App Configuration
AI_PROVIDER = "azure"
AZURE_OPENAI_ENABLED = "True"
USE_SAMPLE_DATA = "True"

# Optional Settings
LOG_LEVEL = "INFO"
```

3. Click **"Save"**

---

### Step 4: Set Python Version

In **Advanced settings**:

1. **Python version:** Select **3.10** (or 3.11)

2. Click **"Deploy!"** button

---

### Step 5: Wait for Deployment

You'll see:
- 📦 **"Installing dependencies..."** (~2 minutes)
- 🔧 **"Starting app..."** (~30 seconds)
- ✅ **"Your app is live!"**

**Total time: 2-3 minutes** ⏱️

---

## 🎯 Your App URL

After deployment, your app will be available at:

```
https://itc-ai-resume-screener.streamlit.app/
```

Or whatever custom name you chose!

---

## 🔧 Managing Your App

### View Logs

1. Go to: https://share.streamlit.io/
2. Click on your app
3. Click **"Manage app"** (bottom right)
4. Click **"Logs"** tab

### Update Secrets

1. Click **"Settings"** tab
2. Scroll to **"Secrets"**
3. Edit and save

### Reboot App

1. Click **"︙"** menu (three dots)
2. Click **"Reboot app"**

### Delete App

1. Click **"︙"** menu
2. Click **"Delete app"**

---

## 🔄 Auto-Deploy on Git Push

Streamlit Cloud automatically redeploys when you push to your branch!

1. Make changes to your code locally or in GitHub
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. Wait 2-3 minutes
4. Refresh your app URL - changes are live!

---

## 📊 App Resources (Free Tier)

Your app gets:
- **CPU:** 1 core
- **RAM:** 1 GB
- **Storage:** Limited (use external storage for large files)
- **Uptime:** Sleeps after 7 days of inactivity
- **Wake time:** ~30 seconds when someone visits

**Note:** The app stays awake as long as people are using it!

---

## 🎨 Custom Domain (Optional)

Want to use your own domain like `resume.itcinfotech.com`?

1. Go to app settings
2. Click **"Custom subdomain"**
3. Follow DNS configuration instructions

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"

**Fix:** Make sure `requirements.txt` is in the root directory

### Error: "Can't find model 'en_core_web_sm'"

**Fix:** Already handled! The app downloads it automatically on first run.

### Error: "File not found: frontend/streamlit_app.py"

**Fix:**
1. Check the **Main file path** setting
2. Should be: `frontend/streamlit_app.py`
3. Not: `streamlit_app.py` or `/frontend/streamlit_app.py`

### App is slow to load

**Cause:** First visitor after sleep period (7 days inactivity)

**Fix:** App will stay awake as long as people use it regularly

### Azure OpenAI errors

**Fix:**
1. Go to app settings → Secrets
2. Verify all Azure credentials are correct
3. Check API key has no extra spaces
4. Reboot app

---

## 🔒 Security Best Practices

### ✅ What We Did:
- Secrets stored in Streamlit Cloud (encrypted)
- API keys not in code or Git
- HTTPS by default

### ⚠️ Important:
- Never commit `.env` file to Git
- Never share your secrets configuration
- Rotate API keys periodically

---

## 📈 Monitoring & Analytics

### View App Stats:

1. Go to https://share.streamlit.io/
2. Click on your app
3. See:
   - Number of viewers
   - App status (running/sleeping)
   - Last deployment time
   - Resource usage

### Wake Up Sleeping App:

If app hasn't been used in 7 days:
1. Just visit the URL
2. Wait ~30 seconds for wake-up
3. App is live again!

---

## 🎯 Complete Deployment Checklist

Before you deploy, make sure:

- [ ] GitHub repository is public (or Streamlit has access)
- [ ] `requirements.txt` is in root directory
- [ ] `frontend/streamlit_app.py` exists
- [ ] You have Azure OpenAI credentials ready
- [ ] Python version is 3.10 or 3.11

---

## 🚀 Alternative Free Options

If you need more resources, consider:

### 1. **Render.com** (Free Tier)
- 512 MB RAM (vs 1 GB on Streamlit)
- More control over environment
- Requires Dockerfile

### 2. **Railway.app**
- $5 free credit/month
- 8 GB RAM, 8 vCPU
- Requires credit card

### 3. **Google Cloud Run**
- Pay-as-you-go
- 2 million requests/month free
- Requires credit card

### 4. **Replit**
- Free hosting
- Built-in IDE
- Limited resources

**Recommendation:** Start with **Streamlit Cloud** - it's the easiest and truly free!

---

## 🎉 After Deployment

### Share Your App:

```
🎯 AI-Powered Resume Screening System
🔗 https://itc-ai-resume-screener.streamlit.app/

✨ Features:
- AI-powered candidate matching
- Resume parsing (PDF, DOCX)
- Semantic search with Azure OpenAI
- Beautiful modern UI
- Real-time matching scores

Built for ITC Infotech by AI
```

### Test Your App:

1. ✅ Upload a sample resume from `data/sample_resumes/`
2. ✅ Paste a JD from `data/sample_jds/`
3. ✅ Click "Start AI Matching"
4. ✅ See beautiful match results with scores!

---

## 💡 Pro Tips

1. **Bookmark your app:** https://share.streamlit.io/
2. **Check logs regularly:** Catch errors early
3. **Monitor usage:** See when app is most active
4. **Update regularly:** Push improvements via Git
5. **Share the URL:** Show off your work!

---

## 🆘 Need Help?

### Streamlit Resources:
- **Docs:** https://docs.streamlit.io/
- **Forum:** https://discuss.streamlit.io/
- **Community:** Very active and helpful!

### Azure OpenAI Issues:
- Check Azure portal for API status
- Verify endpoint and key are correct
- Check API quota limits

---

## 🎊 Success!

Once deployed, you'll have:
- ✅ **Live URL** accessible from anywhere
- ✅ **Beautiful UI** with modern design
- ✅ **AI-powered matching** with Azure OpenAI
- ✅ **Auto-deploy** on every Git push
- ✅ **Free hosting** forever!

**Total cost: $0.00** 💰

---

**Ready to deploy? Go to https://share.streamlit.io/ and follow the steps above!** 🚀
