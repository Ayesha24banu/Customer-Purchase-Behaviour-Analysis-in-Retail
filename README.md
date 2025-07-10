# 🛒 Customer Purchase Behavior Analysis in Retail

This project presents a full-cycle data science solution for analyzing and deriving insights from retail transactional data  using Python and Power BI. It involves structured data cleaning, EDA, customer segmentation using RFM + KMeans, Market Basket Analysis using the Apriori algorithm, and business dashboard creation. Outputs are stored in CSV, visualized with Matplotlib/Seaborn, and optionally integrated with a MySQL database or BI dashboards (Power BI/Tableau).

---

## 🎯 Business Objective

This project aims to derive strategic insights from customer purchase data in an e-commerce/retail environment by:

- Identify customers purchasing patterns and trends
- Segmenting customers based on behavioral metrics (Recency, Frequency, Monetary)
- Generate association rules for product bundling
- Recommend strategies for targeted marketing and inventory optimixation
- Visualize insights through an interactive Power BI dashboard

---

## 📦 Dataset Overview
- **Source**: [Kaggle – Online Retail II Dataset](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)
- **Period**: Dec 2009 – Dec 2011
- **Size**: 779,000+ records
- **Columns**:

| Feature        | Description                                 |
|----------------|---------------------------------------------|
| `InvoiceNo`    | Unique transaction ID                       |
| `StockCode`    | Unique product ID                           |
| `Description`  | Product description                         |
| `Quantity`     | Quantity purchased                          |
| `InvoiceDate`  | Date and time of transaction                |
| `UnitPrice`    | Price per item                              |
| `CustomerID`   | Unique customer ID                          |
| `Country`      | Country of purchase                         |

⚠️ **Note:** *Full dataset not included due to GitHub file size limits. Sample CSVs are used for demonstration.*

---

## 🧰 Tools and Technologies

| Layer            | Technology                              |
|------------------|------------------------------------------|
| Language         | Python 3.10+                             |
| Data Handling    | Pandas, NumPy                            |
| Visualization    | Matplotlib, Seaborn                      |
| ML Algorithms    | KMeans (Scikit-learn), Apriori (mlxtend) |
| Database         | MySQL (via `mysql-connector-python`)     |
| Notebook         | Jupyter Notebook                         |
| Dashboard (opt.) | Power BI (4-page executive dashboard)    |

---

## 🧱 Project Architecture

```
customer_purchase_analysis/
├── data/ # Raw dataset
│ └── online_retail.csv
│
├── scripts/ # Modular ETL/ML scripts
│ ├── _init_.py
│ ├── utils.py
│ ├── data_cleaning.py
│ ├── mysql_pipeline.py
│ ├── eda_analysis.py
│ ├── rfm_segmentation.py
│ └── market_basket.py
│
├── notebooks/ # Main pipeline orchestrator
│ └── purchase_analysis.ipynb
│
├── outputs/
│ ├── data/
│ │ ├── clean_online_retail.csv
│ │ ├── rfm_segments.csv
│ │ └── association_rules.csv
│ └── figures/
│ ├── eda_fig/
│ ├── rfm_fig/
│ └── mba_fig/
│
├── logs/
│ └── process_log.log
├── Reports/
│ ├── Customer_Purchase_Analysis.pbix
│ ├── Customer_Purchase_Analysis.pdf
│ ├── BI_Executive_Summary.png
│ ├── BI_Sales_Trend.png
│ ├── BI_RFM_Segments.png
│ └── BI_Market_Basket.png
├── requirements.txt
└── README.md
```

---

## 🔍 Project Workflow

### 📌 Step 1: Data Cleaning
- Drop duplicates
- Handle missing values (esp. `CustomerID`)
- Removes missing or invalid values
- Creates new columns like `TotalPrice`
- Logs all steps and saves cleaned file

📄 Cleaned dataset: `outputs/data/clean_online_retail.csv

### 📌 Step 2: MySQL Pipeline
- Insert & retrieve cleaned data into/from MySQL
- Optional for production deployment and data integration
- Handles deduplication and backup
  
### 📌 Step 3: Exploratory Data Analysis (EDA)
- Top 10 selling products
- Monthly & daily revenue trends
- Hourly purchase patterns (peak times)
- Country-wise revenue distribution
- Plots saved to `outputs/figures/eda_fig/`

📁 Outputs: `outputs/figures/eda_fig/`

### 📌 Step 4: Key Performance Indicator (KPI) Calculation
- Total Revenue
- Unique Customers
- Quantity Sold
- Average Order Value
- Core KPIs (Revenue, Quantity, AOV, etc.)

### 📌 Step 5: RFM Segmentation
- Calculates Recency, Frequency, and Monetary values
- Removes outliers using IQR
- Scales features and applies KMeans clustering → 4 customer segments
- Uses silhouette + elbow methods to determine optimal `k`
- Segments labeled for business use:
  - `Loyal Valuable Customers`
  - `Recent High-Spenders`
  - `Occasional Low-Spenders`
  - `Inactive Spenders`
- Plots saved to `outputs/figures/rfm_fig/`

📁 Outputs: `outputs/figures/rfm_fig/`
📄 RFM: `outputs/data/rfm_segments.csv`


### 📌 Step 6: Market Basket Analysis
- Applies Apriori algorithm to find frequent itemsets
- Generates association rules (support, confidence, lift)
- Visualizes top rules (bubble chart, lift bar chart)
- Great for cross-selling & bundling strategies

📁 Outputs: `outputs/figures/mba_fig/`  
📄 Rules: `outputs/data/association_rules.csv`

### 📊 Step 7: Power BI Dashboard Visualization
- 4 Pages:
  - Executive Summary
  - Sales Analysis
  - Customer Segments
  - Association Rules

---

## 📈 Example Business Insights

| Insight           | Value                                         |
|-------------------|-----------------------------------------------|
| 📌 70% of revenue | Comes from top 20% of customers               |
| 🎯 Peak time      | 10 AM – 2 PM on weekdays                      |
| 💰 Best countries | UK (80%), Germany, Netherlands                |
| 🛍️ Bundling       | "Gift box set" + "Teacups" has 62% confidence |
| 📊 Segment        | 4 clusters with tailored marketing strategies |

---

## 💼 Use Cases

- 📦 Inventory planning based on top co-purchases
- 🎯 Loyalty programs for high-value customers
- 📢 Targeted email offers during peak purchase times
- 📊 Executive dashboards via Power BI (optional)

---

## 🤖 Results (Summary)

- **Customer Segments**:
  - Loyal Valuable Customers
  - Inactive Spenders
  - Occasional Low Spenders
  - Recent High Spenders

- **Example Association Rule**:
  - If user buys `"Set of Teacups"` → 62% likely to buy `"Gift Wrap"`

---

## 📊 Power BI Dashboard Overview

4 Page Executive BI Dashboard (`Reports/`):

### Page 1: Executive Summary
- Total Revenue, Orders, Customers
- Revenue by Country
- Segment distribution (from RFM)

### Page 2: Sales Trends
- Monthly/Weekly Revenue Trend
- Top Products Sold
- Peak Hour Purchases

### Page 3: RFM Customer Segments
- RFM Cluster Scatter Plots
- Segment-specific KPIs

### Page 4: Market Basket Rules
- Rules Table (A ➡ B)
- Top Rules by Lift
- Scatter: Confidence vs Support

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL Server (optional)
- Jupyter Notebook

### Installation

```bash
git clone https://github.com/your-username/customer_purchase_analysis.git
cd customer_purchase_analysis
pip install -r requirements.txt
```

### Run Notebook

```bash
jupyter notebook notebooks/purchase_analysis.ipynb
```

⚠️ Update your MySQL credentials inside `purchase_analysis.ipynb` and `mysql_pipeline.py`.

---

## 📝 Conclusion

- RFM segmentation helps **personalize marketing** and **optimize offers**.
- Market Basket Analysis guides **product placement**, **bundling**, and **inventory management**.
- Visual outputs can be used by business teams with minimal technical effort.

---

### 🔄 Future Enhancements
- Live segmentation using streaming data
- Recommendation engine using collaborative filtering
- Customer lifetime value prediction
- Streamlit app for business teams
- AutoML for dynamic segmentation
- NLP analysis on customer reviews
- Real-time customer segmentation pipeline
- API-based deployment via FastAPI or Flask

---

### 📎 Deliverables
- `purchase_analysis.ipynb`: Master notebook
- `rfm_segments.csv`: RFM clustering results
- `association_rules.csv`: Market basket rules results
- Visual charts in `/outputs/figures`
- MySQL-ready table insertions (optional)
- Power BI dashboard images in Reports/

---

## 🙏 Acknowledgment

Thanks to the UCI & Kaggle community for the retail dataset.

---

### 👤 Author
**Ayesha Banu**
- 🎓 M.Sc. Computer Science | 🏅 Gold Medalist
- 💼 Data Scientist | Data Analyst | Full-Stack Python Developer | GenAI Enthusiast
- 📫 [LinkedIn](https://www.linkedin.com/in/ayesha_banu_cs)
- **Project:** Customer Purchase Behavior Analysis in Retail  -- 2025  
---

### 📄 License
Distributed under the MIT License. See `LICENSE` file for details.


