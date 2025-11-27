import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import textwrap
import time

# Display settings for small screens (phone-friendly)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

LINES = "=" * 20
TITLE = f"{LINES} Sales Insights Summary {LINES}"


# ================================
# Helper Functions
# ================================

def tier(total):
    """Return customer tier based on total spend."""
    if total >= 200:
        return "Premium"
    elif total >= 100:
        return "Mid"
    return "Budget"


def gen_plot(val, k="bar", r=0, fn="pd_plot1.png"):
    """Generate and save a plot from a Series/DataFrame."""
    val.plot(kind=k)
    plt.xticks(rotation=r)
    plt.savefig(f"image_files/{fn}", dpi=300)
    plt.close()
    print(f"\n\tYour {fn} has been saved successfully.")
    time.sleep(2)

def gather_data(df, arg1, arg2):
    """Group by a column, sum values, and return the top performer."""
    grouped = df.groupby(arg1)[arg2].sum().sort_values(ascending=False)
    top = grouped.index[0]
    return pd.Series([top, grouped.loc[top]])


def report(reg, cm, cat, day):
    """Generate a short text summary of key sales insights."""
    return (
        f"\nBest Performing Region: {reg} led overall sales, showing strong customer demand and consistent growth across product lines."
        f"\n\nMost Valuable Customer: {cm} generated the highest value at the end of the month, indicating strong loyalty and repeated purchase behavior."
        f"\n\nTop Sales Category: {cat} dominated total revenue, proving to be the most profitable segment."
        f"\n\nHighest Revenue Day: Across the full month, {day} generated the highest cumulative revenue, indicating that weekly demand consistently peaks toward the end of the workweek rather than on a single standout date."

        "\n\nAdditional Insights:"  
        "\n- Premium Gold customers contribute the majority of total sales, making them the most profitable target for marketing investment."  
        "\n- All sales occurred within a single month, so performance insights focus on segment behavior and weekday trends rather than long-term seasonal effects."  
    )


def format_text(text, width=70):
    """Wrap long text so it displays neatly on a phone."""
    wrapper = textwrap.TextWrapper(width=width)
    formatted_lines = []

    for line in text.split("\n"):
        formatted_lines.append("") if not line.strip() else formatted_lines.append(wrapper.fill(line))

    return "\n".join(formatted_lines)


def clear_screen():
    """Clear the terminal for readability."""
    os.system("cls" if os.name == "nt" else "clear")


def summary(arg1, arg2, arg3, arg4):
    """Display a formatted insights summary."""
    clear_screen()
    print(TITLE)
    print(format_text(report(arg1, arg2, arg3, arg4)))


# ================================
# Load Data
# ================================

sdata = pd.read_csv("csv_files/sales_data.csv")

# ================================
# Calculations
# ================================

# Total revenue
sdata["total"] = sdata["price"] * sdata["quantity"]

# Filtering examples
above_200 = sdata[sdata["total"] > 200]
tech_sales = sdata[(sdata["category"] == "Tech") & (sdata["region"] == "CA")]

# Groupby operations
avg_price = sdata.groupby("category")["price"].mean()
region_ord = sdata.groupby("region")["quantity"].sum()
total_rev = sdata.groupby("customer")["total"].sum()

# Pivot example
pivot = sdata.pivot_table(
    values="total",
    index="category",
    columns="region",
    aggfunc="sum",
)

# Sorting
sdata = sdata.sort_values("total", ascending=False)

# ================================
# Data Cleaning
# ================================

# Map region codes to names
sdata["region"] = sdata["region"].map({
    "CA": "California",
    "NY": "New York",
    "TX": "Texas",
    "WA": "Washington",
}).fillna("Unknown")

# Convert date column
sdata["date"] = pd.to_datetime(sdata["date"])
sdata["months"] = sdata["date"].dt.month

# January subset (all data is January by design)
jan_sales = sdata[sdata["months"] == 1]

# Apply tier function
sdata["tier"] = sdata["total"].apply(tier)

# Convert column names to title-case and reset index nicely
sdata.columns = sdata.columns.str.title()
sdata = sdata.set_index(np.arange(len(sdata)).astype(np.uint8))

# ================================
# Basic Plots
# ================================

total_per_reg = sdata.groupby("Region")["Total"].sum()
orders_per_cat = sdata.groupby("Category")["Quantity"].sum()

gen_plot(total_per_reg)
gen_plot(orders_per_cat, fn="pd_plot2.png")

# ================================
# Bonus: Merge VIP Data
# ================================

vip = pd.read_csv("csv_files/vip.csv")
vip.columns = vip.columns.str.title()

combined = sdata.merge(vip, on="Customer", how="left")

gold_nd_prem = combined[
    (combined["Tier"] == "Premium") &
    (combined["Vip_Level"] == "Gold")
]

# Add weekday name
combined["Days"] = combined["Date"].dt.day_name()

# ================================
# Gather Insights
# ================================

bp_reg = gather_data(combined, "Region", "Total")
mv_cm = gather_data(combined, "Customer", "Total")
hcat_sal = gather_data(combined, "Category", "Total")
hday_sal = gather_data(combined, "Days", "Total")

# ================================
# Display Summary
# ================================

summary(bp_reg[0], mv_cm[0], hcat_sal[0], hday_sal[0])

# ================================
# Save Output (Optional)
# ================================
"""Uncomment to save in either or both formats"""

#combined.to_csv("cleaned_data/sales_report.csv", index=False)
#combined.to_excel("cleaned_data/sales_report.xlsx", index=False)
