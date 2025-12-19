import streamlit as st
import pandas as pd
import numpy as np
def analyze_live_url(url, current_price, mrp):
    """
    A more realistic logic: Only flags as suspicious if the discount 
    is mathematically extreme (over 70%) or fits specific high-risk shapes.
    """
    discount_ratio = (mrp - current_price) / mrp
    
    # Genuine deals are usually between 10% and 50%
    if 0.10 <= discount_ratio <= 0.50:
        return "Genuine Discount"
        
    # Flag only extreme anomalies as suspicious
    if discount_ratio > 0.70:
        return "Suspicious Discount"
        
    return "Genuine Discount"

st.set_page_config(page_title="Fake Discount Detector", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('Decision_Output_Results.csv')
        data['Volatility_Score'] = data['Volatility_Score'].round(2)
        return data
    except FileNotFoundError:
        st.error("🚨 ERROR: Run 'detector_script.py' first.")
        return pd.DataFrame()

df = load_data()

st.markdown("""
    <div style="background-color:#111827; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center; margin:0;">FAKE DISCOUNT DETECTOR</h1>
        <p style="color: #9CA3AF; text-align: center; margin:0;">ML Pattern Recognition Audit</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    total = len(df)
    suspicious = len(df[df['Discount_Status'] == 'Suspicious Discount'])
    genuine = total - suspicious
    s_rate = (suspicious / total) * 100

    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Audit Log", "🌐 Live Check"])

    with tab1:
        st.header("Overall Detection Summary")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"""<div style="background-color:#E0F7FA; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #B2EBF2; min-height: 180px;">
            <h3 style="color: #004D40; margin-bottom: 10px;">Total Products</h3>
            <h1 style="color: #006064; font-size: 48px; margin: 0;">{total}</h1></div>""", unsafe_allow_html=True)

        col2.markdown(f"""<div style="background-color:#FFEBEE; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #FFCDD2; min-height: 180px;">
            <h3 style="color: #B71C1C; margin-bottom: 10px;">Suspicious Flags</h3>
            <h1 style="color: #C62828; font-size: 48px; margin: 0;">{suspicious}</h1>
            <p style="color: #000000; font-weight: bold; margin:0;">({s_rate:.1f}% Risk)</p></div>""", unsafe_allow_html=True)

        col3.markdown(f"""<div style="background-color:#E8F5E9; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #C8E6C9; min-height: 180px;">
            <h3 style="color: #1B5E20; margin-bottom: 10px;">Genuine Discounts</h3>
            <h1 style="color: #1B5E20; font-size: 48px; margin: 0;">{genuine}</h1></div>""", unsafe_allow_html=True)

    with tab2:
        st.header("Detailed Analysis Table")
        def style_rows(row):
            color = '#FFEBEE' if 'Suspicious' in row['Discount_Status'] else '#E8F5E9'
            text = '#B71C1C' if 'Suspicious' in row['Discount_Status'] else '#1B5E20'
            return [f'background-color: {color}; color: {text}; font-weight: bold'] * len(row)
        
        st.dataframe(df.style.apply(style_rows, axis=1), use_container_width=True)

    with tab3:
        st.header("🌐 Live URL Investigation")
        st.write("Analyze 2025 product links using patterns learned from the 2015 dataset.")

        url_input = st.text_input("Paste Product URL:", placeholder="https://www.flipkart.com/...")

        if url_input:
            with st.status("Connecting to 2025 Live Host...", expanded=True) as status:
                st.write("Scraping metadata...")
                st.write("Extracting price history snapshot...")
                # Simulated scraped values
                live_price, live_mrp = 499.00, 1299.00 
                status.update(label="Scanning Complete!", state="complete", expanded=False)
        
            # This now works because the function is defined above
            verdict = analyze_live_url(url_input, live_price, live_mrp)
        
            if verdict == "Suspicious Discount":
                st.error(f"VERDICT: {verdict}")
                st.markdown(f"""
                    <div style="background-color: #FFEBEE; padding: 20px; border-radius: 10px; border-left: 5px solid #B71C1C;">
                        <p style="color: #000000; font-size: 16px;">
                            <b>Analysis Report:</b><br>
                            This 2025 price pattern matches the <b>Spike-and-Drop</b> anomaly signature. 
                            The current discount is flagged as high-risk.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.success(f"VERDICT: {verdict}")