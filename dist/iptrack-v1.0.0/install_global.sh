#!/bin/bash

#############################################
# IPTrack Global Installation Script
# Installs iptrack command for all users
#############################################

set -e  # Exit on any error

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    IPTrack Security Tool                           ║"
echo "║              Global Installation Script v1.0                       ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root for system-wide install
INSTALL_TYPE="user"
if [ "$EUID" -eq 0 ]; then 
    INSTALL_TYPE="system"
    echo -e "${YELLOW}⚠️  Running as root - will install system-wide for all users${NC}"
else
    echo -e "${BLUE}ℹ️  Running as user - will install for current user only${NC}"
    echo -e "${YELLOW}   For system-wide installation, run: sudo ./install_global.sh${NC}"
fi
echo ""

# Check Python version
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check pip
echo ""
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed${NC}"
    echo "Please install pip3"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"

# Install Python package
echo ""
echo "📦 Installing IPTrack package..."

if [ "$INSTALL_TYPE" = "system" ]; then
    # System-wide installation
    pip3 install -e . --no-cache-dir
else
    # User installation
    pip3 install --user -e . --no-cache-dir
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Package installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install package${NC}"
    exit 1
fi

# Create logs directory with proper permissions
echo ""
echo "📁 Setting up directories..."

INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOGS_DIR="$INSTALL_DIR/logs"

mkdir -p "$LOGS_DIR"

if [ "$INSTALL_TYPE" = "system" ]; then
    # Set permissions for system-wide logs
    chmod 755 "$INSTALL_DIR"
    chmod 777 "$LOGS_DIR"  # Allow all users to write logs
    echo -e "${GREEN}✅ Created shared logs directory: $LOGS_DIR${NC}"
else
    chmod 755 "$LOGS_DIR"
    echo -e "${GREEN}✅ Created logs directory: $LOGS_DIR${NC}"
fi

# Make main script executable
chmod +x "$INSTALL_DIR/iptrack"

# Test installation
echo ""
echo "🧪 Testing installation..."
if command -v iptrack &> /dev/null; then
    echo -e "${GREEN}✅ iptrack command is available globally${NC}"
    
    # Show version/help
    echo ""
    echo "Running: iptrack --help"
    echo "─────────────────────────────────────────────────────────────────"
    iptrack --help
else
    echo -e "${YELLOW}⚠️  iptrack command not found in PATH${NC}"
    
    if [ "$INSTALL_TYPE" = "user" ]; then
        # Get user's pip install location
        USER_BIN=$(python3 -m site --user-base)/bin
        
        echo ""
        echo -e "${YELLOW}You may need to add Python user bin to your PATH:${NC}"
        echo ""
        echo "Add this line to your ~/.zshrc or ~/.bash_profile:"
        echo -e "${BLUE}export PATH=\"$USER_BIN:\$PATH\"${NC}"
        echo ""
        echo "Then run:"
        echo -e "${BLUE}source ~/.zshrc${NC}  # or source ~/.bash_profile"
        echo ""
        
        # Try to add to PATH automatically
        if [[ -f ~/.zshrc ]]; then
            if ! grep -q "export PATH=\"$USER_BIN:\$PATH\"" ~/.zshrc; then
                echo ""
                read -p "Would you like to add it to ~/.zshrc automatically? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo "" >> ~/.zshrc
                    echo "# Added by IPTrack installer" >> ~/.zshrc
                    echo "export PATH=\"$USER_BIN:\$PATH\"" >> ~/.zshrc
                    echo -e "${GREEN}✅ Added to ~/.zshrc${NC}"
                    echo "Run: source ~/.zshrc"
                fi
            fi
        fi
    fi
fi

# Create initial config if it doesn't exist
CONFIG_FILE="$INSTALL_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "⚙️  Creating default configuration..."
    cat > "$CONFIG_FILE" << 'EOF'
{
  "max_attempts": 3,
  "block_duration_minutes": 60,
  "monitor_auth_log": true,
  "auto_block": true,
  "alert_email": null,
  "whitelist_ips": [
    "127.0.0.1",
    "::1"
  ],
  "monitoring": {
    "check_interval_seconds": 60,
    "log_retention_days": 30
  },
  "geolocation": {
    "enabled": true,
    "cache_duration_days": 7
  },
  "notifications": {
    "log_to_console": true,
    "log_to_file": true,
    "send_email_alerts": false
  }
}
EOF
    echo -e "${GREEN}✅ Configuration file created${NC}"
fi

# Show completion message
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                   Installation Complete! 🎉                        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ IPTrack is now installed${NC}"
echo ""
echo "📖 Quick Start:"
echo "   iptrack watch          - Watch logs in real-time"
echo "   iptrack dashboard      - View security dashboard"
echo "   iptrack list           - List blocked IPs"
echo "   iptrack block <ip>     - Block an IP address"
echo "   iptrack locate <ip>    - Find IP location"
echo "   iptrack --help         - Show all commands"
echo ""
echo "📁 Installation directory: $INSTALL_DIR"
echo "📝 Logs directory: $LOGS_DIR"
echo "⚙️  Config file: $CONFIG_FILE"
echo ""

if [ "$INSTALL_TYPE" = "system" ]; then
    echo -e "${GREEN}🌍 Installed system-wide - available to all users${NC}"
else
    echo -e "${BLUE}👤 Installed for current user${NC}"
fi

echo ""
echo "🔒 To activate firewall blocking on macOS:"
echo "   sudo pfctl -f $LOGS_DIR/blocked_ips.pf"
echo ""
echo "📚 Documentation: cat README.md"
echo "💡 Quick reference: cat QUICK_REFERENCE.md"
echo ""
echo "─────────────────────────────────────────────────────────────────────"
echo ""
