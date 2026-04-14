import streamlit as st
import requests
import os

# This is the CRITICAL line for Docker
# It defaults to 'backend' (the docker service name) but falls back to localhost for manual runs
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("Zillow Estimate Agent")
address = st.text_input("Property Address", "11319 NE 23rd St, Vancouver, WA 98684")

if st.button("Deploy Agent"):
    try:
        # Note the endpoint path matches your FastAPI route
        res = requests.post(f"{BACKEND_URL}/agent/execute", json={"address": address})
        
        if res.status_code == 200:
            data = res.json()
            price = int(data['price'])
            label = data['label']
                
            # Format based on rental vs sale
            suffix = "/mo" if "Rent" in label else ""
                
            st.balloons()
            col1, col2 = st.columns(2)
            col1.metric(label, f"${price:,}{suffix}")
            col2.info(f"Data Source: {data['source'].upper()}")
            st.success(f"Agent successfully identified this as a {label} property.")
        else:
            st.error("Agent failed to bypass Zillow's security.")
    except:
        st.error("Backend offline. Attempted: " + BACKEND_URL)