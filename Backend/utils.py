import re

def clean_address(address):
    """Normalize address for Zillow URLs."""
    clean = re.sub(r'[^\w\s-]', '', address)
    return re.sub(r'\s+', '-', clean.strip())

def extract_property_data(html):
    """
    Analyzes Zillow HTML to find property status and price.
    Returns a dict with data or an error message.
    """
    html_lower = html.lower()
    
    # 1. Validation: Check if the address exists on Zillow
    not_found_indicators = [
        "we couldn't find any matching results",
        "check the spelling",
        "invalid address",
        "no matching properties"
    ]
    if any(indicator in html_lower for indicator in not_found_indicators):
        return {"error": "Address not found on Zillow"}

    # 2. Detect Context (Rental vs Sale)
    is_rental = any(x in html_lower for x in ['"forrent"', 'rent zestimate', '/rentals/', 'monthly rent'])

    # 3. Extraction via Regex
    rent_zestimate = re.search(r'"rentZestimate":\s*(\d+)', html)
    sales_zestimate = re.search(r'"zestimate":\s*(\d+)', html)
    list_price = re.search(r'"price":\s*(\d+)', html)

    # 4. Decision Logic
    if is_rental and rent_zestimate:
        return {"price": rent_zestimate.group(1), "label": "Monthly Rent"}
    
    if list_price and list_price.group(1) != "0":
        return {"price": list_price.group(1), "label": "Listing Price"}
    
    if sales_zestimate:
        return {"price": sales_zestimate.group(1), "label": "Sales Zestimate"}
    
    return {"error": "Property found, but no price data is available"}