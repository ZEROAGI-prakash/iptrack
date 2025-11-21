# 🛡️ DEFENDER Security System - Quick Reference

## 🚀 QUICK START

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run demo
python3 quick_start.py

# View dashboard
python3 defender_control.py dashboard
```

## 📋 COMMON COMMANDS

### Monitor & Block
```bash
# Log an access attempt
python3 security_monitor.py log <IP> <username>

# Manually block an IP
python3 security_monitor.py block <IP>

# View all blocked IPs
python3 security_monitor.py list

# Show statistics
python3 security_monitor.py stats
```

### Track Location
```bash
# Find attacker location
python3 ip_locator.py <IP>

# Detailed location report
python3 ip_locator.py report <IP>

# Via control panel
python3 defender_control.py locate <IP>
```

### Unblock & Reverse
```bash
# Unblock specific IP
python3 defender_control.py unblock <IP>

# Unblock all IPs
python3 defender_control.py unblock-all

# View logs for specific IP
python3 defender_control.py logs <IP>
```

### Dashboard & Export
```bash
# View dashboard
python3 defender_control.py dashboard

# Export all data
python3 defender_control.py export backup.json

# Reset system
python3 defender_control.py reset
```

## 🔒 ACTIVATE FIREWALL BLOCKING

```bash
# View generated rules
cat logs/blocked_ips.pf

# Apply rules (requires sudo)
sudo pfctl -f logs/blocked_ips.pf

# Check firewall status
sudo pfctl -s rules
```

## 📊 KEY FEATURES

✅ **Auto-blocking** after 3 failed attempts (configurable)
✅ **IP Geolocation** with city, country, ISP
✅ **Reversible** - easily unblock IPs
✅ **Detailed Logging** - all attempts tracked
✅ **Dashboard** - see everything at a glance
✅ **Export Data** - backup your security logs

## 🎯 TYPICAL WORKFLOW

1. **Someone tries to access your system**
   - System logs the attempt automatically
   - After 3 attempts, IP is blocked

2. **Check who's attacking**
   ```bash
   python3 defender_control.py dashboard
   ```

3. **Find attacker location**
   ```bash
   python3 defender_control.py locate 45.142.120.10
   ```

4. **View on Google Maps**
   - Automatic map link generated
   - Shows exact coordinates

5. **Unblock if needed**
   ```bash
   python3 defender_control.py unblock 45.142.120.10
   ```

## 📁 FILES STRUCTURE

```
difender/
├── security_monitor.py      # Core monitoring engine
├── ip_locator.py            # Location tracker
├── defender_control.py      # Control panel
├── quick_start.py           # Demo script
├── config.json              # Settings
└── logs/                    # All data stored here
    ├── blocked_ips.json     # Blocked IPs database
    ├── login_attempts.json  # All attempts log
    ├── ip_locations.json    # Location cache
    ├── blocked_ips.pf       # Firewall rules
    └── security_*.log       # Daily logs
```

## ⚙️ CONFIGURATION

Edit `config.json`:
```json
{
  "max_attempts": 3,           // Failed attempts before block
  "auto_block": true,          // Auto-block enabled
  "whitelist_ips": [           // Never block these IPs
    "127.0.0.1"
  ]
}
```

## 🔥 EXAMPLES

### Simulate Attack (Testing)
```bash
python3 security_monitor.py simulate 192.168.1.100
```

### View All Logs
```bash
python3 defender_control.py logs
```

### Export Evidence
```bash
python3 defender_control.py export evidence.json
```

### Get Help
```bash
python3 defender_control.py help
```

## 🌍 LOCATION TRACKING

- Uses **FREE** IP geolocation APIs
- No API key required
- Shows:
  - Country, City, Region
  - Latitude/Longitude
  - ISP and Organization
  - Google Maps link

## 🚨 IMPORTANT

1. **macOS Only** - Uses pfctl firewall
2. **Sudo Required** - Firewall changes need admin
3. **Internet Needed** - For IP geolocation
4. **Local Storage** - All data in `logs/` folder

## 💡 PRO TIPS

- Check dashboard regularly
- Export logs weekly for backup
- Review blocked IPs before applying firewall rules
- Use whitelist for trusted IPs
- Monitor the security logs daily

---

**Need Help?** Check `README.md` for full documentation
