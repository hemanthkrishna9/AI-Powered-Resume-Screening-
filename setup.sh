#!/bin/bash

# Quick Setup Script for Local Testing
# Run this once to set up everything

echo "🚀 Setting up AI Resume Screener for local testing..."
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if (( $(echo "$python_version >= 3.8" | bc -l) )); then
    echo "  ✅ Python $python_version detected"
else
    echo "  ❌ Python 3.8+ required. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
python3 -m venv venv
echo "  ✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  ✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "✓ Upgrading pip..."
pip install --upgrade pip --quiet
echo "  ✅ Pip upgraded"

# Install dependencies
echo ""
echo "✓ Installing dependencies (this may take 2-3 minutes)..."
pip install -r requirements.txt --quiet
echo "  ✅ Dependencies installed"

# Download spaCy model
echo ""
echo "✓ Downloading spaCy language model..."
python -m spacy download en_core_web_sm --quiet
echo "  ✅ spaCy model downloaded"

# Create necessary directories
echo ""
echo "✓ Creating directories..."
mkdir -p data/resumes data/vector_db logs
echo "  ✅ Directories created"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "✓ Creating .env file with Azure OpenAI credentials..."
    cat > .env <<EOF
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://itcmentor.openai.azure.com/
AZURE_OPENAI_API_KEY=4FuAkN0MCCjWTv2zGuwvOw622IjmsnwWbh0SCo7U2xuNhP3rY3AoJQQJ99BlACYeBjFXj3w3AAABACOGrcAG
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_GPT_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_EMBEDDING_DIMENSION=3072

# App Configuration
AI_PROVIDER=azure
AZURE_OPENAI_ENABLED=True
USE_SAMPLE_DATA=True
LOG_LEVEL=INFO
EOF
    echo "  ✅ .env file created"
else
    echo "  ✅ .env file already exists"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ Setup complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "To run the app, use:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  streamlit run frontend/streamlit_app.py"
echo ""
