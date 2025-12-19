# Project: Fake Discount Detector

**Category:** Machine Learning / Time-Series Anomaly Detection

**Objective:** To detect misleading discounts by analyzing historical pricing patterns, fulfilling the requirement of pattern recognition focus.

---

## 1. Data Input

* **Source:** `flipkart_com-ecommerce_sample.csv` (Kaggle Dataset).
* **Preprocessing:** Since the raw data lacked daily history, we simulated 180 days of realistic price history for 500 unique products using their 'RetailPrice' and 'DiscountedPrice' as anchors.

## 2. Detection Logic & Pattern Recognition

The system determines the discount status based on three engineered features, which serve as the recognized price patterns:

| Pattern (Feature) | Metric & Calculation | Purpose in Detection |
| :--- | :--- | :--- |
| **Baseline Price** | 90-Day Rolling Mean Price | Establishes the stable, 'normal' price for comparison. |
| **Price Volatility** (Output) | 30-Day Rolling Standard Deviation | Measures how much the price naturally fluctuates. High volatility makes a deep discount less suspicious. |
| **Pre-Sale Inflation** | 14-Day Baseline Price Percentage Change | Detects if the price was artificially raised immediately before the sale was applied. |

## 3. Machine Learning Model

* **Model:** **Isolation Forest** (from `scikit-learn`). 
* **Method:** Unsupervised Anomaly Detection.
* **Decision:** The model was trained on the combination of the `Effective_Discount`, `Volatility_Score`, and `Inflation_Indicator`. Any price point that deviates significantly from the 'normal' historical pattern (receiving an anomaly score of -1) is classified as **Suspicious Discount**.

## 4. Required Outputs

The system generates the following outputs for the most recent date of each product:

1.  **Discount Status:** Genuine Discount or Suspicious Discount.
2.  **Volatility Score:** The 30-day standard deviation of the price.
3.  **Plain-Language Explanation:** A text summary detailing *why* the discount was flagged (e.g., citing pre-sale inflation) or why it was considered genuine.