# 🛡️ Fake Discount Detector: ML Price Audit System
### Category: Machine Learning / Time-Series Anomaly Detection

## 📖 Project Objective
The objective of this system is to detect misleading discounts by analyzing historical pricing patterns, fulfilling the requirement for a focus on **Pattern Recognition**. By identifying the "Spike-and-Drop" signature, the system protects consumers from predatory pricing.

## 📊 Data & Preprocessing
* **Source**: `flipkart_com-ecommerce_sample.csv` (Kaggle Dataset).
* **Synthetic Time-Series Generation**: Since raw data lacked daily history, we simulated 180 days of realistic price history for 500 unique products using 'RetailPrice' and 'DiscountedPrice' as anchors.

## 🔍 Detection Logic & Pattern Recognition
The system determines the discount status based on three engineered features:

| Pattern (Feature) | Metric & Calculation | Purpose in Detection |
| :--- | :--- | :--- |
| **Baseline Price** | 90-Day Rolling Mean Price | Establishes the stable, 'normal' price for comparison. |
| **Price Volatility** | 30-Day Rolling Standard Deviation | Measures natural fluctuations; high volatility makes discounts less suspicious. |
| **Pre-Sale Inflation** | 14-Day Baseline Price % Change | Detects if the price was artificially raised immediately before a sale. |



## 🧠 Machine Learning Model
* **Model**: **Isolation Forest** (Scikit-Learn).
* **Method**: **Unsupervised Anomaly Detection**.
* **Decision Logic**: The model is trained on `Effective_Discount`, `Volatility_Score`, and `Inflation_Indicator`. Any price point that deviates significantly from the 'normal' pattern (Anomaly Score near -1) is classified as a **Suspicious Discount**.



## 🌐 Live URL Bridge (2025 Audit)
The system includes a **Live Check** tab that allows for real-time investigation of 2025 product links. 
* **Input**: User-provided 2025 Product URL.
* **Process**: The system extracts price metadata and runs a heuristic snapshot analysis against the fraud signatures learned from the historical dataset.
* **Output**: Instant verdict (Genuine vs. Suspicious) based on real-time price patterns.



## ✅ Required Outputs
For every audited product, the system generates:
1. **Discount Status**: Final verdict of Genuine or Suspicious.
2. **Volatility Score**: The 30-day standard deviation reflecting price stability.
3. **Plain-Language Explanation**: A text summary detailing *why* the discount was flagged (e.g., citing pre-sale inflation) or verified as genuine.

## 🚀 Installation & Deployment
1. **Live App**: Hosted on Streamlit Community Cloud.
2. **Local Run**: 
   ```bash
   pip install -r requirements.txt
   streamlit run interface.py
