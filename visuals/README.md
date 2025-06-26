# Vendor & Brand Performance Analysis

This project demonstrates a full-stack data workflow for analyzing vendor and product performance from raw transactional CSVs to statistical insights and executive-level business reporting. It combines SQL-backed ingestion, programmatic cleaning, statistical testing, and executive visualization — all fully scripted for reproducibility and scalability.

---

## 💼 Business Problem

Procurement and commercial teams often rely on intuition or static reports to evaluate vendor and brand performance. This leads to inconsistent pricing strategies, missed promotional opportunities, and vendor inefficiencies.

**Goal:** Build an automated analytics pipeline to answer key business questions:
- Who are our most and least profitable vendors?
- Which brands are ripe for promotional focus?
- Are top vendors *statistically* more efficient than low ones?

---

## 🔁 End-to-End Workflow

1. **Raw CSV ingestion** via a Python script into an SQLite database (`inventory.db`)  
2. **SQL-backed transformation and joins** to generate clean, unified tables  
3. **Derived metrics** such as `ProfitMargin`, `StockTurnover`, `PurchaseContribution`  
4. **Segmentation and statistical testing** of vendors using Welch’s t-test and confidence intervals  
5. **Visual storytelling** through plots and a formatted business report

---

## 🧠 Key Technologies

- `pandas`, `numpy` — data manipulation  
- `sqlite3`, `SQL` — structured ingestion and querying  
- `scipy.stats` — hypothesis testing, confidence intervals  
- `matplotlib`, `seaborn` — visual storytelling  
- `python-docx` — automated Word report generation  
- Jupyter — iterative exploration

---

## 📁 Project Structure

```
vendor-performance-analysis/
│
├── data/                        # (Mocked) input CSVs
│   └── sample_data.csv
│
├── scripts/                     # Pipeline automation scripts
│   ├── ingest_data.py
│   ├── clean_prepare.py
│   └── analyze.py
│
├── notebooks/                   # Exploratory and visual workflows
│   └── eda_visuals.ipynb
│
├── visuals/                     # All analysis plots
│   └── [scatter, donut, histograms, bar charts...]
│
├── reports/
│   └── Vendor_Brand_Analysis_Report.docx
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Add your CSVs to /data

# Step 3: Run the pipeline
python scripts/ingest_data.py
python scripts/clean_prepare.py
python scripts/analyze.py
```

All outputs (plots and Word reports) are generated automatically.

---

## 📊 Visual Highlights

### 🔹 Top Vendors' Purchase Share

> Over 66% of all purchases come from just 10 vendors.

<img src="visuals/pie%20char%20top%20vendors%20contribution.png" width="600"/>

---

### 🔹 Profitability: Top vs. Low Vendors

> Statistically significant margin difference confirmed via Welch’s t-test and confidence intervals.

<img src="visuals/top%20vs%20low%20vendors%20hist.png" width="600"/>

---

### 🔹 Brand-Level Targeting

> Low-sales, high-margin brands surfaced for promotional pricing or push.

<img src="visuals/brands%20promotional%20scatter.png" width="600"/>

---

### 🔹 Product and Vendor Activity

<img src="visuals/top%20vendors.png" width="600"/>

---

### 🔹 Metric Distribution Analysis

<img src="visuals/hist.png" width="600"/>

---

## 📈 Statistical Approach

To move beyond descriptive summaries, the analysis applies:

- **Quantile-based segmentation** for vendor classification  
- **Confidence intervals** around average profit margins  
- **Welch’s t-test** to test significance between vendor groups  
- **Visual confirmation** through annotated histograms and KDE plots

---

## 📎 Report Output

All insights are packaged into a Word-format business report with embedded visuals and annotated conclusions — ideal for presentation to commercial or procurement teams.

📄 [`reports/Vendor_Brand_Analysis_Report.docx`](reports/Vendor_Brand_Analysis_Report.docx)

---

## 🔐 Data Note

This repo includes a `sample_data.csv` for demonstration only. Proprietary vendor data is excluded for privacy.

---

## 📌 Next Steps

- Add time-based performance trends  
- Deploy as a Streamlit or Dash dashboard  
- Automate CI/CD pipeline for weekly reporting

---

## 👋 Contact

Open to collaboration or feedback. This project is actively maintained.
