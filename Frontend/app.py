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
            st.metric("Price", f"${int(data['price']):,}")
            st.info(f"Source: {data['source']}")
        else:
            st.error(f"Agent Error: {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Backend offline. Attempted to connect to: {BACKEND_URL}")