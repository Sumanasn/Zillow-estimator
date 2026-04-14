import re

def clean_address(address):
    clean = re.sub(r'[^\w\s-]', '', address)
    return re.sub(r'\s+', '-', clean.strip())

def extract_price(html):
    match = re.search(r'"price":\s*(\d+)', html)
    return match.group(1) if match else None