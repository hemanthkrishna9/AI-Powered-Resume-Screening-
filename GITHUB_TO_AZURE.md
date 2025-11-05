# 🚀 Deploy from GitHub to Azure Portal (No Local Setup!)

**Deploy directly from your GitHub repository to Azure - 100% cloud-based!**

---

## ✨ **Benefits of This Approach:**

- ✅ No local machine setup needed
- ✅ Auto-deploy on every git push
- ✅ Everything in the cloud
- ✅ Easiest method possible
- ✅ Built-in CI/CD

---

## 📋 **Step-by-Step Guide**

### **Step 1: Go to Azure Portal**

1. Open browser and go to: **https://portal.azure.com**
2. Login with your Azure account

---

### **Step 2: Create Web App**

1. Click **"Create a resource"** (big + button)
2. Search for **"Web App"**
3. Click **"Create"**

---

### **Step 3: Configure Basic Settings**

Fill in the form:

**Project Details:**
- **Subscription**: Select your subscription
- **Resource Group**: Click "Create new" → Enter `rg-resume-screener`

**Instance Details:**
- **Name**: `ai-resume-screener` (or any unique name)
- **Publish**: Select **Code**
- **Runtime stack**: Select **Python 3.10**
- **Operating System**: Select **Linux**
- **Region**: Select **East US** (or nearest to you)

**Pricing:**
- **App Service Plan**: Click "Create new"
  - Name: `plan-resume-screener`
  - **Sku**: Select **B1** (Basic - $13/month)
  - Click **OK**

Click **"Next: Deployment >"**

---

### **Step 4: Configure GitHub Deployment**

**Continuous Deployment:**
- Enable: **Yes** ✅

**GitHub Settings:**
- Click **"Authorize"** (login to GitHub if prompted)
- **Organization**: Select your GitHub username
- **Repository**: Select `AI-Powered-Resume-Screening-`
- **Branch**: Select `claude/ai-resume-screening-setup-011CUowYAu6PHatSAwMYjdeF`

Click **"Next: Networking >"**

---

### **Step 5: Skip Optional Settings**

- **Networking**: Keep defaults, click **"Next: Monitoring >"**
- **Monitoring**:
  - Enable Application Insights: **Yes** (optional but recommended)
  - Click **"Next: Tags >"**
- **Tags**: Skip, click **"Next: Review + create >"**

---

### **Step 6: Review and Create**

1. Review all settings
2. Click **"Create"**
3. Wait 2-3 minutes for deployment

You'll see: **"Deployment is in progress..."**

---

### **Step 7: Configure Environment Variables**

After deployment completes:

1. Click **"Go to resource"**
2. In left menu, find **"Configuration"** (under Settings)
3. Click **"Application settings"** tab
4. Click **"+ New application setting"**

Add these settings one by one:

| Name | Value |
|------|-------|
| `AZURE_OPENAI_ENDPOINT` | `https://itcmentor.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | `4FuAkN0MCCjWTv2zGuwvOw622IjmsnwWbh0SCo7U2xuNhP3rY3AoJQQJ99BlACYeBjFXj3w3AAABACOGrcAG` |
| `AZURE_OPENAI_API_VERSION` | `2024-02-01` |
| `AZURE_EMBEDDING_DEPLOYMENT` | `text-embedding-3-large` |
| `AZURE_EMBEDDING_MODEL` | `text-embedding-3-large` |
| `AZURE_GPT_DEPLOYMENT` | `gpt-4o-mini` |
| `AZURE_GPT_MODEL` | `gpt-4o-mini` |
| `AZURE_GPT_API_VERSION` | `2024-12-01-preview` |
| `AI_PROVIDER` | `azure` |
| `USE_SAMPLE_DATA` | `True` |
| `DEBUG` | `False` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |

5. Click **"Save"** at the top
6. Click **"Continue"** when prompted

---

### **Step 8: Configure Startup Command**

Still in Configuration page:

1. Click **"General settings"** tab
2. Find **"Startup Command"** field
3. Enter: `bash startup.sh`
4. Click **"Save"** at the top

---

### **Step 9: Enable HTTPS**

1. In left menu, find **"TLS/SSL settings"**
2. Under **"HTTPS Only"**, toggle to **On**
3. Click **"Save"**

---

### **Step 10: Get Your App URL**

1. Go back to **"Overview"** (in left menu)
2. Find **"URL"** - it will be something like:
   ```
   https://ai-resume-screener.azurewebsites.net
   ```
3. **Copy this URL** - this is your app!

---

### **Step 11: Monitor Deployment**

1. In left menu, find **"Deployment Center"**
2. You'll see GitHub connected
3. Watch the deployment status (should show "Success")

OR

1. In left menu, find **"Log stream"** (under Monitoring)
2. Watch real-time logs
3. Wait for: `"Starting Streamlit server..."`

---

### **Step 12: Access Your App!**

1. Wait **3-5 minutes** for first startup (installing packages, downloading spaCy model)
2. Open your app URL in a new tab:
   ```
   https://ai-resume-screener.azurewebsites.net
   ```
3. You should see your beautiful purple gradient UI! 🎉

---

## 🎊 **Success! What You Should See:**

✅ **Beautiful gradient background** (purple/blue)
✅ **"AI-Powered Resume Screening"** header
✅ **Dashboard with 4 metric cards**
✅ **Sidebar navigation**
✅ **Upload Resumes, Match Candidates, Top Candidates** pages

---

## 🧪 **Test Your Deployed App:**

### Test 1: Upload Resume

1. Go to **"Upload Resumes"** page
2. Create a text file on your desktop with this content (copy from GitHub):
   - https://github.com/YOUR_REPO/blob/YOUR_BRANCH/data/sample_resumes/rajesh_kumar_python.txt
3. Upload the file
4. Click **"Parse Resumes"**
5. Should show: "✅ Successfully parsed 1 resume(s)!"

### Test 2: Match Candidates

1. Go to **"Match Candidates"** page
2. Copy this job description (from GitHub):
   - https://github.com/YOUR_REPO/blob/YOUR_BRANCH/data/sample_jds/senior_python_developer.txt
3. Paste into the text area
4. Add required skills: `Python, FastAPI, Docker, AWS`
5. Click **"Start Matching"**
6. Wait for AI analysis (~30 seconds)

### Test 3: View Results

1. Go to **"Top Candidates"** page
2. Should see Rajesh Kumar with **85-95% match**
3. AI explanation showing why he's a great match
4. Matching skills highlighted in purple tags

---

## 🔄 **Auto-Deploy on Git Push**

Now, every time you push to your GitHub branch:

1. GitHub triggers Azure deployment
2. Azure pulls latest code
3. Rebuilds the app
4. Auto-deploys in 2-3 minutes

**No manual deployment needed ever again!**

---

## 📊 **Monitor Your App (Azure Portal)**

### View Logs:
1. Go to your Web App in Azure Portal
2. **"Log stream"** (left menu) → Real-time logs
3. **"Monitoring" → "Metrics"** → CPU, Memory, Requests

### Application Insights:
1. Go to **"Application Insights"** (left menu)
2. View performance, errors, usage
3. Set up alerts

### Restart App:
1. Go to **"Overview"**
2. Click **"Restart"** button at top

---

## 💰 **Cost**

**Basic B1 Tier:**
- **~$13/month** (₹1,080/month)
- 1.75 GB RAM
- 1 vCPU
- Perfect for testing and demos

**To upgrade later:**
1. Go to **"Scale up (App Service plan)"**
2. Select higher tier (S1, P1V2)
3. Click **"Apply"**

---

## 🔧 **Troubleshooting**

### Issue: "Application Error"

**Solution:**
1. Wait 3-5 minutes for first startup
2. Check **"Log stream"** for errors
3. Restart the app

### Issue: Slow loading

**Solution:**
- First load is always slower (cold start)
- Subsequent loads faster
- Upgrade to S1 tier for better performance

### Issue: 500 Error

**Solution:**
1. Check **"Log stream"**
2. Verify all environment variables are set
3. Check API key is correct
4. Restart app

### Issue: Can't see logs

**Solution:**
1. Go to **"App Service logs"** (left menu)
2. Enable **"Application Logging (Filesystem)"** → On
3. Click **"Save"**
4. Go back to **"Log stream"**

---

## 🎯 **Quick Links (Azure Portal)**

After deployment, bookmark these:

- **Your App URL**: `https://YOUR_APP_NAME.azurewebsites.net`
- **Azure Portal**: https://portal.azure.com
- **Your Resource Group**: Portal → Resource Groups → rg-resume-screener
- **Your Web App**: Portal → App Services → ai-resume-screener

---

## 📱 **Share With Your Team**

Once deployed, share:
1. **App URL** - anyone can access and test
2. **Demo credentials** (if you add authentication later)
3. **Sample data** - from GitHub repository

---

## ✅ **Deployment Checklist**

- [ ] Created Web App in Azure Portal
- [ ] Connected to GitHub repository
- [ ] Added all environment variables (12 settings)
- [ ] Set startup command: `bash startup.sh`
- [ ] Enabled HTTPS Only
- [ ] Waited 3-5 minutes for startup
- [ ] Opened app URL in browser
- [ ] Saw beautiful purple UI
- [ ] Tested resume upload
- [ ] Tested candidate matching
- [ ] Got AI-powered results

---

## 🎉 **You're Done!**

Your app is now:
- ✅ **Live on Azure**
- ✅ **Auto-deploying from GitHub**
- ✅ **Using your Azure OpenAI**
- ✅ **Ready for testing**
- ✅ **Ready to demo**

**App URL**: `https://ai-resume-screener.azurewebsites.net`

---

## 🚀 **Next Steps**

1. **Test thoroughly** with sample data
2. **Share URL** with your team lead
3. **Demo features** to stakeholders
4. **Monitor usage** in Application Insights
5. **Scale up** if needed for production

---

**Need help? Any errors? Let me know and I'll help fix them!**

©2025 ITC Infotech | Deployed on Azure
