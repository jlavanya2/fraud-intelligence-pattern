# 🛡️ Fraud Intelligence Command Center

A practical, end-to-end fraud analytics system that models how real-world
fraud and risk teams monitor evolving patterns, assess transaction risk,
and make informed decisions using explainable signals.

🔗 **Live Demo**  
https://fraud-intelligence-patterngit-rdejt5xfhu8xh2zkmuaqpg.streamlit.app/

---

## 📌 Why This Project Exists

Most fraud projects stop at building a classifier.

In real industry settings, teams care more about:
- How risk is changing over time
- Which patterns are becoming dominant
- Why a transaction is risky
- Which users or strategies need attention first

This project was built to reflect that reality.

Instead of treating fraud detection as a single prediction task,
it models fraud as a **dynamic, evolving system** and presents it
through an analyst-friendly intelligence dashboard.

---

## 🧠 What the System Does

### 1. Risk Scoring
Each transaction is assigned a composite risk score using:
- Statistical deviation (amount anomalies)
- Behavioral changes (device switching, frequency)
- Temporal momentum (risk acceleration)
- Pattern-level risk (cluster behavior)

All scores are clipped and normalized for interpretability.

---

### 2. Explainable Risk
Every transaction includes a human-readable explanation such as:
- Escalating risk pattern
- Unusual transaction amount
- Frequent device changes
- High-risk behavioral cluster

This ensures decisions are transparent and auditable.

---

### 3. Pattern & Trend Intelligence
The system continuously tracks:
- Risk trends over time
- Risk distribution shifts
- Risk acceleration
- Fraud share evolution
- Dominant fraud patterns (clusters)

These insights help identify *emerging threats*, not just known ones.

---

### 4. Analyst Dashboard
An interactive Streamlit dashboard allows users to:
- Filter by time window, users, clusters, and thresholds
- Monitor KPIs and alerts
- Explore risk evolution visually
- Investigate high-risk users and transactions
- Understand *why* risk is increasing

All charts update live based on user inputs.

---

## 📊 Key Dashboard Features

- Live risk KPIs (mean, median, volatility, percentiles)
- Risk trend with evolution bands (10–90%)
- Risk acceleration tracking
- Fraud rate over time
- User risk concentration analysis
- Fraud pattern risk profiling
- High-risk transaction investigation table
  
## 🏗️ Architecture Overview
---
Synthetic / Processed Data
↓
Feature Engineering
↓
Pattern Discovery (Clustering)
↓
Composite Risk Engine
↓
Explainability Layer
↓
Live Intelligence Dashboard
---

## ⚙️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- Streamlit
- YAML-based configuration

---

## 📁 Project Structure

project/
├── app/ # Streamlit dashboard
├── src/ # Risk, explainability & pattern logic
├── data/ # Processed datasets
├── notebooks/ # Experiments and analysis
├── requirements.txt
└── README.md


---

## 🎯 What This Project Demonstrates

- Understanding of fraud as a **system**, not just a model
- Strong emphasis on explainability and usability
- Ability to design analyst-facing tools
- End-to-end ownership: data → logic → UI → deployment

---

## ⚠️ Disclaimer

This project uses synthetic and simulated data for learning
and portfolio purposes only. It does not represent real users
or real financial transactions.

---



## 🏗️ Architecture Overview

