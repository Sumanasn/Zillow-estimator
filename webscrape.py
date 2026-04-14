import sys
import time
import json
import re
import os
import argparse
import random
import platform
import subprocess

# --- Universal Python 3.12+ Compatibility Shim ---
try:
    import distutils
except ImportError:
    try:
        import setuptools
        import types
        distutils = types.ModuleType("distutils")
        sys.modules["distutils"] = distutils
        from setuptools.extern.packaging.version import LegacyVersion as LooseVersion
        distutils.version = types.ModuleType("distutils.version")
        distutils.version.LooseVersion = LooseVersion
    except ImportError:
        pass 

import undetected_chromedriver as uc

class UniversalZillowAgent:
    def __init__(self):
        self.os_type = platform.system()
        # Use absolute pathing for cross-OS stability
        self.profile_dir = os.path.abspath(os.path.join(os.getcwd(), "zillow_session"))
        
    def cleanup_processes(self):
        """Force-kills zombie chrome/driver processes to release file locks."""
        try:
            if self.os_type == "Windows":
                subprocess.run(["taskkill", "/f", "/im", "chrome.exe", "/t"], capture_output=True)
                subprocess.run(["taskkill", "/f", "/im", "chromedriver.exe", "/t"], capture_output=True)
            else:
                subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
                subprocess.run(["pkill", "-f", "chromedriver"], capture_output=True)
        except Exception:
            pass

    def clean_address(self, address):
        """Slugifies address for Zillow's redirect router."""
        clean = re.sub(r'[^\w\s-]', '', address)
        return re.sub(r'\s+', '-', clean.strip())

    def extract_price(self, source):
        """Extracts numerical price from the hydrated data layer."""
        # Pattern matched from your verified diagnostic dump
        match = re.search(r'"price":\s*(\d+)', source)
        if match: return match.group(1)
        match = re.search(r'"zestimate":\s*(\d+)', source)
        if match: return match.group(1)
        return None

    def get_chrome_version(self):
        """Detects Chrome version to prevent 'SessionNotCreated' errors on Windows."""
        if self.os_type == "Windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                return int(version.split('.')[0])
            except:
                return 146 # Fallback to your current version
        return None

    def run(self, address):
        slug = self.clean_address(address)
        target_url = f"https://www.zillow.com/homes/{slug}_rb/"
        
        # Ensure a clean start by removing old locks
        self.cleanup_processes()

        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)

        options = uc.ChromeOptions()
        options.add_argument(f'--user-data-dir={self.profile_dir}')
        
        # Linux specific path for Fedora
        if self.os_type == "Linux" and os.path.exists('/usr/bin/google-chrome-stable'):
            options.binary_location = '/usr/bin/google-chrome-stable'
        
        print(f"🚀 Launching Agent on {self.os_type}...")
        v_main = self.get_chrome_version()
        driver = uc.Chrome(options=options, version_main=v_main)
        
        try:
            # Random jitter to simulate human latency
            time.sleep(random.uniform(2, 4))
            driver.get(target_url)
            
            print("\n--- AGENT MONITORING ---")
            print("Action: Solve any 'Press and Hold' challenges manually.")
            
            price = None
            for i in range(30):
                price = self.extract_price(driver.page_source)
                if price:
                    print(f"\n✅ SUCCESS! Price Captured: ${price}")
                    break
                
                if i % 5 == 0:
                    print(f"   [Wait {i}s] Polling internal data layer...")
                time.sleep(1)
            return price

        finally:
            print("Cleaning up browser session and closing window...")
            try:
                driver.quit()
            except:
                pass
            # Final hard-kill to ensure the terminal is freed immediately
            self.cleanup_processes()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Zillow Extraction Agent")
    parser.add_argument("address", help="Full property address")
    args = parser.parse_args()

    agent = UniversalZillowAgent()
    result = agent.run(args.address)
    
    output = {
        "address": args.address,
        "zestimate": result,
        "status": "COMPLETED" if result else "FAILED"
    }
    
    print("\n" + "="*40)
    print(json.dumps(output, indent=2))
    print("="*40)

