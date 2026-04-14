import streamlit as st
import requests
import os

# Internal Docker URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="Zillow Agent", page_icon="🤖")
st.title("Zillow Estimate Agent")
st.markdown("---")

address = st.text_input("Enter Property Address", placeholder="e.g. 11319 NE 23rd St, Vancouver, WA 98684")

if st.button("Deploy Agent"):
    if not address:
        st.warning("Please enter an address first.")
    else:
        with st.spinner("Agent is navigating Zillow and analyzing data..."):
            try:
                res = requests.post(f"{BACKEND_URL}/agent/execute", json={"address": address}, timeout=70)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data["status"] == "success":
                        st.balloons()
                        price = int(data['price'])
                        label = data['label']
                        suffix = "/mo" if "Rent" in label else ""
                        
                        col1, col2 = st.columns(2)
                        col1.metric(label, f"${price:,}{suffix}")
                        col2.info(f"Source: {data['source'].upper()}")
                        st.success(f"Agent verified: This is a {label} property.")
                    
                    elif data["status"] == "error":
                        st.error(f"⚠️ {data['message']}")
                        st.info("Check the address spelling or try a more specific location.")
                
                else:
                    st.error(f"Technical Failure: {res.json().get('detail', 'Unknown Error')}")
            
            except Exception as e:
                st.error(f"Backend offline. Verify Docker containers are healthy.")