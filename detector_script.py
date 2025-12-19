import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
try:
    df = pd.read_csv('flipkart_com-ecommerce_sample.csv') 
except FileNotFoundError:
    print("FATAL ERROR: CSV file not found. Place 'flipkart_com-ecommerce_sample.csv' in the same folder.")
    exit()
df = df.rename(columns={'uniq_id': 'ProductID', 
                        'retail_price': 'RetailPrice', 
                        'discounted_price': 'DiscountedPrice'})

df = df[['ProductID', 'RetailPrice', 'DiscountedPrice']].copy()
df = df[(df['RetailPrice'] > 0) & (df['DiscountedPrice'] > 0)].drop_duplicates(subset=['ProductID'])
df = df.reset_index(drop=True)
def create_historical_data(base_df):
    """Generates 180 days of price history for each unique product."""
    all_history = []
    dates = pd.to_datetime(pd.date_range(end='2025-12-17', periods=180))
    for index, row in base_df.iterrows():
        product_key = row['ProductID']
        retail_price = row['RetailPrice']
        discounted_price = row['DiscountedPrice']

        is_discounted = (retail_price > discounted_price)
        history_df = pd.DataFrame({'Date': dates, 'ProductID': product_key})
        history_df['Price'] = retail_price
        if is_discounted:
            if np.random.rand() > 0.4: 
                history_df.loc[150:, 'Price'] = discounted_price
            else: 
                spike_price = retail_price * np.random.uniform(1.2, 1.4)
                history_df.loc[130:149, 'Price'] = spike_price 
                history_df.loc[150:, 'Price'] = discounted_price
        history_df['Price'] = history_df['Price'] + np.random.normal(0, retail_price * 0.005, size=len(history_df))
        history_df['Price'] = history_df['Price'].round(2).clip(lower=1)
        
        all_history.append(history_df)
    return all_history
df_history = pd.concat(create_historical_data(df.head(500))) 
df_history = df_history.set_index('Date').sort_values(by=['ProductID', 'Date'])
def calculate_features(group):
    group['Baseline_Price'] = group['Price'].rolling(window=90, min_periods=10).mean().shift(1)
    group['Effective_Discount'] = (group['Baseline_Price'] - group['Price']) / group['Baseline_Price']
    group['Volatility_Score'] = group['Price'].rolling(window=30, min_periods=10).std().shift(1)
    group['Inflation_Indicator'] = group['Baseline_Price'].pct_change(periods=14)

    return group
df_features = df_history.groupby('ProductID').apply(calculate_features).dropna().reset_index(level=0, drop=True)
features = ['Effective_Discount', 'Volatility_Score', 'Inflation_Indicator']
X = df_features[features].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = IsolationForest(contamination=0.1, random_state=42)
df_features['Anomaly_Status'] = model.fit_predict(X_scaled) 
df_features['Anomaly_Score'] = model.decision_function(X_scaled) 
df_features['Discount_Status'] = df_features['Anomaly_Status'].apply(
    lambda x: 'Suspicious Discount' if x == -1 else 'Genuine Discount'
)
def generate_explanation(row):
    status = row['Discount_Status']
    effective_disc = row['Effective_Discount'] * 100
    inflation = row['Inflation_Indicator'] * 100
    
    if status == 'Suspicious Discount':
        if inflation > 0.05:
            return (f"SUSPICIOUS: Price was inflated by ~{inflation:.1f}% in the 14 days prior to sale, "
                    f"suggesting an artificial markdown. Effective discount (vs. 90-day avg) is {effective_disc:.1f}%.")
        else:
            return (f"SUSPICIOUS: Anomaly score ({row['Anomaly_Score']:.2f}) is low. The current price is an outlier compared to the product's history.")
    else:
        return (f"GENUINE: The price is {effective_disc:.1f}% lower than the 90-day average. "
                f"Price history shows low recent volatility and no pre-sale inflation spike.")

df_features['Explanation'] = df_features.apply(generate_explanation, axis=1)
final_output = df_features.reset_index()[['ProductID', 'Date', 'Price', 
                                          'Discount_Status', 'Volatility_Score', 'Explanation']]
final_decision_output = final_output.loc[final_output.groupby('ProductID')['Date'].idxmax()]
final_decision_output.to_csv('Decision_Output_Results.csv', index=False)

print("\n--- Project Execution Complete ---")
print("1. 'Decision_Output_Results.csv' (Decision Output Deliverable) has been generated.")
print("2. Now run 'streamlit run interface.py' to view the colorful dashboard!")
joblib.dump(model, 'discount_detector_model.joblib')
joblib.dump(scaler, 'feature_scaler.joblib')

print("\n3. 'discount_detector_model.joblib' and 'feature_scaler.joblib' saved for deployment.")