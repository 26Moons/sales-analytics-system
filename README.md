# 🧠 Sales Analytics System

### 🚀 Overview
A complete **end-to-end Sales Analytics Data Pipeline** simulating a real-world enterprise environment.  
It automates data ingestion, transformation, and loading into a relational data store — ready for Power BI reporting.

---

### 🏗️ Architecture


---

### ⚙️ Tech Stack

| Layer | Tool | Purpose |
|:--|:--|:--|
| Data Source | CSV | Raw sales data |
| Data Processing | Python (pandas, psycopg2, yaml, logging) | ETL orchestration |
| Data Storage | PostgreSQL | Central analytical data store |
| Visualization | Power BI | Dashboards and metrics visualization |
| Version Control | Git + GitHub | Code management and documentation |

---

###
---

### 🧩 Key Features

- **Dynamic File Ingestion**: Automatically detects and ingests the latest CSV file.
- **Schema Validation**: Aligns columns between source files and database schema.
- **Config-Driven Pipeline**: All paths, DB credentials, and parameters stored in YAML.
- **Modularized ETL**: Extract, Transform, and Load implemented as independent modules.
- **Robust Logging**: Timestamped, rotating logs for every pipeline run.
- **Chunked Inserts**: Optimized PostgreSQL ingestion for large datasets.
- **Error Handling**: Graceful failure capture and retry-ready design.

---

### 🧠 Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/26Moons/sales-analytics-system.git
   cd sales-analytics-system


2.Create a virtual environment and install dependencies:

   pip install -r requirements.txt


3.Update your config/config.yaml with:

  local file paths
  
  PostgreSQL credentials
  
  log paths

4. Run the pipeline:

  python main_etl.py

  
 📁 Project Structure
 sales-analytics-system/
│
├── config/
│ ├── config.yaml
│ └── init.py
│
├── etl_scripts/
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ └── init.py
│
├── utils/
│ └── utils.py
│
├── logs/
│ └── pipeline.log
│
├── notebooks/
│ └── exploration.ipynb
│
├── reports/
│ └── dashboard.pbix
│
├── docs/
│ ├── daily_progress.md
│ └── design_notes.md
│
├── main_etl.py
└── README.md

