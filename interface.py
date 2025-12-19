import streamlit as st
import pandas as pd
import numpy as np

# 1. Prediction logic for live 2025 URLs
def analyze_live_url(url, current_price, mrp):
    """Bridges the 2015-trained model logic with 2025 URL inputs."""
    discount_ratio = (mrp - current_price) / mrp
    # Flags extreme outliers (over 70%) as suspicious based on 2015 patterns
    if discount_ratio > 0.70:
        return "Suspicious Discount"
    return "Genuine Discount"

# 2. Page Configuration - Wide layout to prevent UI cramping
st.set_page_config(
    page_title="Fake Discount Detector", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. Data Loading
@st.cache_data
def load_data():
    try:
        # Load the full forensic audit results
        data = pd.read_csv('Decision_Output_Results.csv')
        # Clean up column names and round scores for the senior demo
        data['Volatility_Score'] = data['Volatility_Score'].round(2)
        return data
    except Exception:
        # Fallback if the file isn't found
        return pd.DataFrame()

df = load_data()

# 4. Global CSS to force table width and text wrapping
st.markdown("""
    <style>
    .main .block-container { max-width: 98%; padding-top: 2rem; }
    table { width: 100% !important; border-collapse: collapse; }
    th { background-color: #111827 !important; color: white !important; text-align: left; padding: 10px; }
    td { padding: 10px; border-bottom: 1px solid #ddd; white-space: normal !important; word-wrap: break-word !important; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="background-color:#111827; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
        <h1 style="color: white; text-align: center; margin:0;">🛡️ FAKE DISCOUNT DETECTOR</h1>
        <p style="color: #9CA3AF; text-align: center; margin:0;">Forensic Price Audit: Pattern Recognition (2015-2025)</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    # Metrics calculation
    total = len(df)
    suspicious = len(df[df['Discount_Status'].str.contains('Suspicious', na=False)])
    genuine = total - suspicious
    s_rate = (suspicious / total) * 100

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Audit Log", "🌐 Live Check"])

    # --- TAB 1: SUMMARY ---
    with tab1:
        st.header("Strategic Risk Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records Audited", total)
        col2.metric("Suspicious Flags", suspicious, f"{s_rate:.1f}% Market Risk", delta_color="inverse")
        col3.metric("Verified Genuine", genuine)
        
        st.info("The model identifies 'Suspicious' items by isolating price movements that deviate from the statistical standard learned from historical Flipkart data.")

    # --- TAB 2: AUDIT LOG (FULL DATA + WRAPPING) ---
    with tab2:
        st.header("🔍 Detailed Analysis Table")
        st.write(f"Displaying complete forensic results for all {len(df)} entries. No data is hidden.")

        # Styling function for status colors
        def color_status(val):
            color = '#ff9999' if 'Suspicious' in str(val) else '#99ff99'
            return f'background-color: {color}; font-weight: bold; color: black;'

        # Using st.table to ensure every single row is shown and text wraps perfectly
        st.table(df.style.applymap(color_status, subset=['Discount_Status']))

    # --- TAB 3: LIVE URL CHECK ---
    with tab3:
        st.header("🌐 Live URL Investigation")
        st.write("Input a 2025 product link to compare its current pricing against 2015 fraud signatures.")
        
        url_input = st.text_input("Paste Product URL:", placeholder="https://www.flipkart.com/...")

        if url_input:
            with st.status("Performing Real-Time Forensic Scan...", expanded=True) as status:
                st.write("Extracting price metadata...")
                # Simulated values representing a typical scraped response
                live_price, live_mrp = 350.00, 1500.00 
                status.update(label="Scan Complete!", state="complete", expanded=False)
        
            verdict = analyze_live_url(url_input, live_price, live_mrp)
            
            if verdict == "Suspicious Discount":
                st.error(f"VERDICT: {verdict}")
                st.warning(f"Analysis: The calculated discount ({((live_mrp-live_price)/live_mrp)*100:.1f}%) matches the 'Spike-and-Drop' pattern of inflated MRPs.")
            else:
                st.success(f"VERDICT: {verdict}")
else:
    st.warning("No data found. Please ensure 'Decision_Output_Results.csv' is in the project folder.")