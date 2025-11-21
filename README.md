# IPTrack - Professional Security Monitoring CLI Tool

🛡️ **Professional command-line security monitoring and IP blocking tool with real-time alerts and geolocation tracking**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

## 🌟 Features

- 🔴 **Real-Time Log Monitoring** - Watch security events as they happen
- 🚫 **Automatic IP Blocking** - Auto-block after configurable failed attempts
- 🌍 **IP Geolocation** - Track attacker locations worldwide
- 📊 **Security Dashboard** - Comprehensive security overview
- 💾 **Data Export** - Export logs and analytics
- 🎨 **Beautiful CLI** - Gemini-style colorful interface
- ⚡ **Global Command** - Works from any directory

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/iptrack.git
cd iptrack

# Run installer
./install_global.sh

# Reload shell
source ~/.zshrc

# Start using
iptrack
```

### Basic Usage

```bash
# Watch security logs in real-time
iptrack watch

# View security dashboard
iptrack dashboard

# Block an IP address
iptrack block 192.168.1.100 -r "Suspicious activity"

# Find IP location
iptrack locate 8.8.8.8

# List blocked IPs
iptrack list -d

# Show statistics
iptrack stats
```

---

## 📖 Documentation

### Commands

| Command | Description |
|---------|-------------|
| `iptrack` | Show welcome screen and available commands |
| `iptrack watch` | Watch security logs in real-time |
| `iptrack block <ip>` | Block an IP address |
| `iptrack unblock <ip>` | Unblock an IP address |
| `iptrack list` | List all blocked IPs |
| `iptrack list -d` | List blocked IPs with location details |
| `iptrack locate <ip>` | Find IP geolocation |
| `iptrack stats` | Show security statistics |
| `iptrack logs` | Show recent access attempts |
| `iptrack dashboard` | Show full security dashboard |
| `iptrack export <file>` | Export security data |
| `iptrack help` | Show detailed help |

### Examples

```bash
# Monitor system in real-time
iptrack watch

# Block an attacker with reason
iptrack block 45.142.120.10 -r "SSH brute force attempt"

# Find where attacker is located
iptrack locate 45.142.120.10
# Output:
# 📍 Location: Sandanski, Bulgaria
# 🗺️  View on map: https://www.google.com/maps?q=41.5678,23.2804

# See all blocked IPs with details
iptrack list -d

# Export security data for analysis
iptrack export security_backup.json
```

---

## 🎨 Screenshots

### Welcome Screen
```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              🛡️  IPTrack Security Tool v1.0.0 🛡️                  ║
║                                                                    ║
║         Professional CLI Security Monitoring & IP Blocking         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

### Dashboard Output
```
📊 Security Statistics
======================================================================
Total Access Attempts: 15
Unique IPs Attempted: 5
Currently Blocked: 3

Blocked IPs:
  • 45.142.120.10 (Bulgaria)
  • 185.220.101.50 (Germany)
  • 203.0.113.50 (United States)
```

---

## 🔧 Configuration

Edit `config.json` to customize settings:

```json
{
  "max_attempts": 3,
  "auto_block": true,
  "whitelist_ips": ["127.0.0.1"],
  "geolocation": {
    "enabled": true,
    "cache_duration_days": 7
  }
}
```

---

## 🛠️ Requirements

- **OS**: macOS 10.15 or higher
- **Python**: 3.7+
- **Internet**: Required for IP geolocation
- **Permissions**: sudo for firewall activation

---

## 📦 Installation Methods

### Method 1: Global Installation (Recommended)
```bash
./install_global.sh
source ~/.zshrc
```

### Method 2: System-Wide (All Users)
```bash
sudo ./install_global.sh
```

### Method 3: Manual Installation
```bash
pip3 install --user -e .
export PATH="/Users/$USER/Library/Python/3.9/bin:$PATH"
```

---

## 🔒 Activating Firewall Rules

After blocking IPs, activate macOS firewall:

```bash
# View generated rules
cat logs/blocked_ips.pf

# Apply rules (requires sudo)
sudo pfctl -f logs/blocked_ips.pf

# Verify rules
sudo pfctl -s rules | grep block
```

---

## 📊 Features Overview

### Real-Time Monitoring
```bash
iptrack watch
```
- Live tail of security logs
- See attacks as they happen
- Press Ctrl+C to stop

### IP Geolocation
```bash
iptrack locate 8.8.8.8
```
- Shows city, country, coordinates
- ISP and organization info
- Google Maps integration
- FREE APIs (no keys needed)

### Automatic Blocking
- Auto-blocks after 3 failed attempts (configurable)
- Manual blocking with custom reasons
- Easy to reverse (unblock)
- macOS firewall integration

---

## 🌍 IP Geolocation APIs

Uses multiple free APIs with automatic fallback:
- ip-api.com
- ipapi.co
- ipwhois.app

No API key required!

---

## 📁 Project Structure

```
iptrack/
├── iptrack                  # Main CLI tool
├── security_monitor.py      # Monitoring engine
├── ip_locator.py           # Geolocation tracker
├── defender_control.py     # Control panel
├── setup.py                # Package configuration
├── install_global.sh       # Global installer
├── requirements.txt        # Dependencies
├── config.json             # Configuration
├── logs/                   # Security logs
│   ├── blocked_ips.json
│   ├── login_attempts.json
│   ├── ip_locations.json
│   └── blocked_ips.pf
└── docs/                   # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with Python
- Inspired by Gemini CLI and GitHub CLI
- Uses free IP geolocation APIs
- macOS firewall integration via pfctl

---

## 📞 Support

- **Documentation**: See [GLOBAL_CLI_GUIDE.md](GLOBAL_CLI_GUIDE.md)
- **Quick Reference**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Issues**: GitHub Issues
- **Help**: `iptrack help`

---

## 🎯 Use Cases

- **Home Security**: Monitor who's trying to access your Mac
- **Server Administration**: Track unauthorized access attempts
- **Development**: Test security features
- **Learning**: Understand IP blocking and geolocation
- **Network Admin**: Track and block malicious IPs

---

## ⚡ Quick Examples

```bash
# Daily security check
iptrack stats && iptrack list -d

# Block and locate
iptrack block 192.168.1.100 -r "Port scanning"
iptrack locate 192.168.1.100

# Export for records
iptrack export daily_$(date +%Y%m%d).json

# Real-time monitoring in tmux
tmux new -s security
iptrack watch
# Ctrl+B then D to detach
```

---

## 🔐 Security Best Practices

1. Regularly check the dashboard
2. Export logs periodically
3. Review blocked IPs weekly
4. Keep whitelist updated
5. Monitor security logs daily

---

## 📈 Roadmap

- [ ] Email alerts
- [ ] Web dashboard
- [ ] Linux support
- [ ] Database integration
- [ ] Advanced analytics
- [ ] Custom rule engine

---

## ⭐ Star History

If you find this tool useful, please consider giving it a star!

---

**Made with 🛡️ for macOS Security**

*Professional security monitoring made simple*
