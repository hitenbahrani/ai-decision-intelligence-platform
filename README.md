# AI Decision Intelligence & Governance Platform

An end-to-end **production-style AI decision governance system** for credit risk decisioning, combining:
- Predictive modeling
- Policy-based decision controls
- Model explainability (SHAP)
- Fairness & bias auditing
- Executive-ready Streamlit dashboard

This project simulates how modern enterprises govern AI-driven decisions in regulated environments.

---

## 🔍 What This Project Demonstrates

- ✅ Probabilistic credit risk modeling
- ✅ Policy thresholds (auto-approve / manual review / reject)
- ✅ Model explainability using SHAP reason codes
- ✅ Fairness & disparate impact analysis
- ✅ Governance-first deployment (models offline, artifacts only)
- ✅ Executive-facing dashboard (Streamlit)

---

## 🧠 Architecture Overview
notebooks/
└── 01_data_overview.ipynb     # Training, SHAP, fairness, artifact generation

models/
├── credit_decision_model.joblib
└── decision_threshold.joblib

reports/artifacts/
├── decision_df.csv            # Decisions + probabilities + reason codes
├── fairness_df.csv            # Fairness metrics by protected group
├── baseline_model.joblib
└── challenger_model.joblib

dashboard/
└── app.py                     # Streamlit executive dashboard
---

## 📊 Dashboard Capabilities

### A) Decision Outcomes
- Auto-Approve / Manual Review / Reject counts
- Policy-driven thresholds

### B) Risk Distribution
- Probability of default histogram

### C) Customer Reason Codes
- Top SHAP-based drivers per decision
- Transparent, regulator-friendly explanations

### D) Fairness & Governance
- Approval rates by protected attribute
- Disparate impact calculation
- 80% rule compliance check
- Governance recommendations

---

## 🛡️ Governance Philosophy

This system **does NOT serve live models**.

Instead:
- Models are trained offline
- Only **governed artifacts** are consumed
- Ensures auditability, reproducibility, and regulatory safety

This mirrors real-world enterprise AI governance.

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py