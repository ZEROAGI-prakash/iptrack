#!/usr/bin/env python3
"""
IP Geolocation Tracker
Tracks the physical location of IP addresses attempting to access the system
"""

import json
import requests
import logging
from datetime import datetime
from pathlib import Path

class IPLocator:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.cache_file = self.log_dir / "ip_locations.json"
        self.location_cache = self.load_cache()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Free IP geolocation APIs (no key required)
        self.apis = [
            {
                "name": "ip-api.com",
                "url": "http://ip-api.com/json/{ip}",
                "fields": ["query", "country", "countryCode", "region", "regionName", 
                          "city", "zip", "lat", "lon", "timezone", "isp", "org", "as"]
            },
            {
                "name": "ipapi.co",
                "url": "https://ipapi.co/{ip}/json/",
                "fields": ["ip", "city", "region", "country", "country_name", 
                          "latitude", "longitude", "timezone", "org"]
            },
            {
                "name": "ipwhois.app",
                "url": "http://ipwhois.app/json/{ip}",
                "fields": ["ip", "country", "country_code", "city", "region", 
                          "latitude", "longitude", "timezone", "isp", "org"]
            }
        ]
    
    def load_cache(self):
        """Load cached IP locations"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
        return {}
    
    def save_cache(self):
        """Save IP locations to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.location_cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving cache: {e}")
    
    def get_location(self, ip_address, force_refresh=False):
        """Get location information for an IP address"""
        # Check cache first
        if not force_refresh and ip_address in self.location_cache:
            self.logger.info(f"Using cached location for {ip_address}")
            return self.location_cache[ip_address]
        
        # Try each API until one succeeds
        for api in self.apis:
            try:
                url = api["url"].format(ip=ip_address)
                self.logger.info(f"Querying {api['name']} for {ip_address}")
                
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Normalize the response
                    location = self.normalize_location_data(data, api['name'])
                    location['queried_at'] = datetime.now().isoformat()
                    location['source'] = api['name']
                    
                    # Cache the result
                    self.location_cache[ip_address] = location
                    self.save_cache()
                    
                    return location
                    
            except Exception as e:
                self.logger.warning(f"Error with {api['name']}: {e}")
                continue
        
        # If all APIs fail
        self.logger.error(f"Could not get location for {ip_address}")
        return None
    
    def normalize_location_data(self, data, source):
        """Normalize location data from different APIs"""
        normalized = {
            "ip": None,
            "country": None,
            "country_code": None,
            "region": None,
            "city": None,
            "latitude": None,
            "longitude": None,
            "timezone": None,
            "isp": None,
            "organization": None
        }
        
        if source == "ip-api.com":
            normalized.update({
                "ip": data.get("query"),
                "country": data.get("country"),
                "country_code": data.get("countryCode"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone"),
                "isp": data.get("isp"),
                "organization": data.get("org")
            })
        
        elif source == "ipapi.co":
            normalized.update({
                "ip": data.get("ip"),
                "country": data.get("country_name"),
                "country_code": data.get("country"),
                "region": data.get("region"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone"),
                "isp": data.get("org"),
                "organization": data.get("org")
            })
        
        elif source == "ipwhois.app":
            normalized.update({
                "ip": data.get("ip"),
                "country": data.get("country"),
                "country_code": data.get("country_code"),
                "region": data.get("region"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone"),
                "isp": data.get("isp"),
                "organization": data.get("org")
            })
        
        return normalized
    
    def get_location_summary(self, ip_address):
        """Get a human-readable location summary"""
        location = self.get_location(ip_address)
        
        if not location:
            return f"Location unknown for {ip_address}"
        
        parts = []
        if location.get("city"):
            parts.append(location["city"])
        if location.get("region"):
            parts.append(location["region"])
        if location.get("country"):
            parts.append(location["country"])
        
        location_str = ", ".join(parts) if parts else "Unknown"
        
        coords = ""
        if location.get("latitude") and location.get("longitude"):
            coords = f" ({location['latitude']}, {location['longitude']})"
        
        isp_info = ""
        if location.get("isp"):
            isp_info = f"\nISP: {location['isp']}"
        
        return (
            f"📍 Location for {ip_address}:\n"
            f"   {location_str}{coords}\n"
            f"   Timezone: {location.get('timezone', 'Unknown')}"
            f"{isp_info}"
        )
    
    def track_multiple_ips(self, ip_list):
        """Track locations for multiple IPs"""
        results = {}
        
        for ip in ip_list:
            self.logger.info(f"Tracking {ip}...")
            location = self.get_location(ip)
            if location:
                results[ip] = location
        
        return results
    
    def get_map_url(self, ip_address):
        """Get a Google Maps URL for the IP location"""
        location = self.get_location(ip_address)
        
        if location and location.get("latitude") and location.get("longitude"):
            lat = location["latitude"]
            lon = location["longitude"]
            return f"https://www.google.com/maps?q={lat},{lon}"
        
        return None
    
    def generate_location_report(self, ip_address):
        """Generate a detailed location report"""
        location = self.get_location(ip_address)
        
        if not location:
            return None
        
        report = {
            "ip_address": ip_address,
            "location": location,
            "summary": self.get_location_summary(ip_address),
            "map_url": self.get_map_url(ip_address),
            "generated_at": datetime.now().isoformat()
        }
        
        return report

def main():
    """CLI interface for IP location tracking"""
    import sys
    
    locator = IPLocator()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ip_locator.py <ip_address> - Get location for IP")
        print("  python ip_locator.py report <ip_address> - Full report")
        print("  python ip_locator.py cache - Show cached locations")
        return
    
    if sys.argv[1] == "cache":
        print("\n📋 Cached IP Locations:")
        print(json.dumps(locator.location_cache, indent=2))
        return
    
    if sys.argv[1] == "report" and len(sys.argv) >= 3:
        ip = sys.argv[2]
        report = locator.generate_location_report(ip)
        if report:
            print("\n" + "="*60)
            print(report["summary"])
            print(f"\n🗺️  Map: {report['map_url']}")
            print("\n📊 Full Details:")
            print(json.dumps(report["location"], indent=2))
            print("="*60)
        else:
            print(f"Could not generate report for {ip}")
        return
    
    # Default: simple location lookup
    ip = sys.argv[1]
    print(locator.get_location_summary(ip))

if __name__ == "__main__":
    main()
