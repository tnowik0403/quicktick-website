#!/bin/bash
#
# Monthly Update Script for Quick Tick
# 
# This script automates the monthly data regeneration process.
# Run this once a month to keep your company data fresh.
#
# Usage:
#   chmod +x monthly_update.sh
#   ./monthly_update.sh
#

echo "=========================================="
echo "Quick Tick - Monthly Update"
echo "=========================================="
echo ""

# Check if API key is set
if [ -z "$XAI_API_KEY" ]; then
    echo "ERROR: XAI_API_KEY not set"
    echo ""
    echo "Please set your API key first:"
    echo "  export XAI_API_KEY='your-key-here'"
    echo ""
    exit 1
fi

echo "✓ API key found"
echo ""

# Check if Python script exists
if [ ! -f "generate_company_data.py" ]; then
    echo "ERROR: generate_company_data.py not found"
    echo "Make sure you're in the correct directory"
    exit 1
fi

echo "Starting data generation..."
echo "This may take a while depending on the number of companies."
echo ""

# Run the Python script
python3 generate_company_data.py

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Update Complete!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Test locally: python3 -m http.server 8000"
    echo "2. Upload the 'data' folder to your web hosting"
    echo "3. Set a reminder for next month!"
    echo ""
else
    echo ""
    echo "ERROR: Data generation failed"
    echo "Check the error messages above for details"
    exit 1
fi
