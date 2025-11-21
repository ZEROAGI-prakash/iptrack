# 🛡️ IPTrack - Professional Security CLI Tool

## Global Command Line Tool for Security Monitoring & IP Blocking

IPTrack is a production-ready CLI tool that provides comprehensive security monitoring, automatic IP blocking, real-time log watching, and geolocation tracking for unauthorized access attempts.

---

## ⚡ Installation

### Quick Install (Current User)
```bash
./install_global.sh
source ~/.zshrc  # Reload shell
```

### System-Wide Install (All Users)
```bash
sudo ./install_global.sh
```

### Verify Installation
```bash
iptrack --help
```

---

## 🚀 Command Reference

### Real-Time Log Monitoring
```bash
# Watch security logs in real-time (like tail -f)
iptrack watch

# Show last 100 lines then watch
iptrack watch -n 100

# Just show last 50 lines (no follow)
iptrack watch --no-follow
```

### Block Management
```bash
# Block an IP
iptrack block 192.168.1.100

# Block with custom reason
iptrack block 192.168.1.100 -r "Port scanning detected"

# Unblock an IP
iptrack unblock 192.168.1.100

# Unblock all IPs
iptrack unblock-all

# List blocked IPs
iptrack list

# List with location details
iptrack list -d
```

### IP Geolocation
```bash
# Find location of any IP
iptrack locate 8.8.8.8

# Locate attacker
iptrack locate 45.142.120.10
```

### Logs & Statistics
```bash
# Show recent access attempts
iptrack logs

# Show last 50 attempts
iptrack logs -n 50

# Show logs for specific IP
iptrack logs 192.168.1.100

# View statistics
iptrack stats

# Full dashboard
iptrack dashboard
```

### Data Management
```bash
# Export all security data
iptrack export backup.json

# Reset system (clear all data)
iptrack reset
```

---

## 📊 Usage Examples

### Scenario 1: Monitor System in Real-Time
```bash
# Terminal 1: Watch logs
iptrack watch

# Terminal 2: Your work
# All security events appear instantly in Terminal 1
```

### Scenario 2: Block Attacker & Find Location
```bash
# Someone is attacking
iptrack block 45.142.120.10 -r "Brute force attack"

# Find where they're from
iptrack locate 45.142.120.10

# Output:
# 📍 Location for 45.142.120.10:
#    Sandanski, Bulgaria (41.5678, 23.2804)
#    ISP: Cloudflare London, LLC
#    🗺️  View on map: https://www.google.com/maps?q=41.5678,23.2804
```

### Scenario 3: Review & Unblock
```bash
# Check who's blocked
iptrack list -d

# Review logs for specific IP
iptrack logs 192.168.1.100

# Decide to unblock
iptrack unblock 192.168.1.100
```

### Scenario 4: Daily Security Check
```bash
# Quick stats
iptrack stats

# See today's attempts
iptrack logs -n 100

# Export for records
iptrack export daily_$(date +%Y%m%d).json
```

---

## 🎯 Key Features

### ✅ Global CLI Command
- Works from **any directory** in terminal
- Just type `iptrack` anywhere
- No need to navigate to installation folder

### ✅ Real-Time Log Monitoring
- Live tail of security logs
- See attacks as they happen
- Press Ctrl+C to stop

### ✅ Automatic IP Blocking
- Auto-blocks after 3 failed attempts (configurable)
- Manual blocking with custom reasons
- Reversible - easy to unblock

### ✅ IP Geolocation
- Shows country, city, coordinates
- ISP and organization info
- Google Maps integration
- Uses FREE APIs (no keys needed)

### ✅ Comprehensive Logging
- All attempts logged with timestamps
- Per-IP attempt tracking
- Daily log rotation
- Export capabilities

### ✅ macOS Firewall Integration
- Generates pfctl firewall rules
- Easy activation with one command

---

## 🔒 Activating Firewall Rules

After blocking IPs, activate the firewall:

```bash
# View generated rules
cat /Users/zero/difender/logs/blocked_ips.pf

# Apply rules (requires sudo)
sudo pfctl -f /Users/zero/difender/logs/blocked_ips.pf

# Verify rules are active
sudo pfctl -s rules | grep block
```

---

## ⚙️ Configuration

Edit `config.json` in the installation directory:

```json
{
  "max_attempts": 3,           // Attempts before auto-block
  "auto_block": true,          // Enable auto-blocking
  "whitelist_ips": [           // Never block these
    "127.0.0.1",
    "::1"
  ],
  "geolocation": {
    "enabled": true,           // Enable IP location tracking
    "cache_duration_days": 7   // Cache locations for 7 days
  }
}
```

---

## 📁 File Locations

```
Installation: /Users/zero/difender/
Logs:         /Users/zero/difender/logs/
Config:       /Users/zero/difender/config.json
Binary:       /Users/zero/Library/Python/3.9/bin/iptrack
```

### Log Files
- `security_YYYYMMDD.log` - Daily security logs
- `blocked_ips.json` - Blocked IPs database
- `login_attempts.json` - All access attempts
- `ip_locations.json` - Geolocation cache
- `blocked_ips.pf` - macOS firewall rules

---

## 🎨 Output Examples

### Dashboard View
```
🛡️  DEFENDER SECURITY DASHBOARD
======================================================================

📊 Statistics:
   Total Access Attempts: 15
   Unique IPs Attempted: 5
   Currently Blocked: 3

🚫 Blocked IPs:

   IP: 45.142.120.10
   Blocked At: 2025-11-21T21:43:56
   Reason: Too many failed attempts
   Attempts: 5
   Location: Sandanski, Bulgaria
   ISP: Cloudflare London, LLC
```

### Real-Time Logs
```
📡 Watching security logs: /Users/zero/difender/logs/security_20251121.log
======================================================================
Press Ctrl+C to stop

2025-11-21 21:43:56 - WARNING - Access attempt from 45.142.120.10 - User: hacker1 - Status: failed - Attempt #1
2025-11-21 21:43:56 - WARNING - Access attempt from 45.142.120.10 - User: hacker1 - Status: failed - Attempt #2
2025-11-21 21:43:56 - WARNING - Access attempt from 45.142.120.10 - User: hacker1 - Status: failed - Attempt #3
2025-11-21 21:43:56 - CRITICAL - 🚫 BLOCKED IP: 45.142.120.10 - Reason: Too many failed attempts
```

---

## 💡 Pro Tips

### 1. Keep it Running
Run in a tmux or screen session to monitor 24/7:
```bash
tmux new -s iptrack
iptrack watch
# Ctrl+B then D to detach
```

### 2. Daily Routine
```bash
# Morning check
iptrack stats && iptrack list -d

# Export weekly
iptrack export weekly_backup.json
```

### 3. Quick Investigation
```bash
# Suspicious IP?
iptrack locate <IP> && iptrack logs <IP>
```

### 4. Auto-Export Cron Job
```bash
# Add to crontab
0 0 * * * /Users/zero/Library/Python/3.9/bin/iptrack export /backups/iptrack_$(date +\%Y\%m\%d).json
```

---

## 🌍 For Distribution to Others

### Package Files
Include these files when sharing:
```
difender/
├── iptrack                  # Main CLI tool
├── security_monitor.py      # Core engine
├── ip_locator.py           # Geolocation module
├── defender_control.py     # Control panel
├── setup.py                # Installation config
├── install_global.sh       # Install script
├── requirements.txt        # Dependencies
├── config.json             # Configuration
├── README.md               # Full docs
├── QUICK_REFERENCE.md      # Command reference
└── LICENSE                 # MIT License
```

### Installation Instructions for Users
```bash
# 1. Extract the package
cd difender

# 2. Run installer
./install_global.sh

# 3. Reload shell
source ~/.zshrc

# 4. Start using
iptrack --help
```

---

## 🚨 Requirements

- **OS**: macOS (tested on macOS 10.15+)
- **Python**: 3.7 or higher
- **Internet**: Required for IP geolocation
- **Permissions**: sudo for firewall activation

---

## 🔧 Troubleshooting

### Command Not Found
```bash
# Add to PATH manually
export PATH="/Users/zero/Library/Python/3.9/bin:$PATH"
echo 'export PATH="/Users/zero/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Permission Denied
```bash
# Make script executable
chmod +x /Users/zero/difender/iptrack
```

### Firewall Not Blocking
```bash
# Check if rules are loaded
sudo pfctl -s rules | grep block

# Reload firewall rules
sudo pfctl -f /Users/zero/difender/logs/blocked_ips.pf
```

### Geolocation Not Working
- Check internet connection
- Free APIs have rate limits (wait 1 minute)
- Try again or use cached data

---

## 📞 Support & Help

```bash
# Show help
iptrack --help

# Show help for specific command
iptrack watch --help
iptrack block --help
iptrack list --help
```

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 🎯 Quick Command Cheat Sheet

```bash
iptrack watch              # 👁️  Watch logs in real-time
iptrack block <ip>         # 🚫 Block an IP
iptrack unblock <ip>       # ✅ Unblock an IP
iptrack list -d            # 📋 List blocked IPs with details
iptrack locate <ip>        # 🌍 Find IP location
iptrack stats              # 📊 Show statistics
iptrack logs               # 📝 Show recent logs
iptrack dashboard          # 🎛️  Full dashboard
iptrack export <file>      # 💾 Export data
iptrack --help             # ❓ Show help
```

---

**IPTrack v1.0.0** - Professional Security Monitoring Made Simple 🛡️
