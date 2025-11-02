# Expenditure Dashboard (May–Oct 2025)

A small script that reads cleaned bank CSV data and produces:
- a nested donut pie (Transfers vs Others + breakdown),
- a monthly expenditure bar chart (May–Oct 2025),
- a categorical expenditure bar chart,
- a summary panel on the figure.

Quick start
1. Clone the repository:
   ```bash
   git clone https://github.com/Haashiraaa/bank-sample-data.git
   cd bank-sample-data
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the helper modules and data are present:
   - Place `sample_cleaned_bank_data.csv` in the repository root.
   - Ensure `formatted_time.py` (with `normalize_date`) and `saver.py` (with `save_plot`) are importable.

Run the script
- To display the visualization:
  ```bash
  python my_bank_statement.py
  ```
- To save the figure instead of only showing it, uncomment or call:
  ```python
  save_plot(fig, "SixMonths_trans.png")
  ```
  inside `my_bank_statement.py` (the `saver` helper handles saving).

Inputs
- CSV must include headers: `Trans. Date`, `Description`, `Debit/Credit(₦)`.
- Negative numbers in `Debit/Credit(₦)` are treated as expenses (debits).

Quick config
- Toggle debug: set `DEBUG = True` at the top of `my_bank_statement.py`.
- Edit `filter_words` and `categories` to change filtering and classification.
- Update `month_labels` / `bar1_colors` if using a different date range.

Author
Haashiraaa — Visualized with Python