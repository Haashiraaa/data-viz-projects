import matplotlib.pyplot as plt

# ------------------------------------
# Data Setup
# ------------------------------------
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Weekly steps for each user
steps = {
    'Alex': [8500, 9000, 12000, 10000, 9500, 13000, 12500],
    'Bree': [7000, 7500, 8200, 8800, 9100, 10000, 11000],
    'Carlos': [6000, 7200, 8000, 8500, 9000, 9500, 9700]
}

# Total calories burned per user
calories = {'Alex': 3500, 'Bree': 3100, 'Carlos': 2900}

# Average sleep hours per user
sleep_hours = {'Alex': 7.1, 'Bree': 6.8, 'Carlos': 8.0}

# Color palettes
tab_col = ("tab:blue", "tab:green", "tab:red")
bri_col = ("blue", "green", "red")

# ------------------------------------
# Figure Setup
# ------------------------------------
plt.style.use("seaborn-v0_8")
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=(19, 6),
    gridspec_kw={"width_ratios": [3, 3, 3]},
)

plt.suptitle("Fitness Tracker Dashboard", fontsize=24, weight="bold")

# ------------------------------------
# Line Plot — Daily Steps
# ------------------------------------
for user, color in zip(steps, bri_col):
    ax1.plot(days, steps[user], label=user, linewidth=2, marker="o", color=color)

ax1.set_title("Daily Steps", fontsize=18, weight='semibold')
ax1.set_xlabel("Days", fontsize=14, weight='semibold')
ax1.set_ylabel("Steps", fontsize=14, weight='semibold')
ax1.tick_params(labelsize=12)
ax1.set_xlim(-0.5, len(days) - 0.5)
ax1.margins(y=0.4)
ax1.legend(loc="upper left", fontsize=12)

# Annotation for maximum step achievement
ax1.annotate(
    'Alex Achieved Max Steps.\nDay 7 --> Saturday\nSteps --> 13k',
    xy=("Sat", 13000),
    xytext=("Wed", 14000),
    fontsize=12,
    weight='semibold',
    color='black',
    arrowprops=dict(arrowstyle='->', color='red', lw=2)
)

# ------------------------------------
# Bar Chart — Total Calories Burned
# ------------------------------------
x_positions = [i * 1.8 for i in range(len(calories))]


ax2.bar(
    x_positions,
    calories.values(),
    width=1,
    color=tab_col
)

ax2.set_xticks(x_positions)
ax2.set_xticklabels([f"{name.title()}\n(Mon–Sun)" for name in calories])

ax2.set_title("Total Calories Burned", fontsize=18, weight='semibold')
ax2.set_xlabel("Users", fontsize=14, weight='semibold')
ax2.set_ylabel("Calories", fontsize=14, weight='semibold')
ax2.tick_params(labelsize=12)
ax2.margins(y=0.15)

# Create legend manually using user names and colors
for name, color in zip(calories.keys(), tab_col):
    ax2.bar(0, 0, color=color, label=name)
ax2.legend(fontsize=12)

# ------------------------------------
# Pie Chart — Sleep Hours
# ------------------------------------
explode = (0, 0, 0.15)

x_values, y_values, percentages  = ax3.pie(
    sleep_hours.values(),
    labels=sleep_hours.keys(),
    autopct="%1.1f%%",
    colors=tab_col,
    startangle=90,
    shadow=True,
    explode=explode
)
ax3.axis('equal')  # Ensures pie is a circle
ax3.set_title("Average Sleep Time Distribution", fontsize=18, weight='semibold')
for value in y_values:
    value.set_fontweight('semibold')
    value.set_fontsize(15)
for percent in percentages:
    percent.set_fontweight('semibold')
    percent.set_fontsize(14)

ax3.legend()

# ------------------------------------
# Final Layout and Save
# ------------------------------------
fig.text(
    0.25,
    0.02,
    "All visualized data above represents cumulative results over one week.",
    ha='center',
    fontsize=12,
    color='black',
    style='italic',
    weight='bold'
)

plt.tight_layout()
""" 
Removing '#' from plt.savefig() enables 
saving to current directory
"""
# fig.savefig("fitness_tracker_dashboard.png")
plt.show()  # Show final dashboard image
