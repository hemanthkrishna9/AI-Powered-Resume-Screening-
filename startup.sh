#!/bin/bash

# Startup script for Azure App Service
# This script runs when the container starts

echo "Starting AI Resume Screening Application..."

# Install spaCy model if not present
echo "Checking spaCy model..."
python -m spacy download en_core_web_sm --quiet || true

# Create necessary directories
echo "Creating directories..."
mkdir -p data/resumes
mkdir -p data/vector_db
mkdir -p logs

# Start Streamlit app
echo "Starting Streamlit server..."
streamlit run frontend/streamlit_app.py \
    --server.port=8000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
