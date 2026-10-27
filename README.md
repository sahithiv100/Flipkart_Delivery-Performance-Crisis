# 📦 Flipkart Delivery Performance Crisis: Operational Diagnostic & Intervention Prototype

> **⚠️ MANDATORY DISCLAIMER:**  
> **100% SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA.**  
> This project is an illustrative operational prototype built for data science, operations research, and product demonstration. All order IDs, timestamps, fulfillment centers, carrier metrics, and customer interactions are synthetic computer-generated records. No proprietary systems, real customer data, or live Flipkart APIs were scraped or accessed.

---

## 🎯 Executive Problem Statement
During high-velocity shopping periods and peak promotional events, e-commerce fulfillment networks experience localized delivery SLA breaches that lead to customer churn, increased concessions/refund vouchers, and expensive re-attempts. 

This interactive system provides an end-to-end operational diagnostic platform to:
1. **Deconstruct order journeys** across 9 sequential lifecycle milestones (Order Placed $\rightarrow$ Pick $\rightarrow$ Pack $\rightarrow$ Dock Staging $\rightarrow$ Linehaul Transit $\rightarrow$ Destination Hub $\rightarrow$ Out for Delivery $\rightarrow$ Doorstep Attempt $\rightarrow$ Final Delivery).
2. **Isolate root-cause bottlenecks** across warehouse shift staffing shortages, cross-regional inventory stockouts, carrier trunkline delays, and first-attempt doorstep failures.
3. **Deploy a pre-delivery early warning machine learning model** (Random Forest) that flags high-risk orders *before* linehaul dispatch using pre-delivery operational signals.
4. **Formulate evidence-backed recommendations** with governance guardrails and human-in-the-loop sign-offs.
5. **Simulate what-if pilot operational interventions** (flex staffing, inventory pre-positioning, carrier reallocation, WhatsApp address pre-validation) with immediate recalculation of SLA compliance and financial ROI.

---

## 🗂️ Project File Structure (Zero Subfolder Root Layout)
In compliance with project specifications and to guarantee 100% plug-and-play deployment on **Streamlit Community Cloud** and **GitHub**, all files reside directly in the root directory:

```text
delivery_performance_crisis/
├── app.py                  # Primary Streamlit web application & multi-page interactive dashboard
├── data_generator.py       # Parametric synthetic data generation engine with reproducible random seed
├── analytics_engine.py     # Stage deconstruction, ML risk classifier, recommendations & what-if simulator
├── ui_components.py        # Dark navy/charcoal styling, custom KPI cards, banners & Plotly theme
├── requirements.txt        # Exact Python dependencies
└── README.md               # Architecture documentation, run instructions & verification notes
```

---

## ⚙️ Quickstart & Windows-Friendly Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.
- PowerShell or Windows Command Prompt.

### Step 1: Clone / Navigate to the Directory
```powershell
cd C:\Users\DELL\.gemini\antigravity\scratch\delivery_performance_crisis
```

### Step 2: Create and Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1

# (If running standard cmd.exe, use: .\venv\Scripts\activate.bat)
```

### Step 3: Install Required Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
The browser will automatically open to `http://localhost:8501`.

---

## 🚀 One-Click Deployment to Streamlit Community Cloud
1. Push this folder directly to a new GitHub repository (e.g., `flipkart-delivery-crisis`).
2. Log into [share.streamlit.io](https://share.streamlit.io/).
3. Select the repository, choose branch `main`, set `app.py` as the entrypoint file.
4. Click **Deploy**. Since all modules are flat in the root directory, no path resolution errors can occur!

---

## 💡 System Modules & Technical Capabilities

| Module | Purpose & Core Capabilities |
| :--- | :--- |
| `app.py` | Full multi-page application offering 8 views: Executive Overview, Bottleneck Deep-Dive, Late-Order Risk Queue (ML), Targeted Recommendations, What-If Pilot Simulator, Manager Exploration Suite, How the Algorithm Works, and Data Explorer. |
| `data_generator.py` | Generates 1,500 - 6,000 synthetic order journeys with reproducible seeds, realistic FC capacities (Malur, Bhiwandi, Farukhnagar, Haringhata, Shamshabad), shifts (A, B, C-Night), 5 carriers (Ekart, Delhivery, Shadowfax, BlueDart, Xpressbees), city tiers, and customer escalation tickets. |
| `analytics_engine.py` | Calculates SLA variance, primary bottleneck attribution, trains pre-delivery Random Forest classifier vs zero-rule baseline, generates data-backed recommendations with governance notes, and computes dynamic what-if pilot simulation with financial ledger. |
| `ui_components.py` | Injects dark charcoal/navy styling (`#0B0F19`, `#111827`) with restrained purple accents (`#8B5CF6`), responsive KPI cards, algorithm flowchart graph, and data dictionary specification. |

---

## 🔬 Predictive Machine Learning & Transparency Disclosures
- **Pre-Delivery Early Warning System:** Evaluates order risk strictly using pre-transit signals (warehouse staffing ratio, pick duration, dock staging time, category complexity, carrier, city tier, order hour).
- **Zero-Rule Baseline Disclosed:** To avoid inventing accuracy, Random Forest classifier performance (Accuracy, Precision, Recall, F1, ROC-AUC) is benchmarked against a `DummyClassifier(strategy="most_frequent")`.
- **Human-in-the-Loop Governance:** In accordance with industrial safety and labor policies, all high-impact actions (shift reassignments, carrier contract reallocation caps) require human managerial review.

---

## 🧪 Verification & Testing Completed
- [x] Verified synthetic data generation with strict timestamp progression ($t_{\text{order}} < t_{\text{pick}} < t_{\text{pack}} < t_{\text{manifest}} < t_{\text{dispatch}} < t_{\text{transit}} \le t_{\text{delivery}}$).
- [x] Tested Random Forest model training and baseline metrics computation.
- [x] Tested What-If intervention simulator across extreme parameter sliders.
- [x] Validated CSV data downloads for both the live at-risk queue and full filtered dataset.
- [x] Validated responsive dark mode UI layout and charts.
