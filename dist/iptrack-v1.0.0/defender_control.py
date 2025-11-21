#!/usr/bin/env python3
"""
Defender Control Panel
Central utility to manage the security system - unblock IPs, view logs, reverse actions
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from security_monitor import SecurityMonitor
from ip_locator import IPLocator

class DefenderControl:
    def __init__(self):
        self.monitor = SecurityMonitor()
        self.locator = IPLocator()
        
    def show_dashboard(self):
        """Show security dashboard with all stats"""
        stats = self.monitor.get_statistics()
        blocked_ips = self.monitor.get_blocked_ips()
        
        print("\n" + "="*70)
        print("🛡️  DEFENDER SECURITY DASHBOARD")
        print("="*70)
        print(f"\n📊 Statistics:")
        print(f"   Total Access Attempts: {stats['total_attempts']}")
        print(f"   Unique IPs Attempted: {stats['unique_ips_attempted']}")
        print(f"   Currently Blocked: {stats['blocked_ips_count']}")
        
        if blocked_ips:
            print(f"\n🚫 Blocked IPs:")
            for ip, info in blocked_ips.items():
                print(f"\n   IP: {ip}")
                print(f"   Blocked At: {info['blocked_at']}")
                print(f"   Reason: {info['reason']}")
                print(f"   Attempts: {info['attempts']}")
                
                # Get location
                try:
                    location = self.locator.get_location(ip)
                    if location:
                        loc_str = f"{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}"
                        print(f"   Location: {loc_str}")
                        if location.get('isp'):
                            print(f"   ISP: {location['isp']}")
                except Exception as e:
                    print(f"   Location: Unable to fetch ({e})")
        
        print("\n" + "="*70 + "\n")
    
    def unblock_ip(self, ip_address):
        """Unblock an IP address and clear its attempts"""
        print(f"\n🔓 Unblocking {ip_address}...")
        
        # Unblock the IP
        if self.monitor.unblock_ip(ip_address):
            # Clear attempts history
            if ip_address in self.monitor.login_attempts:
                old_attempts = len(self.monitor.login_attempts[ip_address])
                del self.monitor.login_attempts[ip_address]
                self.monitor.save_login_attempts()
                print(f"   ✅ Cleared {old_attempts} recorded attempts")
            
            print(f"   ✅ {ip_address} has been unblocked")
            return True
        else:
            print(f"   ⚠️  {ip_address} was not blocked")
            return False
    
    def unblock_all(self):
        """Unblock all currently blocked IPs"""
        blocked_ips = list(self.monitor.get_blocked_ips().keys())
        
        if not blocked_ips:
            print("\n   No IPs are currently blocked")
            return
        
        print(f"\n🔓 Unblocking {len(blocked_ips)} IPs...")
        
        for ip in blocked_ips:
            self.unblock_ip(ip)
        
        print("\n   ✅ All IPs have been unblocked")
    
    def view_logs(self, ip_address=None):
        """View access attempt logs"""
        if ip_address:
            if ip_address in self.monitor.login_attempts:
                attempts = self.monitor.login_attempts[ip_address]
                print(f"\n📋 Login Attempts from {ip_address}:")
                for i, attempt in enumerate(attempts, 1):
                    print(f"\n   Attempt #{i}:")
                    print(f"   Time: {attempt['timestamp']}")
                    print(f"   User: {attempt['username']}")
                    print(f"   Status: {attempt['status']}")
            else:
                print(f"\n   No recorded attempts from {ip_address}")
        else:
            print("\n📋 All Login Attempts:")
            for ip, attempts in self.monitor.login_attempts.items():
                print(f"\n   IP: {ip} ({len(attempts)} attempts)")
                for attempt in attempts[-3:]:  # Show last 3
                    print(f"      {attempt['timestamp']} - {attempt['username']} - {attempt['status']}")
    
    def track_ip_location(self, ip_address):
        """Track and display IP location"""
        print(f"\n🌍 Tracking location for {ip_address}...")
        
        report = self.locator.generate_location_report(ip_address)
        
        if report:
            print("\n" + report["summary"])
            if report.get("map_url"):
                print(f"\n🗺️  View on map: {report['map_url']}")
            
            print("\n📊 Detailed Information:")
            location = report["location"]
            print(f"   Country: {location.get('country', 'Unknown')} ({location.get('country_code', 'N/A')})")
            print(f"   Region: {location.get('region', 'Unknown')}")
            print(f"   City: {location.get('city', 'Unknown')}")
            print(f"   Coordinates: {location.get('latitude', 'N/A')}, {location.get('longitude', 'N/A')}")
            print(f"   Timezone: {location.get('timezone', 'Unknown')}")
            print(f"   ISP: {location.get('isp', 'Unknown')}")
            print(f"   Organization: {location.get('organization', 'Unknown')}")
        else:
            print("   ⚠️  Could not retrieve location information")
    
    def export_logs(self, output_file="security_export.json"):
        """Export all security data to a file"""
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "statistics": self.monitor.get_statistics(),
            "blocked_ips": self.monitor.get_blocked_ips(),
            "login_attempts": self.monitor.login_attempts,
            "ip_locations": self.locator.location_cache
        }
        
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n📦 Security data exported to: {output_path.absolute()}")
        return str(output_path.absolute())
    
    def reset_system(self):
        """Reset the security system (clear all blocks and logs)"""
        print("\n⚠️  WARNING: This will clear all blocks and logs!")
        response = input("Are you sure? (yes/no): ")
        
        if response.lower() == 'yes':
            # Clear all blocked IPs
            self.monitor.blocked_ips = {}
            self.monitor.save_blocked_ips()
            
            # Clear all login attempts
            self.monitor.login_attempts = {}
            self.monitor.save_login_attempts()
            
            # Clear location cache
            self.locator.location_cache = {}
            self.locator.save_cache()
            
            # Clear PF rules file
            pf_rules_file = self.monitor.log_dir / "blocked_ips.pf"
            if pf_rules_file.exists():
                pf_rules_file.unlink()
            
            print("   ✅ System has been reset")
        else:
            print("   ❌ Reset cancelled")
    
    def show_help(self):
        """Show help information"""
        print("\n" + "="*70)
        print("🛡️  DEFENDER CONTROL PANEL - HELP")
        print("="*70)
        print("\nAvailable Commands:")
        print("  dashboard          - Show security dashboard with stats")
        print("  unblock <ip>       - Unblock a specific IP address")
        print("  unblock-all        - Unblock all blocked IPs")
        print("  logs [ip]          - View access logs (all or for specific IP)")
        print("  locate <ip>        - Track location of an IP address")
        print("  export [file]      - Export all security data to JSON")
        print("  reset              - Reset system (clear all data)")
        print("  help               - Show this help message")
        print("\nExamples:")
        print("  python defender_control.py dashboard")
        print("  python defender_control.py unblock 192.168.1.100")
        print("  python defender_control.py locate 8.8.8.8")
        print("  python defender_control.py logs 192.168.1.100")
        print("="*70 + "\n")

def main():
    """Main CLI interface"""
    control = DefenderControl()
    
    if len(sys.argv) < 2:
        control.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "dashboard":
        control.show_dashboard()
    
    elif command == "unblock":
        if len(sys.argv) >= 3:
            ip = sys.argv[2]
            control.unblock_ip(ip)
        else:
            print("Error: Please specify an IP address to unblock")
    
    elif command == "unblock-all":
        control.unblock_all()
    
    elif command == "logs":
        ip = sys.argv[2] if len(sys.argv) >= 3 else None
        control.view_logs(ip)
    
    elif command == "locate":
        if len(sys.argv) >= 3:
            ip = sys.argv[2]
            control.track_ip_location(ip)
        else:
            print("Error: Please specify an IP address to locate")
    
    elif command == "export":
        output_file = sys.argv[2] if len(sys.argv) >= 3 else "security_export.json"
        control.export_logs(output_file)
    
    elif command == "reset":
        control.reset_system()
    
    elif command == "help":
        control.show_help()
    
    else:
        print(f"Unknown command: {command}")
        control.show_help()

if __name__ == "__main__":
    main()
