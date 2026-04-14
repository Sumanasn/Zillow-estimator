import requests
import json
import logging
import os
from datetime import datetime, timedelta
from utils import clean_address, extract_property_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | AGENT: %(message)s')
logger = logging.getLogger(__name__)

class ZillowAutonomousAgent:
    def __init__(self, api_key, memory_file="memory.json", ttl_hours=24):
        self.api_key = api_key
        self.memory_file = memory_file
        self.ttl_hours = ttl_hours
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file) and os.path.getsize(self.memory_file) > 0:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def is_stale(self, timestamp):
        return datetime.now() > datetime.fromisoformat(timestamp) + timedelta(hours=self.ttl_hours)

    def run(self, address):
        slug = clean_address(address)
        
        # Check Memory
        if slug in self.memory:
            data = self.memory[slug]
            if not self.is_stale(data['timestamp']):
                logger.info(f"Memory Hit: {slug}")
                return {"status": "success", **data, "source": "cache"}

        # Fetch New Data
        logger.info(f"Memory Miss: Deploying Agent for {address}")
        params = {"url": f"https://www.zillow.com/homes/{slug}_rb/", "apikey": self.api_key, "js_render": "true", "antibot": "true", "premium_proxy": "true"}
        
        try:
            response = requests.get("https://api.zenrows.com/v1/", params=params, timeout=60)
            if response.status_code == 200:
                extracted = extract_property_data(response.text)
                if extracted:
                    result = {**extracted, "timestamp": datetime.now().isoformat()}
                    self.memory[slug] = result
                    self._save_memory()
                    return {"status": "success", **result, "source": "network"}
        except Exception as e:
            logger.error(f"Agent Task Failed: {e}")
        
        return {"status": "failed", "error": "Property data unavailable or blocked."}