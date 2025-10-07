#!/bin/bash

echo "🔄 Rebuilding FAISS Vector Store with Updated Data"
echo "=================================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "💡 Run: bash setup_env.sh"
    exit 1
fi

# Delete old FAISS index
echo "🗑️  Deleting old FAISS index..."
rm -rf faiss_index/
echo "✅ Old index deleted"
echo ""

# Rebuild index by running the test script
echo "🔨 Building new FAISS index with updated data..."
echo "📁 Loading files from data/ directory:"
ls -1 data/
echo ""

python test_prototype.py

echo ""
echo "✅ FAISS index rebuilt successfully!"
echo "🚀 You can now restart the backend server"
