# Amazon Sales Data Analysis & Dashboard

This project provides a full analysis of Amazon sales data and an interactive dashboard to visualize key insights. The dashboard covers **5 key aspects** of sales analytics and can be used to explore sales trends, top products, customer segmentation, fulfillment, and geographical analysis.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Project Structure](#project-structure)  
4. [Installation & Setup](#installation--setup)  
5. [Data Preparation](#data-preparation)  
6. [Running the Dashboard](#running-the-dashboard)  
7. [Analysis Breakdown](#analysis-breakdown)  
8. [Dependencies](#dependencies)  
9. [Future Improvements](#future-improvements)  
10. [Commit Guidelines](#commit-guidelines)  
11. [Author](#author)  

---

## Project Overview

This project analyzes Amazon sales data stored in MongoDB Atlas and presents insights using an interactive **Python dashboard**.  

- Backend data analysis is done in `analysis.py`.  
- Frontend dashboard is implemented in `dashboard.py` using **Plotly Dash** for interactivity and modern styling.  

The dashboard allows users to interactively filter data, view charts, and download visualizations.

---

## Key Features

1. **Total Sales & Orders**:  
   - Total revenue  
   - Total number of orders  
   - Average order value  

2. **Monthly Sales Trend**:  
   - Revenue over time (monthly)  
   - Line chart for trend analysis  

3. **Top-Selling Categories & Products**:  
   - Quantity sold and revenue per category  
   - Interactive bar charts  

4. **Customer Segmentation**:  
   - B2B vs Individual customer analysis  
   - Revenue and order counts  
   - High-value customer identification  

5. **Fulfillment & Geographical Analysis**:  
   - Orders by fulfillment method  
   - Revenue by states and cities  

---

## Project Structure
amazon-dashboard/
│
├─ analysis.py # Backend data processing and aggregation
├─ dashboard.py # Frontend interactive dashboard using Plotly Dash
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation
└─ data/ # Optional #CSV/Excel files



---

## Installation & Setup

** 1. Clone the repository:**

```
git clone 
cd amazon-dashboard
```

** 2. Create a virtual environment: **

```
python -m venv .venv

```
*** 3. Activate the virtual environment: ***
```
Windows (cmd): .venv\Scripts\activate

```

*** 4. Install dependencies: ***

pip install -r requirements.txt


