#!/bin/bash

# Defender Security System - Installation Script for macOS

echo "🛡️  Installing Defender Security System..."
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create logs directory
echo ""
echo "Creating logs directory..."
mkdir -p logs
echo "✅ Logs directory created"

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x security_monitor.py
chmod +x ip_locator.py
chmod +x defender_control.py
chmod +x quick_start.py
echo "✅ Scripts are now executable"

# Run quick demo
echo ""
echo "🎉 Installation complete!"
echo ""
echo "To get started, run the demo:"
echo "  python3 quick_start.py"
echo ""
echo "Or check the dashboard:"
echo "  python3 defender_control.py dashboard"
echo ""
echo "For help:"
echo "  python3 defender_control.py help"
echo ""
echo "📖 Read README.md for full documentation"
echo ""
