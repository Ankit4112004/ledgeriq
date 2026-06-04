# Ledger·IQ: Vendor Invoice Intelligence

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikit-learn&logoColor=white)

An end-to-end machine learning system designed to support procurement and finance operations by intelligently analyzing vendor invoices. The system is tailored for an **India-specific** supply chain context, forecasting logistics costs in INR and flagging high-risk discrepancies for manual review.

## Project Overview

Processing vendor invoices manually is time-consuming and error-prone. This project automates two critical finance workflows:
1. **Freight Cost Forecasting (Regression):** Predicts the expected logistics and freight costs based on distance, weight, and delivery mode.
2. **Invoice Risk Review (Classification):** Surfaces invoices that exhibit abnormal cost gaps or operational mismatches compared to their purchase orders.

By catching discrepancies before payment and accurately forecasting landed costs, **Ledger·IQ** minimizes financial leakage and streamlines the auto-approval of routine invoices.

## Business Value

- **Reduce Financial Leakage:** Prevent overpayment by catching PO-to-invoice gaps early.
- **Improve Landed Cost Accuracy:** Budget freight expenses confidently with predictive regression models.
- **Scale Procurement Operations:** Auto-clear low-risk invoices and route only the exceptions to finance analysts, significantly reducing manual review fatigue.

## Data Architecture & Modeling

The models are trained on real-world Indian logistics data, ensuring the predictive logic matches regional freight patterns and INR pricing.

* **Freight Forecasting (`Delivery_Logistics_India.csv`):** Utilizes delivery modes, vehicle types, package weights, and regional factors to train a Random Forest Regressor.
* **Invoice Risk Classification (`DTDC_Courier_India.csv`):** Synthetically derives realistic invoice-to-PO mismatches from courier data to train a balanced Random Forest Classifier, optimized via GridSearchCV.

### Evaluation Metrics
- **Regression:** Optimized for minimal Mean Absolute Error (MAE) and R² Score.
- **Classification:** Tuned for a high F1-score to handle class imbalance (prioritizing precision in flagging).



