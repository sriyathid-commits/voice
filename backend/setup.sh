#!/bin/bash
# Voice for Bharat Backend Setup Script

set -e

echo "🚀 Setting up Voice for Bharat Backend..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3.11 --version 2>&1 | awk '{print $2}')
if [[ -z "$python_version" ]]; then
    echo "❌ Python 3.11 not found. Please install Python 3.11 first."
    exit 1
fi
echo "✅ Python $python_version found"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing..."
    rm -rf venv
fi
python3.11 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install root dependencies
echo "📥 Installing root dependencies..."
pip install -r requirements.txt

# Install service-specific dependencies
echo "📥 Installing service-specific dependencies..."
services=("user_service" "voice_service" "scheme_service" "application_service" "document_service" "notification_service" "sync_service")

for service in "${services[@]}"; do
    echo "  Installing dependencies for $service..."
    pip install -r "lambdas/$service/requirements.txt"
done

echo "✅ All dependencies installed"

# Check AWS CLI
echo "📋 Checking AWS CLI..."
if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI not found. Please install AWS CLI to deploy."
else
    aws_version=$(aws --version 2>&1 | awk '{print $1}')
    echo "✅ $aws_version found"
fi

# Check SAM CLI
echo "📋 Checking SAM CLI..."
if ! command -v sam &> /dev/null; then
    echo "⚠️  SAM CLI not found. Please install SAM CLI to deploy."
else
    sam_version=$(sam --version 2>&1)
    echo "✅ $sam_version found"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Configure AWS credentials: aws configure"
echo "3. Build the application: sam build"
echo "4. Deploy to AWS: sam deploy --guided"
echo ""
