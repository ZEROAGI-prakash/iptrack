#!/usr/bin/env python3
"""
Security Monitor System
Tracks unauthorized access attempts, blocks IPs, and logs all activities
"""

import os
import sys
import json
import logging
import subprocess
import hashlib
from datetime import datetime
from pathlib import Path
import socket
import re

class SecurityMonitor:
    def __init__(self, log_dir="logs", config_file="config.json"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.config_file = config_file
        self.config = self.load_config()
        
        # Setup logging
        log_file = self.log_dir / f"security_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize tracking files
        self.blocked_ips_file = self.log_dir / "blocked_ips.json"
        self.attempts_file = self.log_dir / "login_attempts.json"
        self.blocked_ips = self.load_blocked_ips()
        self.login_attempts = self.load_login_attempts()
        
        self.logger.info("Security Monitor initialized")
    
    def load_config(self):
        """Load configuration settings"""
        default_config = {
            "max_attempts": 3,
            "block_duration_minutes": 60,
            "monitor_auth_log": True,
            "auto_block": True,
            "alert_email": None
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def load_blocked_ips(self):
        """Load blocked IPs from file"""
        if self.blocked_ips_file.exists():
            try:
                with open(self.blocked_ips_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading blocked IPs: {e}")
        return {}
    
    def save_blocked_ips(self):
        """Save blocked IPs to file"""
        try:
            with open(self.blocked_ips_file, 'w') as f:
                json.dump(self.blocked_ips, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving blocked IPs: {e}")
    
    def load_login_attempts(self):
        """Load login attempts from file"""
        if self.attempts_file.exists():
            try:
                with open(self.attempts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading login attempts: {e}")
        return {}
    
    def save_login_attempts(self):
        """Save login attempts to file"""
        try:
            with open(self.attempts_file, 'w') as f:
                json.dump(self.login_attempts, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving login attempts: {e}")
    
    def get_current_connections(self):
        """Get current network connections"""
        try:
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, check=True)
            connections = []
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line or 'SYN_SENT' in line:
                    connections.append(line)
            return connections
        except Exception as e:
            self.logger.error(f"Error getting connections: {e}")
            return []
    
    def extract_ip_from_line(self, line):
        """Extract IP address from a log line or connection string"""
        # Pattern for IPv4 addresses
        ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        matches = re.findall(ipv4_pattern, line)
        
        # Filter out local/private IPs
        for ip in matches:
            if not ip.startswith(('127.', '10.', '192.168.', '172.')):
                return ip
        return matches[0] if matches else None
    
    def monitor_ssh_attempts(self):
        """Monitor SSH login attempts from system logs"""
        auth_logs = [
            '/var/log/auth.log',
            '/var/log/secure',
            '/var/log/system.log'  # macOS
        ]
        
        for log_file in auth_logs:
            if os.path.exists(log_file):
                try:
                    # On macOS, we need sudo to read system logs
                    # For demo purposes, we'll track simulated attempts
                    self.logger.info(f"Monitoring {log_file}")
                except Exception as e:
                    self.logger.error(f"Error reading {log_file}: {e}")
    
    def log_attempt(self, ip_address, username="unknown", status="failed"):
        """Log an access attempt"""
        timestamp = datetime.now().isoformat()
        
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = []
        
        attempt_record = {
            "timestamp": timestamp,
            "username": username,
            "status": status,
            "attempt_number": len(self.login_attempts[ip_address]) + 1
        }
        
        self.login_attempts[ip_address].append(attempt_record)
        self.save_login_attempts()
        
        self.logger.warning(
            f"Access attempt from {ip_address} - User: {username} - "
            f"Status: {status} - Attempt #{attempt_record['attempt_number']}"
        )
        
        # Auto-block if threshold exceeded
        if (self.config['auto_block'] and 
            len(self.login_attempts[ip_address]) >= self.config['max_attempts']):
            self.block_ip(ip_address, reason="Too many failed attempts")
        
        return attempt_record
    
    def block_ip(self, ip_address, reason="Unauthorized access attempt"):
        """Block an IP address using pfctl (macOS firewall)"""
        if ip_address in self.blocked_ips:
            self.logger.info(f"IP {ip_address} is already blocked")
            return False
        
        timestamp = datetime.now().isoformat()
        
        # Add to blocked list
        self.blocked_ips[ip_address] = {
            "blocked_at": timestamp,
            "reason": reason,
            "attempts": len(self.login_attempts.get(ip_address, [])),
            "method": "pfctl"
        }
        
        self.save_blocked_ips()
        
        # Block using pfctl (macOS)
        try:
            # Create a PF rule file if it doesn't exist
            pf_rules_file = self.log_dir / "blocked_ips.pf"
            with open(pf_rules_file, 'a') as f:
                f.write(f"block drop from {ip_address} to any\n")
            
            self.logger.critical(
                f"🚫 BLOCKED IP: {ip_address} - Reason: {reason} - "
                f"Attempts: {self.blocked_ips[ip_address]['attempts']}"
            )
            
            # Note: Actual pfctl commands require sudo
            # You would run: sudo pfctl -f /path/to/blocked_ips.pf
            self.logger.info(
                f"To activate blocking, run: sudo pfctl -f {pf_rules_file}"
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error blocking IP {ip_address}: {e}")
            return False
    
    def unblock_ip(self, ip_address):
        """Unblock an IP address"""
        if ip_address not in self.blocked_ips:
            self.logger.info(f"IP {ip_address} is not blocked")
            return False
        
        # Remove from blocked list
        blocked_info = self.blocked_ips.pop(ip_address)
        self.save_blocked_ips()
        
        # Rebuild PF rules file without this IP
        pf_rules_file = self.log_dir / "blocked_ips.pf"
        if pf_rules_file.exists():
            with open(pf_rules_file, 'r') as f:
                rules = f.readlines()
            
            with open(pf_rules_file, 'w') as f:
                for rule in rules:
                    if ip_address not in rule:
                        f.write(rule)
        
        self.logger.info(
            f"✅ UNBLOCKED IP: {ip_address} - Was blocked at: {blocked_info['blocked_at']}"
        )
        
        return True
    
    def get_blocked_ips(self):
        """Get list of all blocked IPs"""
        return self.blocked_ips
    
    def get_statistics(self):
        """Get security statistics"""
        total_attempts = sum(len(attempts) for attempts in self.login_attempts.values())
        unique_ips = len(self.login_attempts)
        blocked_count = len(self.blocked_ips)
        
        stats = {
            "total_attempts": total_attempts,
            "unique_ips_attempted": unique_ips,
            "blocked_ips_count": blocked_count,
            "blocked_ips": list(self.blocked_ips.keys())
        }
        
        return stats
    
    def simulate_attack(self, ip_address, username="attacker", attempts=5):
        """Simulate an attack for testing purposes"""
        self.logger.info(f"🔴 Simulating attack from {ip_address}")
        
        for i in range(attempts):
            self.log_attempt(ip_address, username=username, status="failed")
        
        return self.get_statistics()

def main():
    """Main function for CLI usage"""
    monitor = SecurityMonitor()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python security_monitor.py log <ip> <username> - Log an attempt")
        print("  python security_monitor.py block <ip> - Block an IP")
        print("  python security_monitor.py unblock <ip> - Unblock an IP")
        print("  python security_monitor.py list - List blocked IPs")
        print("  python security_monitor.py stats - Show statistics")
        print("  python security_monitor.py simulate <ip> - Simulate attack")
        return
    
    command = sys.argv[1]
    
    if command == "log" and len(sys.argv) >= 3:
        ip = sys.argv[2]
        username = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        monitor.log_attempt(ip, username)
    
    elif command == "block" and len(sys.argv) >= 3:
        ip = sys.argv[2]
        monitor.block_ip(ip)
    
    elif command == "unblock" and len(sys.argv) >= 3:
        ip = sys.argv[2]
        monitor.unblock_ip(ip)
    
    elif command == "list":
        blocked = monitor.get_blocked_ips()
        print("\n🚫 Blocked IPs:")
        print(json.dumps(blocked, indent=2))
    
    elif command == "stats":
        stats = monitor.get_statistics()
        print("\n📊 Security Statistics:")
        print(json.dumps(stats, indent=2))
    
    elif command == "simulate" and len(sys.argv) >= 3:
        ip = sys.argv[2]
        stats = monitor.simulate_attack(ip)
        print("\n📊 Attack Simulation Complete:")
        print(json.dumps(stats, indent=2))
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    main()
