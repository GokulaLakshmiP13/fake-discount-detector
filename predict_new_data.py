import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

MODEL_PATH = 'discount_detector_model.joblib'
SCALER_PATH = 'feature_scaler.joblib'

try:
    loaded_model = joblib.load(MODEL_PATH)
    loaded_scaler = joblib.load(SCALER_PATH)
except FileNotFoundError:
    print("🚨 ERROR: Model or Scaler not found. Please run detector_script.py first!")
    exit()

def predict_discount_status(price_history_series, current_price):
    """
    Predicts the status of a new discount based on its recent history.
    
    Args:
        price_history_series (pd.Series): Last 90 days of price data for the product.
        current_price (float): The price being checked today.
    """
   
    baseline_price = price_history_series.mean()
    
    volatility_score = price_history_series.iloc[-30:].std()
    
    inflation_indicator = (baseline_price - price_history_series.iloc[-14:-1].mean()) / price_history_series.iloc[-14:-1].mean()
    
    effective_discount = (baseline_price - current_price) / baseline_price
    
    new_features = pd.DataFrame({
        'Effective_Discount': [effective_discount],
        'Volatility_Score': [volatility_score],
        'Inflation_Indicator': [inflation_indicator]
    })
   
    X_new_scaled = loaded_scaler.transform(new_features)
    
    status_code = loaded_model.predict(X_new_scaled)[0]
    
    status = 'Suspicious Discount' if status_code == -1 else 'Genuine Discount'
    
    print("\n--- NEW PRODUCT ANALYSIS ---")
    print(f"Current Price: ${current_price:.2f}")
    print(f"90-Day Baseline: ${baseline_price:.2f}")
    print(f"30-Day Volatility: {volatility_score:.2f}")
    print(f"Prediction: {status}")
    print("-" * 30)
history_genuine = pd.Series([150 + np.random.normal(0, 2) for _ in range(90)])
predict_discount_status(history_genuine, current_price=100)

history_fake_base = pd.Series([150 + np.random.normal(0, 2) for _ in range(70)])
history_fake_spike = pd.Series([200 + np.random.normal(0, 2) for _ in range(20)])
history_fake = pd.concat([history_fake_base, history_fake_spike])
predict_discount_status(history_fake, current_price=160)