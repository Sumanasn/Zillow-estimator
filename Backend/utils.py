import re

def clean_address(address):
    clean = re.sub(r'[^\w\s-]', '', address)
    return re.sub(r'\s+', '-', clean.strip())

def extract_property_data(html):
    """Detects if a property is for Rent or Sale and picks the right price."""
    # 1. Detect Status Keywords
    html_lower = html.lower()
    is_rental = any(x in html_lower for x in ['"forrent"', 'rent zestimate', '/rentals/', 'monthly rent'])

    # 2. Extract specific data fields
    rent_zestimate = re.search(r'"rentZestimate":\s*(\d+)', html)
    sales_zestimate = re.search(r'"zestimate":\s*(\d+)', html)
    list_price = re.search(r'"price":\s*(\d+)', html)

    # 3. Decision Tree
    if is_rental and rent_zestimate:
        return {"price": rent_zestimate.group(1), "label": "Monthly Rent"}
    if list_price:
        return {"price": list_price.group(1), "label": "Listing Price"}
    if sales_zestimate:
        return {"price": sales_zestimate.group(1), "label": "Sales Zestimate"}
    
    return None