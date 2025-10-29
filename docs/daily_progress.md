# 📘 Daily Progress Log — *Sales Analytics System*

---

## 🚀 Project Overview
This project simulates a **real-world analytics environment** — including data extraction, transformation, loading (ETL), and dashboarding — using **Python, PostgreSQL, and Power BI**.

---

## 🧩 Architecture


---

## 📅 Daily Progress

---

### 🗓️ **Day 1 — Environment Setup**
✅ Set up folder structure  
✅ Installed PostgreSQL  
✅ Created `salesdb` database and `transactions` table  
✅ Pushed initial project to GitHub  

---

### 🗓️ **Day 2 — Base ETL + Logging**
✅ Created Python ETL script:  
`extract(read from csv) → transform(calculate total sales) → load(insert to database)`  
✅ Understood and implemented **production-style logging**  
✅ Pushed all changes to GitHub  

---

### 🗓️ **Day 3 — File Automation + Modularization**
✅ Added **automatic latest-file ingestion** using `glob` and `os`  
✅ Implemented **schema validation** and column alignment for extra/missing columns  
✅ Added `config/` folder and restructured the project for **modular, production-style pipeline**  

---

### 🗓️ **Day 4 — Config Loader & Extract Module**
✅ Centralized all paths and database credentials into `config.yaml`  
✅ Built `config_loader.py` to read YAML configuration dynamically  
✅ Created `extract.py` with:
- `get_latest_file()` → fetches newest CSV from folder  
- `extract_data()` → reads and loads CSV data into DataFrame  

---

### 🗓️ **Day 5 — Transform Module**
✅ Enhanced `config_loader.py` for full integration with ETL modules  
✅ Created `transform.py` to clean, align, and transform data using **pandas**  
✅ Added schema checks to ensure consistent structure before loading  

---

### 🗓️ **Day 6 ,7 — Load Module (Production-Ready)**
✅ Built fully modularized **Load phase**  
✅ Used **psycopg2.extras.execute_values()** for **chunked inserts** (optimized bulk inserts)  
✅ Implemented **`WITH` statement + psycopg.SQL** for **safe SQL execution**  
✅ Tested load process with dummy DataFrame (`test_load.py`)  
✅ Confirmed successful end-to-end load to PostgreSQL  

---

### 🗓️ **Day 8 — Main Module (Production-Ready)**
✅ Built the final orchestration phase through main.py 

---

### 🗓️ **Day 9 — ISSUE Fix and Modularization completed**
✅ fix(postgres): handle schema-qualified table names correctly using sql.Identifier
✅ Modularization completed with all components running smoothly

---

### 🗓️ **Day 10 , 11 — ADDED archive_manager.py**
✅ Added(postgres): to stop same file getting processed multiple times

---

### 🗓️ **Day 12 — TEST ( archive_manager.py )**
✅ Tested archive_manager each functionality by creating unit tests for each of them

---

### 🗓️ **Day 13 — FEAT : Integrated archive_manager in ETL**
✅ Incorporated the archival step after the extract module is run.

---

### 🗓️ **Day 14 — REFACTOR : Making changes to extract.py and main.py**
✅ Trying to build isolation across each steps in the pipeline.

## 🧠 Summary of Learning So Far

| Area | Skill / Concept | Type |
|:--|:--|:--|
| ETL Design | Modular extraction, transformation, loading | ✅ Applied |
| Config Management | YAML + dynamic loader pattern | ✅ Applied |
| Database Ops | psycopg2, transactions, safe SQL | ✅ Applied |
| Logging | Multi-handler logging and file-based logs | ✅ Applied |
| Data Handling | Schema alignment, null handling | ✅ Applied |

---

## 🏁 Next Steps

- Implement **data type validation** in Transform phase  
- Add **error handling and retries** in Load  
- Introduce **alerting via email or log-based triggers**  
- Connect PostgreSQL → Power BI for final dashboard  

---

> 🧡 *Maintained daily by Ria Gupta — documenting a transition from MIS to Data Engineering with hands-on, production-style projects.*
