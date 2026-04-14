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
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError: return {}
        return {}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def is_stale(self, timestamp):
        return datetime.now() > datetime.fromisoformat(timestamp) + timedelta(hours=self.ttl_hours)

    def run(self, address):
        slug = clean_address(address)
        
        # 1. Check Memory
        if slug in self.memory:
            data = self.memory[slug]
            if not self.is_stale(data.get('timestamp', '2000-01-01')):
                logger.info(f"Memory Hit: {slug}")
                return {"status": "success", **data, "source": "cache"}

        # 2. Deploy Network Resource
        logger.info(f"Memory Miss: Fetching live data for {address}")
        params = {
            "url": f"https://www.zillow.com/homes/{slug}_rb/",
            "apikey": self.api_key,
            "js_render": "true",
            "antibot": "true",
            "premium_proxy": "true"
        }
        
        try:
            response = requests.get("https://api.zenrows.com/v1/", params=params, timeout=60)
            if response.status_code == 200:
                extracted = extract_property_data(response.text)
                
                # Check for "Not Found" or "No Data" errors
                if "error" in extracted:
                    return {"status": "error", "message": extracted["error"]}
                
                # Success: Save to memory
                result = {**extracted, "timestamp": datetime.now().isoformat()}
                self.memory[slug] = result
                self._save_memory()
                return {"status": "success", **result, "source": "network"}
                
            return {"status": "failed", "message": f"ZenRows Error: {response.status_code}"}
        except Exception as e:
            logger.error(f"Agent Crash: {e}")
            return {"status": "failed", "message": str(e)}