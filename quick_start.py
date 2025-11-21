#!/usr/bin/env python3
"""
Quick Start Script
Demonstrates the security system with a simulated attack
"""

from security_monitor import SecurityMonitor
from ip_locator import IPLocator
from defender_control import DefenderControl
import time

def demo():
    """Run a demonstration of the security system"""
    print("="*70)
    print("🛡️  DEFENDER SECURITY SYSTEM - DEMO")
    print("="*70)
    
    # Initialize
    print("\n1️⃣  Initializing security monitor...")
    monitor = SecurityMonitor()
    locator = IPLocator()
    control = DefenderControl()
    
    # Simulate attacks
    print("\n2️⃣  Simulating unauthorized access attempts...")
    test_ips = [
        ("45.142.120.10", "hacker1"),
        ("185.220.101.50", "attacker"),
        ("8.8.8.8", "test_user")
    ]
    
    for ip, username in test_ips:
        print(f"\n   🔴 Simulating attack from {ip} ({username})")
        monitor.log_attempt(ip, username, status="failed")
        monitor.log_attempt(ip, username, status="failed")
        monitor.log_attempt(ip, username, status="failed")
        time.sleep(0.5)
    
    # Show dashboard
    print("\n3️⃣  Security Dashboard:")
    control.show_dashboard()
    
    # Track locations
    print("\n4️⃣  Tracking attacker locations...")
    for ip, _ in test_ips[:2]:  # Track first 2
        try:
            print(f"\n   Locating {ip}...")
            location = locator.get_location(ip)
            if location:
                print(f"   📍 {location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}")
                if location.get('isp'):
                    print(f"   ISP: {location['isp']}")
        except Exception as e:
            print(f"   Error: {e}")
    
    # Show how to unblock
    print("\n5️⃣  Unblock Example:")
    print("   To unblock an IP, run:")
    print(f"   python defender_control.py unblock {test_ips[0][0]}")
    
    print("\n" + "="*70)
    print("✅ Demo complete! Check the 'logs' folder for detailed logs.")
    print("="*70 + "\n")

if __name__ == "__main__":
    demo()
