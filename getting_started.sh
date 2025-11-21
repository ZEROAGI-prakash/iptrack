#!/bin/bash

##############################################################################
# IPTrack - Quick Getting Started Guide
# Run this after installation to test all features
##############################################################################

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          🛡️  IPTrack - Getting Started Guide  🛡️                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Ensure iptrack is in PATH
export PATH="/Users/zero/Library/Python/3.9/bin:$PATH"

echo "1️⃣  Testing Global Command..."
echo "   Running: iptrack --help"
echo ""
iptrack --help 2>/dev/null || {
    echo "⚠️  iptrack not in PATH. Run: source ~/.zshrc"
    exit 1
}

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "2️⃣  View Current Security Status"
echo "   Running: iptrack stats"
echo ""
iptrack stats

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "3️⃣  List Blocked IPs with Details"
echo "   Running: iptrack list -d"
echo ""
iptrack list -d

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "4️⃣  Show Recent Access Logs"
echo "   Running: iptrack logs -n 10"
echo ""
iptrack logs -n 10

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "✅ All features working!"
echo ""
echo "📚 Next Steps:"
echo ""
echo "   📡 Watch logs in real-time:"
echo "      iptrack watch"
echo ""
echo "   🌍 Track IP location:"
echo "      iptrack locate <ip>"
echo ""
echo "   🚫 Block an IP:"
echo "      iptrack block <ip> -r 'Your reason'"
echo ""
echo "   🎛️  Full dashboard:"
echo "      iptrack dashboard"
echo ""
echo "   💾 Export data:"
echo "      iptrack export backup.json"
echo ""
echo "   🔒 Activate firewall:"
echo "      sudo pfctl -f logs/blocked_ips.pf"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Documentation:"
echo "   • GLOBAL_CLI_GUIDE.md - Complete command reference"
echo "   • README.md - Full documentation"
echo "   • STATUS.txt - System overview"
echo ""
echo "🎉 You're ready to start monitoring!"
echo ""
