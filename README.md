# Sales Analytics System

### 🚀 Project Overview
This project simulates a real-world analytics environment — including data extraction, transformation, loading (ETL), and dashboarding — using **Python, PostgreSQL, and Power BI**.

---

### 🧩 Architecture
Data Source → Python ETL → PostgreSQL (Data Store) → Power BI (Visualization)

---

### 📅 Day 1 Progress
- ✅ Set up folder structure
- ✅ Installed PostgreSQL
- ✅ Created `salesdb` database and `transactions` table
- ✅ Pushed project to GitHub

### 📅 Day 2 Progress
- ✅ Created Python ETL script ( extract(read data from csv) -> transform(calculated total sales) -> load(load the results into database table) )
- ✅ Understood the logging module ( **production style logging**)
- ✅ Pushed changes

### 📅 Day 3 Progress
- ✅ Added automatic latest-file ingestion using glob
- ✅ Added schema validation & column alignment for extra/missing columns
- ✅ Added config folder , changed the folder structure so as to modularize ( **production style data pipeline**)
