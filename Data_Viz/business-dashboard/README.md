# Business Dashboard: Monthly Sales Growth Visualization

A professional **interactive business analytics dashboard** built with **Plotly and Python**, designed to visualize monthly sales performance, ad expenditure, and growth metrics.  
This project marks the completion of **Chapter 15** in *Python Crash Course (3rd Edition)* — extended far beyond the textbook exercise into a **full-scale data visualization project**.

---

##  Features

- **Multi-Chart Layout** — Combines Line, Bar, Scatter, and Donut charts in one interactive dashboard.  
- **Dynamic Annotations** — Highlights key insights like the peak-sales month.  
- **Custom Hover Templates** — Clean, professional data tooltips for better interpretation.  
- **Color-Coded Visualization** — Distinguishes sales, ad spend, and growth metrics intuitively.  
- **Interactive Dashboard Export** — Generates a standalone HTML dashboard that can be opened in any browser.

---

##  Tech Stack

- **Language:** Python 3 
- **Library:** Plotly (`plotly.graph_objects`, `plotly.subplots`)
- **Tools Used:** `make_subplots`, annotations, shared axes, custom layouts  
- **Output Format:** Interactive `.html` file

---

Each subplot includes **custom hover data**, **themed axis titles**, and **dynamic scaling** for optimal readability.

---

##  How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Haashiraaa/business-dashboard.git
cd business-dashboard

# 2. Install dependencies
pip install plotly
pip install emoji

# 3. Run the script
python business_dashboard.py

# 4. View the dashboard
# The HTML file will be saved automatically in the same directory.
