# 🥖 Bakery Sales Forecasting  ( Republished ) 

## 📋 Project Overview

This project addresses a real-world inventory management challenge for a local bakery.
The goal is to predict daily revenue to adjust production levels, minimize food waste, and prevent stock shortages.

**Key Result:** The final model reduces forecasting uncertainty by **23%** compared to a naive baseline.

## 🚧 Limitations & Future Improvements

**Granularity Constraint:**
Ideally, this model would predict sales at the **product level** (e.g., number of baguettes vs. pastries) rather than global revenue. However, due to the **technical limitations of the bakery's current Point of Sale (POS) system**, extracting granular item-level data is currently not feasible. 

**Next Steps:**
* If the data infrastructure allows it in the future, shifting to item-level forecasting would significantly improve inventory management precision.

## 🛠️ Technical Architecture

### 1. Data Engineering (`CSV_Generator.py`)
* **Extraction:** Parsing PDF cash reports using `pdfplumber`.
* **Enrichment:** Integrating weather data via the `Meteostat` API.
* **Cleaning:** Outlier detection, handling closed days, and fixing data entry errors.

### 2. Exploratory Data Analysis (`Analyse.ipynb`)
* Seasonality analysis (ACF/PACF).
* Correlation study (Weather vs. Sales).
* Weekly and monthly trend visualization.

### 3. Modeling (`AI_model.ipynb`)
Comparison of multiple approaches using **Time Series Cross-Validation**:
* **Baseline:** Lag 5.
* **Machine Learning:** XGBoost (Selected) vs. Random Forest.

## 📊 Performance & Results

**Best model (XGBoost)** 

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **MAE** | **€264** | Mean Absolute Error per day |
| **MAPE** | **16%** | Mean Absolute Percentage Error |
| **Lift** | **+23%** | Improvement over the baseline |

### Feature Importance
The model analysis reveals that prediction relies structurally on:
1.  **Day of the Week (82%)**: Weekly seasonality is the dominant factor.
2.  **Recent History (13%)**: Lag-1 (Yesterday) and Lag-5(Lag-7).
3.  **Trend (5%)**: Weekly trend.

## 🚀 Installation & Usage

### Prerequisites
* Python 3.x
* Libraries listed in `requirements.txt`

### Installation
```bash
git clone [https://github.com/Shyzo/bakery-forecasting-project.git](https://github.com/Shyzo/bakery-forecasting-project.git)
cd bakery-forecasting-project
pip install -r requirements.txt
