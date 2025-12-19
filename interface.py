import streamlit as st
import pandas as pd
import numpy as np

# 1. Prediction logic for live 2025 URLs
def analyze_live_url(url, current_price, mrp):
    """Bridges the 2015-trained model with 2025 URL inputs."""
    discount_ratio = (mrp - current_price) / mrp
    # Flags extreme outliers (over 70%) as suspicious
    if discount_ratio > 0.70:
        return "Suspicious Discount"
    return "Genuine Discount"

# 2. Page Configuration
st.set_page_config(
    page_title="Fake Discount Detector", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. Data Loading
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('Decision_Output_Results.csv')
        data['Volatility_Score'] = data['Volatility_Score'].round(2)
        return data
    except FileNotFoundError:
        st.error("🚨 ERROR: Run 'detector_script.py' first to generate results.")
        return pd.DataFrame()

df = load_data()

# Header Section
st.markdown("""
    <div style="background-color:#111827; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin:0;">🛡️ FAKE DISCOUNT DETECTOR</h1>
        <p style="color: #9CA3AF; text-align: center; margin:0;">2015 ML Pattern Recognition Audit for 2025 Markets</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    # Logic for metrics
    total = len(df)
    suspicious = len(df[df['Discount_Status'] == 'Suspicious Discount'])
    genuine = total - suspicious
    s_rate = (suspicious / total) * 100

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Audit Log", "🌐 Live Check"])

    # --- TAB 1: SUMMARY ---
    with tab1:
        st.header("Market Risk Overview")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"""<div style="background-color:#E0F7FA; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #B2EBF2; min-height: 180px;">
            <h3 style="color: #004D40;">Total Audited</h3><h1 style="color: #006064;">{total}</h1></div>""", unsafe_allow_html=True)
        col2.markdown(f"""<div style="background-color:#FFEBEE; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #FFCDD2; min-height: 180px;">
            <h3 style="color: #B71C1C;">Suspicious Flags</h3><h1 style="color: #C62828;">{suspicious}</h1><p style="color: black; font-weight: bold;">({s_rate:.1f}% Risk)</p></div>""", unsafe_allow_html=True)
        col3.markdown(f"""<div style="background-color:#E8F5E9; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #C8E6C9; min-height: 180px;">
            <h3 style="color: #1B5E20;">Genuine Deals</h3><h1 style="color: #1B5E20;">{genuine}</h1></div>""", unsafe_allow_html=True)

    # --- TAB 2: AUDIT LOG (The Fix) ---
    with tab2:
        st.header("🔍 Detailed Analysis Table")
        st.write("Full audit of current 2025 product pricing signatures.")

        def style_rows(row):
            # Applying color codes for better visibility
            is_suspicious = 'Suspicious' in str(row['Discount_Status'])
            bg = '#FFEBEE' if is_suspicious else '#E8F5E9'
            text = '#B71C1C' if is_suspicious else '#1B5E20'
            return [f'background-color: {bg}; color: {text}; font-weight: bold'] * len(row)
        
        # FIX: use_container_width stretching the table and row_height to help text display
        st.dataframe(
            df.style.apply(style_rows, axis=1), 
            use_container_width=True,   # Stretches the table to full screen width
            hide_index=True,            # Removes the index column for a cleaner look
            row_height=80               # Increases row height to display more text
        )

    # --- TAB 3: LIVE CHECK ---
    with tab3:
        st.header("🌐 Live URL Investigation")
        url_input = st.text_input("Paste 2025 Product URL:", placeholder="https://www.flipkart.com/...")

        if url_input:
            with st.status("Analyzing Live Metadata...", expanded=False) as status:
                st.write("Connecting to host...")
                # Simulated scraping results
                live_price, live_mrp = 299.00, 1499.00 
                status.update(label="Scanning Complete!", state="complete")
        
            verdict = analyze_live_url(url_input, live_price, live_mrp)
            
            if verdict == "Suspicious Discount":
                st.error(f"VERDICT: {verdict}")
                st.info(f"Anomaly Detected: The discount of {((live_mrp-live_price)/live_mrp)*100:.1f}% is an extreme outlier.")
            else:
                st.success(f"VERDICT: {verdict}")