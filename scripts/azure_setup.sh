#!/bin/bash

# Azure Setup Script for AI Resume Screener
# This script automates the Azure deployment setup

set -e  # Exit on error

# Colors for output
RED='\033[0:31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  AI Resume Screener - Azure Setup${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Configuration
RESOURCE_GROUP="rg-resume-screener"
LOCATION="eastus"
APP_SERVICE_PLAN="plan-resume-screener"
WEB_APP_NAME="ai-resume-screener-$(date +%s)"  # Unique name
SKU="B1"  # Basic tier (change to P1V2 for production)

# Prompt for Azure OpenAI credentials
echo -e "${YELLOW}Enter your Azure OpenAI details:${NC}"
read -p "Azure OpenAI Endpoint: " AZURE_ENDPOINT
read -sp "Azure OpenAI API Key: " AZURE_API_KEY
echo ""

# Step 1: Login to Azure
echo -e "\n${GREEN}Step 1: Logging in to Azure...${NC}"
az login

# Step 2: Create Resource Group
echo -e "\n${GREEN}Step 2: Creating Resource Group...${NC}"
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION \
  --output table

# Step 3: Create App Service Plan
echo -e "\n${GREEN}Step 3: Creating App Service Plan (SKU: $SKU)...${NC}"
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku $SKU \
  --output table

# Step 4: Create Web App
echo -e "\n${GREEN}Step 4: Creating Web App...${NC}"
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEB_APP_NAME \
  --runtime "PYTHON:3.10" \
  --output table

# Step 5: Configure App Settings
echo -e "\n${GREEN}Step 5: Configuring Environment Variables...${NC}"
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings \
    AZURE_OPENAI_ENDPOINT="$AZURE_ENDPOINT" \
    AZURE_OPENAI_API_KEY="$AZURE_API_KEY" \
    AZURE_OPENAI_API_VERSION="2024-02-01" \
    AZURE_EMBEDDING_DEPLOYMENT="text-embedding-3-large" \
    AZURE_EMBEDDING_MODEL="text-embedding-3-large" \
    AZURE_GPT_DEPLOYMENT="gpt-4o-mini" \
    AZURE_GPT_MODEL="gpt-4o-mini" \
    AZURE_GPT_API_VERSION="2024-12-01-preview" \
    AI_PROVIDER="azure" \
    USE_SAMPLE_DATA="True" \
    DEBUG="False" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    PYTHON_VERSION="3.10" \
  --output table

# Step 6: Configure Startup Command
echo -e "\n${GREEN}Step 6: Setting Startup Command...${NC}"
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --startup-file "bash startup.sh" \
  --output table

# Step 7: Enable HTTPS Only
echo -e "\n${GREEN}Step 7: Enabling HTTPS Only...${NC}"
az webapp update \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --https-only true \
  --output table

# Step 8: Get deployment URL
echo -e "\n${GREEN}Step 8: Getting Web App URL...${NC}"
APP_URL=$(az webapp show \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query defaultHostName \
  --output tsv)

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Resource Group: ${YELLOW}$RESOURCE_GROUP${NC}"
echo -e "App Service Plan: ${YELLOW}$APP_SERVICE_PLAN${NC}"
echo -e "Web App Name: ${YELLOW}$WEB_APP_NAME${NC}"
echo -e "App URL: ${GREEN}https://$APP_URL${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Deploy your code using GitHub Actions or Azure CLI"
echo "2. Monitor deployment: az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
echo "3. Access your app: https://$APP_URL"
echo ""
echo -e "${GREEN}To deploy code manually:${NC}"
echo "  cd /path/to/AI-Powered-Resume-Screening-"
echo "  zip -r deploy.zip . -x '*.git*' 'venv/*'"
echo "  az webapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --src deploy.zip"
echo ""
echo -e "${GREEN}To view logs:${NC}"
echo "  az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
