#!/bin/bash

# Setup script for Google Maps API Key
# This script helps you set up your API key securely as an environment variable

echo "Google Maps API Key Setup"
echo "========================="
echo ""
echo "This script will help you set up your Google Maps API key securely."
echo "The API key will be stored as an environment variable instead of in code."
echo ""

# Check if API key is already set
if [ -n "$GOOGLE_MAPS_API_KEY" ]; then
    echo "✓ GOOGLE_MAPS_API_KEY is already set in your environment"
    echo "Current key starts with: ${GOOGLE_MAPS_API_KEY:0:10}..."
    exit 0
fi

echo "To set up your API key:"
echo "1. Get your Google Maps API key from Google Cloud Console"
echo "2. Run this command in your terminal:"
echo ""
echo "   export GOOGLE_MAPS_API_KEY='your_actual_api_key_here'"
echo ""
echo "3. To make it permanent, add the above line to your ~/.zshrc or ~/.bashrc"
echo ""
echo "Security Note: Never commit API keys to version control!"
echo "This repository now uses environment variables to protect your credentials." 