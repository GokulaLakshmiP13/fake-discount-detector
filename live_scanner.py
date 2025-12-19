import pandas as pd
import numpy as np
import joblib

def analyze_live_url(url, current_price, mrp):
    # 1. Load your trained brain
    # (Ensure you saved these from your detector_script.py)
    model = joblib.load('discount_detector_model.joblib')
    scaler = joblib.load('feature_scaler.joblib')

    # 2. Calculate Features today (2025)
    # We compare the current price to the MRP (which acts as the baseline)
    effective_discount = (mrp - current_price) / mrp
    
    # We simulate a 'Spike' for the demo if it's a suspicious link
    # In a real app, this comes from a Price History API
    inflation_val = 0.45 if "sale" in url.lower() else 0.02
    volatility_val = 15.5
    
    # 3. Predict
    new_data = pd.DataFrame([[effective_discount, volatility_val, inflation_val]], 
                            columns=['Effective_Discount', 'Volatility_Score', 'Inflation_Indicator'])
    
    prediction = model.predict(scaler.transform(new_data))[0]
    return "Suspicious Discount" if prediction == -1 else "Genuine Discount"