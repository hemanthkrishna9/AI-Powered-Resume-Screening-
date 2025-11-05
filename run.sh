#!/bin/bash

# Quick Run Script - Start the AI Resume Screener

echo "🚀 Starting AI Resume Screener..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Using defaults..."
fi

echo "✅ Starting Streamlit app..."
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🎯 AI-Powered Resume Screening System"
echo "  🌐 Opening in browser..."
echo "  📍 URL: http://localhost:8501"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run frontend/streamlit_app.py
