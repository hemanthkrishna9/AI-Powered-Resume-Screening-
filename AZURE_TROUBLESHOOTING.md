# Azure Deployment Troubleshooting Guide

## 🚨 Application Error - Quick Fix Steps

If you see "Application Error" when accessing your Azure app, follow these steps:

---

## Step 1: Check Deployment Logs

### Via Azure Portal:
1. Go to **Azure Portal** → Your App Service
2. Click **Deployment Center** (left menu)
3. Click on the **Logs** tab
4. Look for errors in the deployment process
5. Check if the build completed successfully

### Common Issues:
- ❌ **Build timeout**: Dependencies taking too long to install
- ❌ **Missing files**: GitHub branch or files not found
- ❌ **Python version mismatch**: Wrong Python version selected

---

## Step 2: Check Application Logs

### Via Azure Portal:
1. Go to **Azure Portal** → Your App Service
2. Click **Log stream** (left menu under Monitoring)
3. Wait 10-20 seconds for logs to appear
4. Look for startup errors

### Via SSH Console:
1. Go to **Azure Portal** → Your App Service
2. Click **SSH** (left menu under Development Tools)
3. Click **Go** to open SSH console
4. Run these commands:

```bash
# Check if startup script exists and is executable
ls -la startup.sh

# Check if dependencies are installed
pip list | grep -E "streamlit|openai|spacy"

# Check if spaCy model is downloaded
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✅ spaCy model OK')"

# Check environment variables
env | grep AZURE

# Check logs
cat /home/LogFiles/*.log
```

---

## Step 3: Verify Configuration Settings

### Required App Settings (Environment Variables):

Go to **Configuration** → **Application settings** and verify these exist:

| Setting Name | Value | Required |
|-------------|--------|----------|
| `AZURE_OPENAI_ENDPOINT` | `https://itcmentor.openai.azure.com/` | ✅ Yes |
| `AZURE_OPENAI_API_KEY` | Your API key | ✅ Yes |
| `AZURE_EMBEDDING_DEPLOYMENT` | `text-embedding-3-large` | ✅ Yes |
| `AZURE_GPT_DEPLOYMENT` | `gpt-4o-mini` | ✅ Yes |
| `AI_PROVIDER` | `azure` | ✅ Yes |
| `AZURE_OPENAI_ENABLED` | `True` | ✅ Yes |
| `USE_SAMPLE_DATA` | `True` | ⚠️ Recommended |

### Required General Settings:

Go to **Configuration** → **General settings** and verify:

| Setting | Value |
|---------|-------|
| **Stack** | Python |
| **Python version** | 3.10 or 3.11 |
| **Startup Command** | `bash startup.sh` |

---

## Step 4: Common Fixes

### Fix 1: Redeploy with Correct Branch

If deployment used wrong branch:

1. **Deployment Center** → **Settings**
2. Verify **Branch**: `claude/ai-resume-screening-setup-011CUowYAu6PHatSAwMYjdeF`
3. Click **Save**
4. Click **Sync** to trigger redeployment

### Fix 2: Restart the App

Sometimes a simple restart helps:

1. Go to **Overview**
2. Click **Restart** button at top
3. Click **Yes** to confirm
4. Wait 2-3 minutes
5. Try accessing your app URL again

### Fix 3: Clear Deployment Cache

If old files are cached:

1. Go to **Deployment Center** → **Settings**
2. Click **Disconnect** (removes GitHub connection temporarily)
3. Click **Save**
4. Wait 30 seconds
5. Click **Settings** again and reconnect to GitHub
6. Select your repository and branch
7. Click **Save** to redeploy fresh

### Fix 4: Check Startup Command

Ensure the startup command is correct:

1. Go to **Configuration** → **General settings**
2. **Startup Command** should be: `bash startup.sh`
3. Click **Save**
4. Restart the app

### Fix 5: Enable Diagnostic Logging

Get more detailed error information:

1. Go to **App Service logs** (left menu)
2. Enable these settings:
   - **Application Logging (Filesystem)**: On → Level: Verbose
   - **Detailed Error Messages**: On
   - **Failed Request Tracing**: On
3. Click **Save**
4. Restart app
5. Check **Log stream** again for detailed errors

---

## Step 5: Test Locally (Optional)

To verify code works before deploying:

### Using Docker:

```bash
# Build Docker image
docker build -t ai-resume-screener .

# Run container
docker run -p 8000:8000 \
  -e AZURE_OPENAI_ENDPOINT="https://itcmentor.openai.azure.com/" \
  -e AZURE_OPENAI_API_KEY="your_key_here" \
  -e AZURE_EMBEDDING_DEPLOYMENT="text-embedding-3-large" \
  -e AZURE_GPT_DEPLOYMENT="gpt-4o-mini" \
  ai-resume-screener

# Open browser to: http://localhost:8000
```

### Without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file with credentials
cat > .env <<EOF
AZURE_OPENAI_ENDPOINT=https://itcmentor.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key_here
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_GPT_DEPLOYMENT=gpt-4o-mini
USE_SAMPLE_DATA=True
EOF

# Run Streamlit
streamlit run frontend/streamlit_app.py
```

---

## Step 6: Specific Error Solutions

### Error: "ModuleNotFoundError"

**Cause**: Missing Python package

**Fix**:
1. Check if `requirements.txt` is in root directory
2. Verify deployment logs show: "Installing dependencies..."
3. If not, trigger redeployment

### Error: "Can't find model 'en_core_web_sm'"

**Cause**: spaCy model not downloaded

**Fix**:
1. Check `startup.sh` contains: `python -m spacy download en_core_web_sm`
2. SSH into app and manually run: `python -m spacy download en_core_web_sm`
3. Restart app

### Error: "Port 8000 already in use" or "Connection refused"

**Cause**: App not using Azure's PORT environment variable

**Fix**:
1. Ensure latest `startup.sh` uses: `PORT="${PORT:-8000}"`
2. Redeploy latest code from GitHub
3. Restart app

### Error: "Azure OpenAI API error" or "Invalid API key"

**Cause**: Missing or incorrect Azure OpenAI credentials

**Fix**:
1. Verify all 12 environment variables in **Configuration** → **Application settings**
2. Check API key has no extra spaces or quotes
3. Test API key using SSH console:

```bash
python -c "from openai import AzureOpenAI; client = AzureOpenAI(api_key='YOUR_KEY', azure_endpoint='https://itcmentor.openai.azure.com/', api_version='2024-02-15-preview'); print('✅ API key works')"
```

### Error: "Application Timeout"

**Cause**: App takes too long to start (spaCy model download)

**Fix**:
1. Increase timeout in **Configuration** → **General settings**
2. Set **Startup time** to 300 seconds (5 minutes)
3. Or use Docker deployment (model pre-downloaded in image)

---

## Step 7: Resource Verification

Check if your App Service has enough resources:

### Minimum Requirements:
- **Tier**: Basic B1 or higher
- **CPU**: 1 core
- **Memory**: 1.75 GB RAM
- **Storage**: 10 GB

### Check Current Resources:
1. Go to **Overview**
2. See **App Service plan** section
3. If on Free (F1) tier → Upgrade to Basic B1

### Upgrade if needed:
1. Click on your **App Service plan** name
2. Click **Scale up (App Service plan)**
3. Select **Production** → **B1** (or higher)
4. Click **Apply**

---

## Step 8: Manual Deployment (Alternative)

If GitHub deployment keeps failing, try manual ZIP deployment:

### Via Azure CLI (in local terminal):

```bash
# Login to Azure
az login

# Package code
zip -r app.zip . -x "*.git*" "venv/*" "__pycache__/*" "*.pyc"

# Deploy
az webapp deployment source config-zip \
  --resource-group your-resource-group \
  --name your-app-name \
  --src app.zip
```

### Via Portal:
1. Download your repository as ZIP from GitHub
2. Go to **Deployment Center** → **FTPS credentials**
3. Note username and password
4. Use FTP client (FileZilla) to upload files

---

## Still Having Issues?

### Check these resources:

1. **Azure Status Page**: https://status.azure.com
   - Check if Azure services are down in your region

2. **GitHub Actions**:
   - Check `.github/workflows/azure-deploy.yml` for CI/CD errors

3. **Sample Data**:
   - Ensure `data/sample_resumes/` and `data/sample_jds/` exist
   - Copy from: https://github.com/[your-repo]/tree/main/data

4. **Support Channels**:
   - Azure Portal → **Support + troubleshooting** → **New support request**
   - Check Azure documentation: https://docs.microsoft.com/azure/app-service/

---

## Success Indicators ✅

Your app is working correctly when you see:

1. **In Azure Portal** → **Log stream**:
   ```
   Starting AI Resume Screening Application...
   Using port: 8080
   Checking spaCy model...
   ✅ spaCy model already installed
   Starting Streamlit server on port 8080...
   You can now view your Streamlit app in your browser.
   ```

2. **In browser** at `https://your-app-name.azurewebsites.net`:
   - Purple gradient header
   - "🎯 AI-Powered Resume Screening" title
   - Sidebar with navigation menu
   - Dashboard with metrics (all showing 0 initially)

3. **Sample data test**:
   - Upload a resume from `data/sample_resumes/`
   - Enter a JD from `data/sample_jds/`
   - Click "Start Matching"
   - See match results with scores

---

## Quick Reference Commands

### Check App Status:
```bash
curl -I https://your-app-name.azurewebsites.net
```

### Check Health Endpoint:
```bash
curl https://your-app-name.azurewebsites.net/_stcore/health
```

### Restart App via CLI:
```bash
az webapp restart --name your-app-name --resource-group your-resource-group
```

### View Recent Logs via CLI:
```bash
az webapp log tail --name your-app-name --resource-group your-resource-group
```

---

**Need more help?** Contact your Azure administrator or check the main deployment guide: `GITHUB_TO_AZURE.md`
