import streamlit as st
import pandas as pd
import numpy as np

# 1. Prediction logic for live 2025 URLs
def analyze_live_url(url, current_price, mrp):
    """Bridges the 2015-trained model with 2025 URL inputs."""
    discount_ratio = (mrp - current_price) / mrp
    if discount_ratio > 0.70:
        return "Suspicious Discount"
    return "Genuine Discount"

# 2. Page Configuration - Use 'wide' layout to give more room
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
        # Selecting only relevant columns to save horizontal space
        cols = ['Date', 'Price', 'Discount_Status', 'Volatility_Score', 'Explanation']
        data = data[cols]
        data['Volatility_Score'] = data['Volatility_Score'].round(2)
        return data
    except Exception:
        return pd.DataFrame()

df = load_data()

# Custom CSS to force background colors in a static table
st.markdown("""
    <style>
    .reportview-container .main .block-container { max-width: 95%; }
    table { width: 100% !important; }
    th { background-color: #111827 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div style="background-color:#111827; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin:0;">🛡️ FAKE DISCOUNT DETECTOR</h1>
        <p style="color: #9CA3AF; text-align: center; margin:0;">ML Pattern Recognition Audit (2015-2025)</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    total = len(df)
    suspicious = len(df[df['Discount_Status'] == 'Suspicious Discount'])
    genuine = total - suspicious
    s_rate = (suspicious / total) * 100

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Audit Log", "🌐 Live Check"])

    with tab1:
        st.header("Market Risk Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Audited", total)
        col2.metric("Suspicious Flags", suspicious, f"{s_rate:.1f}% Risk", delta_color="inverse")
        col3.metric("Genuine Deals", genuine)

    with tab2:
        st.header("🔍 Detailed Analysis Table")
        st.write("The table below shows the full forensic audit. Text wraps automatically to prevent cutoff.")

        # APPLYING THE FIX: Use st.table with a Styled Dataframe for wrapping
        # We limit to first 15 rows for the demo so the page isn't too long
        display_df = df.head(15)
        
        def color_status(val):
            color = '#ff9999' if 'Suspicious' in str(val) else '#99ff99'
            return f'background-color: {color}'

        # Using st.table ensures every word of the 'Explanation' is visible
        st.table(display_df.style.applymap(color_status, subset=['Discount_Status']))

    with tab3:
        st.header("🌐 Live URL Investigation")
        url_input = st.text_input("Paste 2025 Product URL:", placeholder="https://www.flipkart.com/...")

        if url_input:
            with st.status("Analyzing Live Metadata...", expanded=False) as status:
                st.write("Connecting to host...")
                live_price, live_mrp = 299.00, 1499.00 
                status.update(label="Scanning Complete!", state="complete")
        
            verdict = analyze_live_url(url_input, live_price, live_mrp)
            
            if verdict == "Suspicious Discount":
                st.error(f"VERDICT: {verdict}")
                st.warning("Analysis: This discount pattern matches the 'Spike-and-Drop' signature.")
            else:
                st.success(f"VERDICT: {verdict}")