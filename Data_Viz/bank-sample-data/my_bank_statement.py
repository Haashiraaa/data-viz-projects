# ────────────────────────────────────────────────
# EXPENDITURE DASHBOARD (May–Oct 2025)
# Author: Haashiraaa
# Description: Cleaned and documented version of the
# data visualization script showing bank expenditure
# using bar and pie charts.
# ────────────────────────────────────────────────

import csv  # CSV reading for cleaned bank data
from datetime import datetime  # Date handling for monthly aggregation
from itertools import chain  # Helper to iterate combined lists for styling
import textwrap  # Wrap long summary text for display in figure
import matplotlib.pyplot as plt  # Plotting library
from matplotlib.gridspec import GridSpec  # Grid layout manager for subplots
from icecream import ic  # Debug printing helper
from formatted_time import normalize_date  # Custom date normalizer for input dates
from saver import save_plot
from pathlib import Path
import sys

# ────────────────────────────────────────────────
# DEBUG MODE SETUP
# ────────────────────────────────────────────────
# Toggle debug printing via the icecream ic() wrapper
DEBUG = False
if not DEBUG:
    ic.disable()
else:
    ic.enable()

# ────────────────────────────────────────────────
# FILTERS AND PLACEHOLDERS
# ────────────────────────────────────────────────
# Words to filter out from transactions (case-insensitive)
filter_words = ["OWealth Withdrawal", "Card", "Save"]
norm_filter = [fil.lower() for fil in filter_words]  # normalize for comparison
filtered_count = 0  # counter for how many rows were filtered

# Lists to store parsed transaction data
credit, debit = [], []  # numeric values for credits and debits
credit_date, debit_date = [], []  # corresponding transaction dates
credit_desc, debit_desc = [], []  # descriptions for classification
monthly_totals = {}  # totals aggregated by "YYYY-MM" key

# ────────────────────────────────────────────────
# READ AND PROCESS CLEANED CSV DATA
# ────────────────────────────────────────────────
# Open the cleaned CSV and parse rows into lists for further processing

file = Path("sample_cleaned_bank_data.csv")

if not file.exists():
    print("File not found! Exiting program.")
    sys.exit()

with file.open() as fc:
    reader = csv.DictReader(fc)
    header_row = [next(reader) for _ in range(5)]  # Skip header sample rows

    for row in reader:
        # Extract and normalize relevant fields
        amount = row['Debit/Credit(₦)'].replace(",", "").strip()  # remove thousands sep
        desc = row['Description'].strip().lower()  # normalize description for matching
        trans_date = normalize_date(row['Trans. Date'].strip())  # convert to datetime
        amt = float(amount)  # convert numeric string to float

        # Filter out transactions that match any of the filter keywords
        if any(word in desc for word in norm_filter):
            filtered_count += 1
            continue  # skip further processing for filtered rows

        # Classify transaction as debit (negative) or credit (positive)
        if amt < 0:
            debit.append(abs(amt))  # store as positive expense value
            debit_date.append(trans_date)
            debit_desc.append(desc)
        elif amt > 0:
            credit.append(amt)
            credit_date.append(trans_date)

# ────────────────────────────────────────────────
# CATEGORIZE EXPENDITURE DATA
# ────────────────────────────────────────────────
# Define categories and keywords for simple keyword-based classification
categories = {
    "Transfers": ["transfer to"],
    "Mobile Data": ["mobile data"],
    "Airtime": ["airtime"],
    "Bills & Levies": ["electricity", "sms", "electronic money transfer levy"],
}

# Initialize mapping from category -> list of amounts
category_map = {cat: [] for cat in categories}

# Map each debit transaction into appropriate category based on keywords
for desc, amt in zip(debit_desc, debit):
    for cat, keywords in categories.items():
        if any(k in desc for k in keywords):
            category_map[cat].append(amt)
            break
    else:
        # If no category matched, group under "Others"
        category_map.setdefault("Others", []).append(amt)

# Calculate monthly totals aggregated by year-month (e.g., "2025-05")
for d_d, d in zip(debit_date, debit):
    month = datetime.strftime(d_d, "%Y-%m")
    monthly_totals[month] = monthly_totals.get(month, 0) + d

# ────────────────────────────────────────────────
# COMPUTE AGGREGATE CATEGORY DATA
# ────────────────────────────────────────────────
# Sum amounts per category for plotting
plot_category = {cat: sum(amt) for cat, amt in category_map.items()}

# Prepare outer and inner pie breakdowns:
# outer_data groups Transfers vs Others (aggregated),
# inner_data shows breakdown of the "Others" group by its categories
outer_data = {'Transfers': 0, 'Others': 0}
for cat, amounts in category_map.items():
    total = sum(amounts)
    if cat == 'Transfers':
        outer_data['Transfers'] += total
    else:
        outer_data['Others'] += total

# inner_data contains category totals excluding Transfers (so it describes "Others")
inner_data = {cat: sum(amt) for cat, amt in category_map.items() if cat != 'Transfers'}

# ────────────────────────────────────────────────
# PREPARE LABELS AND CHART VARIABLES
# ────────────────────────────────────────────────
# Months and amounts for the monthly bar chart
months = list(monthly_totals.keys())  # e.g., ["2025-05", "2025-06", ...]
amount = [round(amt) for amt in monthly_totals.values()]

# Human-readable month labels for x-axis (explicit mapping for this period)
month_labels = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
full_month = ["May", "June", "July", "August", "September", "October"]
# Category labels and expenses for categorical bar chart
cat_labels = list(plot_category.keys())
cat_expenses = [round(amt) for amt in plot_category.values()]

# Values and labels used for the nested pie chart (outer ring and inner ring)
outside = [round(amt) for amt in outer_data.values()]
outside_labels = list(outer_data.keys())
inside = [round(amt) for amt in inner_data.values()]
inside_labels = list(inner_data.keys())

# ────────────────────────────────────────────────
# COLOR SCHEMES
# ────────────────────────────────────────────────
# Color mappings for pie slices and bars
outer_colors = {1: "tab:blue", 2: "#D27045"}  # two-tone outer pie
inner_colors = {1: "purple", 2: "tab:orange", 3: "#F9D040"}  # inner pie slices
bar1_colors = {
    "2025-05": "red",
    "2025-06": "green",
    "2025-07": "#2986cc",
    "2025-08": "orange",
    "2025-09": "purple",
    "2025-10": "blue",
}
bar2_colors = {1: "tab:blue", 2: "purple", 3: "tab:orange", 4: "#F9D040"}  # categorical bars

# ────────────────────────────────────────────────
# FIGURE LAYOUT CONFIGURATION
# ────────────────────────────────────────────────
plt.style.use("seaborn-v0_8")  # apply style for consistent visuals
fig = plt.figure(figsize=(20, 14))  # main figure container
gs = GridSpec(2, 2, figure=fig, wspace=0.25, hspace=0.4)  # grid layout for axes

# Create three axes: left column for pie, right column stacked for two bar plots
ax_pie = fig.add_subplot(gs[:, 0])  # pie spans both rows in left column
ax_bar1 = fig.add_subplot(gs[0, 1])  # top-right: monthly bar chart
ax_bar2 = fig.add_subplot(gs[1, 1])  # bottom-right: category bar chart

# Figure title
plt.suptitle("Expenditure Overview (May–Oct 2025)", fontsize=24, weight="bold", y=0.98)

# ────────────────────────────────────────────────
# PIE CHART (OUTER & INNER)
# ────────────────────────────────────────────────
# Build color lists for pie slices using the color mapping dictionaries
outer_col = [outer_colors.get(i, "tab:blue") for i in outer_colors]
inner_col = [inner_colors.get(i, "purple") for i in inner_colors]

# Outer pie: Transfers vs Others
wedges_outer, texts_outer, autotexts_outer = ax_pie.pie(
    outside,
    labels=outside_labels,
    autopct="%1.1f%%",
    startangle=45,
    radius=1,
    pctdistance=0.86,
    labeldistance=0.73,
    wedgeprops=dict(width=0.3, edgecolor="white"),
    colors=outer_col,
)

# Inner pie: breakdown of the "Others" group into specific categories
wedges_inner, texts_inner, autotexts_inner = ax_pie.pie(
    inside,
    autopct="%1.1f%%",
    startangle=90,
    radius=0.7,
    pctdistance=0.82,
    wedgeprops=dict(width=0.3, edgecolor="white"),
    explode=(0.01, 0.01, 0.01),  # slight separation for inner slices
    colors=inner_col,
)

# Add a white center circle to create a donut appearance
center_circle = plt.Circle((0, 0), 0.15, fc="white")
ax_pie.add_artist(center_circle)

# Add an internal title inside the pie axis area (positioned in axes coords)
ax_pie.text(
    0.5, 0.97,
    "Expenditure Share by Category (%)",
    ha='center',
    va='center',
    fontsize=18,
    weight='bold',
    transform=ax_pie.transAxes
)

# Legend for the inner pie that explains the breakdown of "Others"
ax_pie.legend(
    wedges_inner,
    inside_labels,
    title="Others Category\nBreakdown",
    title_fontproperties={"weight": "bold", "size": 12},
    fontsize=10,
    bbox_to_anchor=(1.05, 0.07),
    loc="lower right",
)

# Style the percent text labels to be bold and centered
for pct in chain(autotexts_outer, autotexts_inner):
    pct.set_fontweight("bold")
    pct.set_ha("center")
    pct.set_va("center")

# Make the outer labels bold for readability
for text in texts_outer:
    text.set_fontweight("bold")

# Ensure pie chart is drawn as a circle
ax_pie.set(aspect="equal")

# ────────────────────────────────────────────────
# BAR CHART 1 — Monthly Breakdown
# ────────────────────────────────────────────────
# Build colors for monthly bars based on the month keys
bar1_col = [bar1_colors.get(m, "green") for m in months]
ax_bar1.bar(months, amount, width=0.6, color=bar1_col, alpha=0.7, label=month_labels)

# Titles, axis labels and legend for monthly bar
ax_bar1.set_title("Monthly Expenditure Breakdown", fontsize=18, weight="bold")
ax_bar1.set_xlabel("Months (May–Oct)", fontsize=14, weight="bold")
ax_bar1.set_ylabel("Amount Spent (₦)", fontsize=14, weight="bold")
ax_bar1.margins(y=0.13)  # add vertical margins so bars don't touch edges
ax_bar1.legend(
title="Months",
title_fontproperties = {"weight":"bold", "size":12},
fontsize=10,
)

# Rotate xtick labels for readability
for label in ax_bar1.get_xticklabels():
    label.set_rotation(45)
    label.set_ha("right")

# ────────────────────────────────────────────────
# BAR CHART 2 — Category Breakdown
# ────────────────────────────────────────────────
# Categorical bar chart — colors are taken from bar2_colors values
ax_bar2.bar(cat_labels, cat_expenses, width=0.6, color=bar2_colors.values(), alpha=0.9, label=cat_labels)

# Titles, axis labels and legend for category bar
ax_bar2.set_title("Categorical Expenditure (May–Oct)", fontsize=18, weight="bold")
ax_bar2.set_xlabel("Category", fontsize=14, weight="bold")
ax_bar2.set_ylabel("Amount Spent (₦)", fontsize=14, weight="bold")
ax_bar2.margins(y=0.22)  # add vertical margins for readability
ax_bar2.legend(
title="Categories",
title_fontproperties = {"weight":"bold", "size":12},
fontsize=10,
)


# ────────────────────────────────────────────────
# ADJUST LAYOUT AND POSITION
# ────────────────────────────────────────────────
# Fine-tune the subplot layout to balance whitespace
fig.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.08)
pos = ax_pie.get_position()  # get current pie axis position
# Nudge the pie to the left/up to make space for summary box and legend
new_pos = [pos.x0 - 0.03, pos.y0 + 0.144, pos.width, pos.height]
ax_pie.set_position(new_pos)

# ────────────────────────────────────────────────
# SUMMARY BOX (BOTTOM LEFT)
# ────────────────────────────────────────────────
# Compute totals and percentages for the summary panel

outer_total = sum(outer_data.values())
percentages = {k: (v / outer_total) * 100 for k, v in outer_data.items()} if outer_total else {k: 0 for k in outer_data}
transfers_pct = round(percentages.get("Transfers", 0), 1)
others_pct = round(percentages.get("Others", 0), 1)
# Identify the peak spending month and its rounded value
month_map = {mt:fm for mt, fm in zip(monthly_totals.keys(), full_month)}
peak_month = max(monthly_totals, key=monthly_totals.get)
peak_month_fmt = month_map.get(peak_month, 0)
peak_value = round(monthly_totals[peak_month])
total_expenditure_fmt = f"{round(outer_total)}"

# Compose a human-readable summary paragraph shown on the figure
summary_text = (
    f"Expenditure Summary (May–Oct 2025)\n"
    f"Over the six-month period, total expenditure reached ₦{total_expenditure_fmt}, "
    f"with Transfers dominating at {transfers_pct}%.\n"
    f"Other categories accounted for {others_pct}%, covering data, airtime, and utilities.\n"
    f"Spending peaked in {peak_month_fmt} with ₦{peak_value} spent, "
    f"reflecting seasonal transfers and payments.\n"
    f"Overall, expenditure trends show consistent spending and balanced digital usage."
)

# Wrap the summary text so it fits nicely inside the figure text box
lines = summary_text.split("\n")
wrapped_summary = "\n".join([textwrap.fill(line, width=60) for line in lines])

# Place the summary text box at the bottom-left of the figure with a light background
fig.text(
    0.02, 0.09,
    wrapped_summary,
    fontsize=18,
    ha='left', va='bottom',
    wrap=True,
    color='#333333',
    weight='bold',
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="#f9f9f9",
        edgecolor="#cccccc",
        alpha=0.9,
    ),
)

# ────────────────────────────────────────────────
# FOOTER TEXT
# ────────────────────────────────────────────────
# Small footer credit centered near the bottom of the figure
fig.text(
    0.44, 0.04,
    "Visualized with Python — by Haashiraaa",
    fontsize=14,
    ha='center',
    va='center',
    wrap=True,
    color='gray',
    weight='bold',
)

# ────────────────────────────────────────────────
# Debug Summary
# ────────────────────────────────────────────────
# Display number of filtered desc
ic(f"No of Filtered transactions: {filtered_count}")
ic(peak_month_fmt)
# ────────────────────────────────────────────────
# THE FINAL VISUALIZATION
# ────────────────────────────────────────────────

# save_plot(fig, "SixMonths_trans.png") # Uncomment to save to current dir
plt.show()

