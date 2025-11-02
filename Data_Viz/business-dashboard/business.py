"""
Business Dashboard: Monthly Sales Growth Visualization
------------------------------------------------------

This script generates a 4-panel business dashboard using Plotly.
The first subplot shows monthly sales growth with annotations for the
highest sales month (June). The visualization is exported as an HTML file.

Author: [Haashiraaa]
"""

# ==============================
#  Imports
# ==============================
import emoji
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


# ==============================
#  Data Setup
# ==============================
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12000, 18000, 15000, 22000, 26000, 30000]

# Customer satisfaction level (scale: 1–10)
cs_lvl = [7.2, 8.0, 7.8, 8.5, 9.0, 9.2]

# Advertising spend per month
ad_spend = [4000, 4200, 5000, 5200, 6000, 7000]

# Full month names for hover text
mon = ["January", "February", "March", "April", "May", "June"]

# Apply Plotly’s "ggplot2" template for consistent visual style
pio.templates.default = "ggplot2"


# ==============================
#  Create Subplots Layout
# ==============================
fig = make_subplots(
    horizontal_spacing=0.08,
    rows=1,
    cols=4,
    subplot_titles=[
        emoji.emojize(":chart_with_upwards_trend:<b>Monthly Sales Growth</b>", language="alias"),
        emoji.emojize(":moneybag:<b>Ad Spend by Month</b>", language="alias"),
        emoji.emojize(":smile:<b>Customer Satisfaction</b>", language="alias"),
        emoji.emojize(":doughnut:<b>Total Sales Percentage per Month</b>", language="alias"),
    ],
    specs=[[{"type": "xy"}, {"type": "xy"}, {"type": "xy"}, {"type": "domain"}]],
)


# ==============================
#  Hover Text Setup
# ==============================
# Each trace has its own hover text for rich interactivity.
plot1_text = [f"Month: {m}<br>Sales: ${s}" for m, s in zip(mon, sales)]
plot2_text = [f"Month: {m}<br>Ad expenses: ${ads}" for m, ads in zip(mon, ad_spend)]
plot3_text = [f"Satisfaction: {sl}<br>Sales: ${s}" for sl, s in zip(cs_lvl, sales)]
plot4_text = [f"Month: {m}<br>Total sales: ${s}" for m, s in zip(mon, sales)]


# ==============================
#  Subplot 1: Monthly Sales Growth (Line Plot)
# ==============================
fig.add_trace(
    go.Scatter(
        x=list(range(len(months))),
        y=sales,
        mode="lines+markers",
        name="Monthly Sales Growth",
        line=dict(color="rgb(102, 225, 0)", width=3),
        marker=dict(size=10, color="blue"),
        text=plot1_text,
        hovertemplate="<b>%{text}</b><extra></extra>",
    ),
    row=1,
    col=1,
)


# ==============================
#  Subplot 2: Ad Spend (Bar Chart)
# ==============================
fig.add_trace(
    go.Bar(
        x=list(range(len(months))),
        y=ad_spend,
        name="Ad Spend",
        marker_color="blue",
        text=plot2_text,
        textposition="none",  # hides text on bars
        hovertemplate="<b>%{text}</b><extra></extra>",
    ),
    row=1,
    col=2,
)


# ==============================
#  Subplot 3: Customer Satisfaction (Scatter Plot)
# ==============================
fig.add_trace(
    go.Scatter(
        x=[str(v) for v in cs_lvl],
        y=sales,
        mode="markers",
        name="Customer Satisfaction Level",
        marker=dict(size=10, color="rgb(255, 95, 0)"),
        text=plot3_text,
        hovertemplate="<b>%{text}</b><extra></extra>",
    ),
    row=1,
    col=3,
)


# ==============================
#  Subplot 4: Sales Distribution (Donut Chart)
# ==============================
fig.add_trace(
    go.Pie(
        labels=months,
        values=sales,
        textinfo="none",
        texttemplate="<b>%{label}</b><br>%{percent}",
        name="Monthly Sales Percentage",
        sort=False,
        direction="clockwise",
        hole=0.4,  # makes it a donut
        rotation=-23,  # controls starting angle
        text=plot4_text,
        textposition="inside",
        insidetextorientation="horizontal",
        hovertemplate="<b>%{text}</b><extra></extra>",
    ),
    row=1,
    col=4,
)


# ==============================
#  Axis Configuration
# ==============================

# --- X-Axis Setup ---
fig.update_xaxes(
    title="<b>Months</b>",
    range=[-1, len(months)],
    tickvals=list(range(len(months))),
    ticktext=months,
    row=1,
    col=1,
)

fig.update_xaxes(
    title="<b>Months</b>",
    range=[-1, len(months)],
    tickvals=list(range(len(months))),
    ticktext=months,
    row=1,
    col=2,
)

fig.update_xaxes(
    tickmode="array",
    tickvals=[str(v) for v in cs_lvl],
    ticktext=[str(v) for v in cs_lvl],
    range=[-1, len(cs_lvl)],
    title="<b>Customer Satisfaction Level<br>(scale: 1–10)</b>",
    row=1,
    col=3,
)

# --- Y-Axis Setup ---
# Reusable y-axis padding calculation for spacing
ymin, ymax = min(sales), max(sales)
padding = (ymax - ymin) * 0.27

fig.update_yaxes(
    title="<b>Sales ($)</b>",
    range=[ymin - padding, ymax + padding],
    row=1,
    col=1,
)

ymin, ymax = min(ad_spend), max(ad_spend)
padding = (ymax - ymin) * 0.27

fig.update_yaxes(
    title="<b>Ads Expenditure ($)</b>",
    range=[ymin - padding, ymax + padding],
    row=1,
    col=2,
)

ymin, ymax = min(sales), max(sales)
padding = (ymax - ymin) * 0.27

fig.update_yaxes(
    title="<b>Sales ($)</b>",
    range=[ymin - padding, ymax + padding],
    row=1,
    col=3,
)


# ==============================
#  Layout & Styling
# ==============================
fig.update_layout(
    showlegend=False,
    margin=dict(l=100, r=100, t=120, b=130),
    height=400,
    width=1300,
    title=dict(
        text=emoji.emojize(":bar_chart:<b>Business Dashboard Overview</b>", language="alias"),
        x=0.52,
        y=0.97,
        font=dict(size=24, color="black"),
    ),
    font=dict(size=12, family="Arial Black"),
    xaxis_title_font=dict(size=14, family="Arial Black"),
    yaxis_title_font=dict(size=14, family="Arial Black"),
)

# Update subplot title fonts for consistency
for ann in fig["layout"]["annotations"]:
    ann["font"] = dict(size=18, family="Arial Black", color="black")


# ==============================
#  Annotations
# ==============================

# Highlight peak sales (June)
fig.add_annotation(
    x=5,  # index for "Jun"
    y=30000,
    text=emoji.emojize(
        ":money_with_wings:<b>Sales peaked at $30k in June</b>",
        language="alias",
    ),
    font=dict(size=10),
    xref="x1",  # link to first subplot axes
    yref="y1",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=1.5,
    arrowcolor="red",
    ax=-80,
    ay=-20,
)

# Footer / subtitle annotation
fig.add_annotation(
    x=0.5,
    y=-0.8,
    text="<b>Data simulated for demonstration — created by Haashiraaa</b>",
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=14),
)


# ==============================
#  Save & Export
# ==============================
fig.write_html("business_dashboard_tracker.html")

print(emoji.emojize("Saved Successfully :white_check_mark:", language="alias"))
