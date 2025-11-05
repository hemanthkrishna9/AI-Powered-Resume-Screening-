# 🚀 Azure Deployment Guide

Complete guide to deploy the AI Resume Screening application to Azure App Service.

---

## 📋 Prerequisites

- Azure Account with active subscription
- Azure CLI installed ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- Git and GitHub account
- Docker installed (optional, for local testing)

---

## 🎯 Deployment Options

### **Option A: Azure App Service with Docker** (Recommended)
- Best for production
- Containerized deployment
- Easy scaling
- Automatic updates

### **Option B: Azure App Service (Direct Deploy)**
- Simpler setup
- Good for quick testing
- Direct from GitHub

---

## 🚀 Option A: Deploy with Docker Container

### Step 1: Login to Azure

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "Your-Subscription-Name"
```

### Step 2: Create Resource Group

```bash
# Create resource group
az group create \
  --name rg-resume-screener \
  --location eastus

# Verify creation
az group show --name rg-resume-screener
```

### Step 3: Create Container Registry (Optional but recommended)

```bash
# Create Azure Container Registry
az acr create \
  --resource-group rg-resume-screener \
  --name resumescreeneracr \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials
az acr credential show --name resumescreeneracr
```

### Step 4: Build and Push Docker Image

```bash
# Login to ACR
az acr login --name resumescreeneracr

# Build Docker image
docker build -t ai-resume-screener:latest .

# Tag image
docker tag ai-resume-screener:latest resumescreeneracr.azurecr.io/ai-resume-screener:latest

# Push to ACR
docker push resumescreeneracr.azurecr.io/ai-resume-screener:latest
```

### Step 5: Create App Service Plan

```bash
# Create App Service Plan (Linux, B1 tier)
az appservice plan create \
  --name plan-resume-screener \
  --resource-group rg-resume-screener \
  --is-linux \
  --sku B1

# For production, use higher tier:
# --sku P1V2  (Premium)
# --sku S1    (Standard)
```

### Step 6: Create Web App

```bash
# Create Web App with container
az webapp create \
  --resource-group rg-resume-screener \
  --plan plan-resume-screener \
  --name ai-resume-screener \
  --deployment-container-image-name resumescreeneracr.azurecr.io/ai-resume-screener:latest

# Enable ACR authentication
az webapp config container set \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --docker-custom-image-name resumescreeneracr.azurecr.io/ai-resume-screener:latest \
  --docker-registry-server-url https://resumescreeneracr.azurecr.io \
  --docker-registry-server-user resumescreeneracr \
  --docker-registry-server-password $(az acr credential show --name resumescreeneracr --query "passwords[0].value" -o tsv)
```

### Step 7: Configure Environment Variables

```bash
# Set Azure OpenAI credentials
az webapp config appsettings set \
  --resource-group rg-resume-screener \
  --name ai-resume-screener \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://itcmentor.openai.azure.com/" \
    AZURE_OPENAI_API_KEY="YOUR_API_KEY_HERE" \
    AZURE_OPENAI_API_VERSION="2024-02-01" \
    AZURE_EMBEDDING_DEPLOYMENT="text-embedding-3-large" \
    AZURE_GPT_DEPLOYMENT="gpt-4o-mini" \
    USE_SAMPLE_DATA="True" \
    DEBUG="False"
```

### Step 8: Enable Continuous Deployment (Optional)

```bash
# Enable CI/CD from ACR
az webapp deployment container config \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --enable-cd true
```

### Step 9: Access Your App

```bash
# Get app URL
az webapp show \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --query defaultHostName \
  --output tsv

# Open in browser
# https://ai-resume-screener.azurewebsites.net
```

---

## 🔧 Option B: Direct Deploy from GitHub

### Step 1: Create App Service

```bash
# Create resource group
az group create --name rg-resume-screener --location eastus

# Create App Service Plan
az appservice plan create \
  --name plan-resume-screener \
  --resource-group rg-resume-screener \
  --is-linux \
  --sku B1

# Create Web App (Python runtime)
az webapp create \
  --resource-group rg-resume-screener \
  --plan plan-resume-screener \
  --name ai-resume-screener \
  --runtime "PYTHON:3.10"
```

### Step 2: Configure GitHub Deployment

```bash
# Get publish profile
az webapp deployment list-publishing-profiles \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --xml

# Copy the output and add as GitHub Secret: AZURE_WEBAPP_PUBLISH_PROFILE
```

### Step 3: Setup GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add new secret:
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: Paste the publish profile XML from previous step

4. Add Azure OpenAI credentials:
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`

### Step 4: Configure App Settings

```bash
az webapp config appsettings set \
  --resource-group rg-resume-screener \
  --name ai-resume-screener \
  --settings \
    AZURE_OPENAI_ENDPOINT="https://itcmentor.openai.azure.com/" \
    AZURE_OPENAI_API_KEY="YOUR_API_KEY" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    PYTHON_VERSION="3.10"
```

### Step 5: Configure Startup Command

```bash
az webapp config set \
  --resource-group rg-resume-screener \
  --name ai-resume-screener \
  --startup-file "bash startup.sh"
```

### Step 6: Deploy

Push to main branch - GitHub Actions will automatically deploy!

```bash
git add .
git commit -m "Deploy to Azure"
git push origin main
```

---

## 🔍 Monitoring & Logs

### View Application Logs

```bash
# Stream logs in real-time
az webapp log tail \
  --name ai-resume-screener \
  --resource-group rg-resume-screener

# Download logs
az webapp log download \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --log-file logs.zip
```

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app ai-resume-screener-insights \
  --location eastus \
  --resource-group rg-resume-screener \
  --application-type web

# Get instrumentation key
az monitor app-insights component show \
  --app ai-resume-screener-insights \
  --resource-group rg-resume-screener \
  --query instrumentationKey

# Configure Web App
az webapp config appsettings set \
  --resource-group rg-resume-screener \
  --name ai-resume-screener \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="YOUR_KEY_HERE"
```

---

## 📊 Scaling

### Manual Scaling

```bash
# Scale up (increase resources)
az appservice plan update \
  --name plan-resume-screener \
  --resource-group rg-resume-screener \
  --sku P1V2

# Scale out (increase instances)
az appservice plan update \
  --name plan-resume-screener \
  --resource-group rg-resume-screener \
  --number-of-workers 3
```

### Auto-Scaling

```bash
# Enable autoscale
az monitor autoscale create \
  --resource-group rg-resume-screener \
  --resource ai-resume-screener \
  --resource-type Microsoft.Web/sites \
  --name autoscale-resume-screener \
  --min-count 1 \
  --max-count 5 \
  --count 1

# Add CPU-based rule
az monitor autoscale rule create \
  --resource-group rg-resume-screener \
  --autoscale-name autoscale-resume-screener \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

---

## 🔒 Security Best Practices

### 1. Use Managed Identity

```bash
# Enable system-assigned managed identity
az webapp identity assign \
  --name ai-resume-screener \
  --resource-group rg-resume-screener
```

### 2. Store Secrets in Key Vault

```bash
# Create Key Vault
az keyvault create \
  --name kv-resume-screener \
  --resource-group rg-resume-screener \
  --location eastus

# Add secrets
az keyvault secret set \
  --vault-name kv-resume-screener \
  --name "AzureOpenAIKey" \
  --value "YOUR_API_KEY"

# Grant access to Web App
az keyvault set-policy \
  --name kv-resume-screener \
  --object-id $(az webapp identity show --name ai-resume-screener --resource-group rg-resume-screener --query principalId -o tsv) \
  --secret-permissions get list
```

### 3. Enable HTTPS Only

```bash
az webapp update \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --https-only true
```

---

## 🧪 Testing Deployment

### 1. Health Check

```bash
curl https://ai-resume-screener.azurewebsites.net/_stcore/health
```

### 2. Access Application

Open in browser:
```
https://ai-resume-screener.azurewebsites.net
```

### 3. Test Features

1. Upload sample resume
2. Enter job description
3. Run matching
4. Verify AI responses

---

## 🐛 Troubleshooting

### Issue: App not starting

**Check logs:**
```bash
az webapp log tail --name ai-resume-screener --resource-group rg-resume-screener
```

**Common fixes:**
- Verify Python version in App Settings
- Check startup script is executable
- Verify all dependencies in requirements.txt

### Issue: Slow performance

**Solutions:**
- Upgrade App Service Plan to higher tier
- Enable Application Insights to identify bottlenecks
- Consider Redis cache for embeddings

### Issue: Out of memory

**Solutions:**
- Upgrade to plan with more memory (P1V2 or higher)
- Optimize batch sizes in code
- Add memory limits in Dockerfile

### Issue: Azure OpenAI errors

**Check:**
- API key is correct in App Settings
- Endpoint URL is correct
- Network connectivity to Azure OpenAI
- Check quota limits

---

## 💰 Cost Estimation

### Basic Tier (B1)
- **Cost**: ~$13/month
- **RAM**: 1.75 GB
- **vCPU**: 1
- **Good for**: Testing, demos

### Standard Tier (S1)
- **Cost**: ~$70/month
- **RAM**: 1.75 GB
- **vCPU**: 1
- **Good for**: Small production

### Premium Tier (P1V2)
- **Cost**: ~$80/month
- **RAM**: 3.5 GB
- **vCPU**: 1
- **Good for**: Production with better performance

**Additional costs:**
- Azure Container Registry: ~$5/month (Basic)
- Application Insights: Pay-per-use (~$2-10/month)
- Azure OpenAI: Pay-per-token

---

## 🔄 CI/CD Pipeline

GitHub Actions workflow is already configured in `.github/workflows/azure-deploy.yml`

**Automatic deployment triggers:**
- Push to `main` branch
- Manual workflow dispatch

**Pipeline steps:**
1. Checkout code
2. Setup Python environment
3. Install dependencies
4. Download spaCy model
5. Create deployment package
6. Deploy to Azure
7. Configure app settings

---

## 📝 Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Build new Docker image
docker build -t ai-resume-screener:v2 .

# Push to ACR
docker tag ai-resume-screener:v2 resumescreeneracr.azurecr.io/ai-resume-screener:v2
docker push resumescreeneracr.azurecr.io/ai-resume-screener:v2

# Update Web App
az webapp config container set \
  --name ai-resume-screener \
  --resource-group rg-resume-screener \
  --docker-custom-image-name resumescreeneracr.azurecr.io/ai-resume-screener:v2
```

### Backup

```bash
# Create backup
az webapp config backup create \
  --resource-group rg-resume-screener \
  --webapp-name ai-resume-screener \
  --backup-name backup-$(date +%Y%m%d) \
  --container-url "<storage_account_sas_url>"
```

---

## 🎉 Success!

Your AI Resume Screening application is now deployed on Azure!

**Access URL:** `https://ai-resume-screener.azurewebsites.net`

### Next Steps:
1. Test all features
2. Set up custom domain (optional)
3. Enable autoscaling for production
4. Set up monitoring alerts
5. Configure backup strategy

---

For support or questions, refer to the main [README.md](README.md)

©2025 ITC Infotech | Powered by Azure OpenAI
