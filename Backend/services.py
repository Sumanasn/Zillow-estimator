import requests
import logging
from utils import clean_address, extract_price

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ZillowService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.zenrows.com/v1/"

    def fetch_zestimate(self, address):
        slug = clean_address(address)
        logger.info(f"Targeting address: {address} (Slug: {slug})")
        
        params = {
            "url": f"https://www.zillow.com/homes/{slug}_rb/",
            "apikey": self.api_key,
            "js_render": "true",
            "antibot": "true",
            "premium_proxy": "true"
        }

        try:
            response = requests.get(self.url, params=params, timeout=60)
            if response.status_code == 200:
                price = extract_price(response.text)
                if price:
                    logger.info(f"Successfully retrieved price: ${price}")
                    return price
            logger.error(f"Failed with status {response.status_code}")
        except Exception as e:
            logger.exception("Scraper encountered an error")
        return None