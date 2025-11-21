#!/bin/bash

##############################################################################
# IPTrack Distribution Package Creator
# Creates a ready-to-distribute package for sharing with other users
##############################################################################

set -e

PACKAGE_NAME="iptrack-v1.0.0"
DIST_DIR="dist"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║           IPTrack Distribution Package Creator                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Create distribution directory
echo "📦 Creating distribution package..."
rm -rf "$DIST_DIR/$PACKAGE_NAME"
mkdir -p "$DIST_DIR/$PACKAGE_NAME"

# Copy essential files
echo "📋 Copying files..."
cp iptrack "$DIST_DIR/$PACKAGE_NAME/"
cp security_monitor.py "$DIST_DIR/$PACKAGE_NAME/"
cp ip_locator.py "$DIST_DIR/$PACKAGE_NAME/"
cp defender_control.py "$DIST_DIR/$PACKAGE_NAME/"
cp quick_start.py "$DIST_DIR/$PACKAGE_NAME/"
cp setup.py "$DIST_DIR/$PACKAGE_NAME/"
cp install_global.sh "$DIST_DIR/$PACKAGE_NAME/"
cp requirements.txt "$DIST_DIR/$PACKAGE_NAME/"
cp config.json "$DIST_DIR/$PACKAGE_NAME/"
cp README.md "$DIST_DIR/$PACKAGE_NAME/"
cp QUICK_REFERENCE.md "$DIST_DIR/$PACKAGE_NAME/"
cp GLOBAL_CLI_GUIDE.md "$DIST_DIR/$PACKAGE_NAME/"
cp LICENSE "$DIST_DIR/$PACKAGE_NAME/"
cp MANIFEST.in "$DIST_DIR/$PACKAGE_NAME/" 2>/dev/null || true

# Create installation instructions
cat > "$DIST_DIR/$PACKAGE_NAME/INSTALL.txt" << 'EOF'
╔════════════════════════════════════════════════════════════════════╗
║                  IPTrack Security Tool v1.0.0                      ║
║                      Installation Guide                            ║
╚════════════════════════════════════════════════════════════════════╝

QUICK INSTALL
═════════════

1. Open Terminal and navigate to this folder:
   cd /path/to/iptrack-v1.0.0

2. Run the installer:
   ./install_global.sh

3. Reload your shell:
   source ~/.zshrc

4. Test the installation:
   iptrack --help

5. Start using:
   iptrack dashboard


SYSTEM-WIDE INSTALLATION (All Users)
═════════════════════════════════════

For installing on a server for all users:
   sudo ./install_global.sh


REQUIREMENTS
════════════

• macOS 10.15 or higher
• Python 3.7+
• Internet connection (for IP geolocation)


QUICK START
═══════════

# Watch security logs in real-time
iptrack watch

# View dashboard
iptrack dashboard

# Block an IP
iptrack block 192.168.1.100

# Find IP location
iptrack locate 8.8.8.8

# Show all commands
iptrack --help


DOCUMENTATION
═════════════

• README.md - Full documentation
• GLOBAL_CLI_GUIDE.md - Complete command reference
• QUICK_REFERENCE.md - Quick command cheat sheet


SUPPORT
═══════

For help: iptrack --help
For issues: Check README.md troubleshooting section


LICENSE
═══════

MIT License - Free for personal and commercial use
See LICENSE file for details

════════════════════════════════════════════════════════════════════

Happy monitoring! 🛡️
EOF

# Make scripts executable
chmod +x "$DIST_DIR/$PACKAGE_NAME/iptrack"
chmod +x "$DIST_DIR/$PACKAGE_NAME/install_global.sh"
chmod +x "$DIST_DIR/$PACKAGE_NAME/quick_start.py"

# Create archive
echo ""
echo "📦 Creating archive..."
cd "$DIST_DIR"
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME"
zip -r -q "$PACKAGE_NAME.zip" "$PACKAGE_NAME"
cd ..

# Calculate checksums
echo ""
echo "🔐 Generating checksums..."
cd "$DIST_DIR"
shasum -a 256 "$PACKAGE_NAME.tar.gz" > "$PACKAGE_NAME.tar.gz.sha256"
shasum -a 256 "$PACKAGE_NAME.zip" > "$PACKAGE_NAME.zip.sha256"
cd ..

# Display results
echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                   Package Created Successfully! 🎉                 ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Distribution packages created in: $DIST_DIR/"
echo ""
ls -lh "$DIST_DIR/$PACKAGE_NAME."*
echo ""
echo "✅ Ready for distribution!"
echo ""
echo "Share these files:"
echo "  • $DIST_DIR/$PACKAGE_NAME.tar.gz (for macOS/Linux)"
echo "  • $DIST_DIR/$PACKAGE_NAME.zip (for all platforms)"
echo ""
echo "Users should:"
echo "  1. Extract the archive"
echo "  2. Run: ./install_global.sh"
echo "  3. Use: iptrack --help"
echo ""
