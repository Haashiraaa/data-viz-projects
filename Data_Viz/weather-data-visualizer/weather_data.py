"""
Weather Data Visualization
--------------------------
This script reads weather data from a CSV file and visualizes
daily high and low temperatures using Matplotlib.
"""

from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from icecream import ic
from saver import save_plot

# -----------------------------------------------------
# Debug Configuration
# -----------------------------------------------------
DEBUG = False
if not DEBUG:
    ic.disable()
else:
    ic.enable()

# -----------------------------------------------------
# Initialize Tracking Lists
# -----------------------------------------------------
error_data = []      # Track rows with missing or invalid data
all_instance = []    # Store all station name occurrences

# -----------------------------------------------------
# Read and Parse CSV File
# -----------------------------------------------------
path = Path('4150697.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)  # Skip header row

# Initialize Data Containers
dates, highs, lows = [], [], []

# -----------------------------------------------------
# Extract Temperature Data
# -----------------------------------------------------
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')

    try:
        high = int(row[4])
        low = int(row[5])
    except ValueError:
        # Debug missing data when DEBUG = True
        ic(f"Missing data for {current_date}.")
        error_data.append(current_date)
    else:
        dates.append(current_date)
        highs.append(high)
        lows.append(low)
        all_instance.append(row[1])

# -----------------------------------------------------
# Hacky Method to Auto-Extract Station Name
# -----------------------------------------------------
# Convert the list of repeated station names into a unique set.
# This avoids hardcoding the station name manually.
set_data = set(all_instance)
station_name = [name for name in set_data]
ic(station_name)

# -----------------------------------------------------
# Plot Configuration
# -----------------------------------------------------
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(14, 8))

# Plot temperature lines and shaded area
ax.plot(dates, highs, color='red', alpha=0.5, label="High")
ax.plot(dates, lows, color='blue', alpha=0.5, label="Low")
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

# -----------------------------------------------------
# Legend Configuration
# -----------------------------------------------------
# Create a legend with a bold title and customized label style.
ax.legend(
    title="Temperature Category",
    title_fontproperties={"weight": "bold", "size": 16},
    prop={'size': 12, 'weight': 'bold'}
)

# -----------------------------------------------------
# Axis and Title Settings
# -----------------------------------------------------
ax.margins(x=0.1, y=0.2)
ax.set_title(
    f"Daily High Temperatures, 2024/2025\n{station_name[0]}",
    fontsize=24,
    weight='bold'
)
ax.set_xlabel("")  # Empty because dates on x-axis are self-explanatory
ax.set_ylabel("Temperature (°F)", fontsize=20, weight='bold')

fig.autofmt_xdate()  # Rotate x-ticks for better readability
ax.tick_params(labelsize=16)

# -----------------------------------------------------
# Debug Summary (Optional)
# -----------------------------------------------------
if error_data:
    """
    Enable DEBUG to view missing-data summary.
    Lists how many rows were skipped due to missing values.
    """
    ic(f"\nSkipped {len(error_data)} rows due to missing data.")


# -----------------------------------------------------
# User Interaction: View or Save Plot
# -----------------------------------------------------
# Prompt the user to either display the plot or save it as an image file.
# This section allows flexibility when running the script from a terminal.
try:
    choice = input("Would you like to view or save the plot? (v/s): ").strip().lower()

    if choice == 'v':
        plt.show()
    elif choice == 's':
        save_plot(fig, "weather_data.png")
    else:
        print("\nInvalid input. The plot will not be displayed or saved.")
except EOFError:
    # Handle EOFError (common in mobile environments like PyDroid)
    # This ensures the program doesn't crash when `input()` fails due to no standard input stream.
    # It provides a graceful fallback so the script can default to "view plot" without breaking.
    plt.show()
