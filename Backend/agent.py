import requests
import json
import logging
import os
from datetime import datetime, timedelta
from utils import clean_address, extract_price

logger = logging.getLogger(__name__)

class ZillowAutonomousAgent:
    def __init__(self, api_key, memory_file="memory.json", ttl_hours=24):
        self.api_key = api_key
        self.memory_file = memory_file
        self.ttl_hours = ttl_hours
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def is_stale(self, timestamp):
        """Checks if the cached data is older than the allowed TTL."""
        cached_time = datetime.fromisoformat(timestamp)
        return datetime.now() > cached_time + timedelta(hours=self.ttl_hours)

    def run(self, address):
        slug = clean_address(address)
        
        # 1. Check Memory and Freshness
        if slug in self.memory:
            data = self.memory[slug]
            if not self.is_stale(data['timestamp']):
                logger.info(f"Fresh Memory Hit! Data is from {data['timestamp']}")
                return {"status": "success", "price": data['price'], "source": "cache"}
            else:
                logger.info(f"Stale Memory found for {slug}. Refreshing from Zillow...")

        # 2. Execute Fresh Extraction
        params = {
            "url": f"https://www.zillow.com/homes/{slug}_rb/",
            "apikey": self.api_key,
            "js_render": "true",
            "antibot": "true",
            "premium_proxy": "true"
        }

        try:
            response = requests.get("https://api.zenrows.com/v1/", params=params, timeout=45)
            if response.status_code == 200:
                price = extract_price(response.text)
                if price:
                    # 3. Update Memory with Current Timestamp
                    self.memory[slug] = {
                        "price": price,
                        "timestamp": datetime.now().isoformat()
                    }
                    self._save_memory()
                    return {"status": "success", "price": price, "source": "network"}
        except Exception as e:
            logger.error(f"Agent error: {e}")
            
        return {"status": "failed", "error": "Could not retrieve fresh data"}