# Mamaearth Growth Analytics

## Project Overview

This project analyzes Mamaearth's order data to understand revenue, customer orders, returns, and business risks.

The project has three stages:

1. **SQL Analysis:** Create the database tables, load the raw data, and generate business reports.
2. **Python Analysis:** Clean the data, perform exploratory data analysis (EDA), identify outliers, calculate return rates, and generate visualizations.
3. **GenAI Narrative:** Use verified Python findings to generate a Situation, Complication, and Resolution (SCR) business narrative.

Follow the instructions below in order to reproduce the complete project.

## 1. SQL Analysis

### Prerequisite

Open MySQL Workbench and connect to your MySQL server. Select or create the database you intend to use before executing the SQL scripts.

### Step 1: Create the database tables

Open `sql/schema.sql` in MySQL Workbench and execute the complete file.

This creates three tables:

- `customers` — customer information
- `products` — product information
- `orders` — order information

### Step 2: Load the data

Open `sql/seed_data.sql` and execute the complete file.

This loads the customer, product, and order records into the database.

Verify that the tables contain the expected number of records:

- Customers: 45
- Products: 16
- Orders: 180

### Step 3: Generate SQL reports

Open `sql/reports.sql` and execute the required queries.

This generates the business reports covering revenue, order counts, customer spending, return rates, category performance, and customer loyalty tiers.

**Important:** If you are rerunning the scripts against an existing database, check whether the tables or the `loyalty_tier` column already exist before executing the schema and reporting scripts again.

## 2. Python Analysis

The Python stage uses the raw CSV files in the `data/` folder. It performs data cleaning, exploratory analysis, and the calculations required for the project.

### Step 1: Prepare the Python environment

Make sure Python is installed on your system.

For the standard workflow, use VS Code or a terminal:

1. Open or extract the complete project repository.
2. Open the main project folder containing `README.md`, `analysis/`, `data/`, `sql/`, and `narrator/`.
3. Open a terminal in that main project folder.
4. Install the required Python dependencies before running the scripts.

If the repository contains a `requirements.txt` file, install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

**Important:** Run the commands below from the main project folder, not from inside the `analysis/` or `narrator/` folders.

Run the `.py` files as Python scripts. Do not copy and paste the entire contents of a script into a notebook cell, because the scripts may rely on their file paths and the project's folder structure.

### Step 2: Clean the data and perform EDA

Run:

```bash
python analysis/clean_and_eda.py
```

This script:

- Loads the customer, product, and order CSV files.
- Checks the structure and quality of the data.
- Standardizes payment methods.
- Removes duplicate orders.
- Handles missing discounts and ratings.
- Calculates order values and total revenue.
- Detects unusual order quantities using the IQR method.
- Calculates return rates by payment method and customer city tier.
- Examines relationships between ratings, returns, discounts, and quantities.
- Calculates monthly revenue and identifies the true revenue peak after accounting for outliers.

At the end of the analysis, the verified findings are automatically saved to:

`narrator/findings.json`

This JSON file passes the verified results from the Python analysis stage to the GenAI narrative stage. Run this script before generating the visualizations or the narrative.

### Step 3: Generate visualizations

Run:

```bash
python analysis/visualize.py
```

This script generates the required charts using the project data and the analysis and outlier-handling logic implemented in the script.

The charts are saved in the `visualizations/` folder:

- `return_rate_by_payment.png`
- `monthly_revenue_trend.png`

After execution, confirm that both files exist in the folder.

### Running in Google Colab

Google Colab can also be used, but the complete project folder and its directory structure must be available in the notebook environment.

1. Upload or clone the complete repository into Colab.
2. Set the working directory to the main project folder containing `README.md`.
3. Ensure the required Python dependencies are installed.
4. Run the Python scripts as files in the same order shown above, rather than pasting their entire source code into notebook cells.

This matters because `__file__` is normally available when Python runs a `.py` file, but is not defined in a standard notebook cell. Pasting the script directly into a cell may therefore cause a `NameError`.

## 3. GenAI Narrative

The final stage uses the verified findings in:

`narrator/findings.json`

to generate a business narrative with three sections:

- Situation
- Complication
- Resolution

**Prerequisite:** Run `analysis/clean_and_eda.py` first so that `narrator/findings.json` exists and contains the latest findings.

### Option A: Run with a Gemini API key

If you have a Gemini API key, set it as the `GEMINI_API_KEY` environment variable.

In Windows PowerShell, run:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your own Gemini API key.

Then run the narrative script from the project root:

```bash
python narrator/generate_narrative.py
```

Do not hard-code or commit your API key into any project file or GitHub repository.

### Option B: Run without an API key

An API key is not required to run the project.

From the project root, run:

```bash
python narrator/generate_narrative.py
```

If `GEMINI_API_KEY` is not configured, the program automatically uses the deterministic offline fallback.

The offline fallback does not require an API key or network connection. It generates the narrative directly from the verified findings.

The script also checks five required numerical findings and prints `FINAL CHECK: PASS` when all five checks pass.

## 4. Complete Reproduction Order

Follow these steps from top to bottom to reproduce the complete project:

1. Execute `sql/schema.sql` in MySQL Workbench.
2. Execute `sql/seed_data.sql` in MySQL Workbench.
3. Execute the required queries in `sql/reports.sql`.
4. From the project root, run `python analysis/clean_and_eda.py`.
5. Confirm that `narrator/findings.json` has been generated or refreshed.
6. Run `python analysis/visualize.py`.
7. Confirm that both required PNG files exist in `visualizations/`.
8. Run `python narrator/generate_narrative.py`.
9. Verify that the narrative is generated and the numerical accuracy check prints `FINAL CHECK: PASS`.

## Expected Project Outputs

After completing the workflow, the repository should contain:

- `narrator/findings.json` — verified analytical findings generated by the Python analysis.
- `visualizations/return_rate_by_payment.png` — return-rate comparison by payment method.
- `visualizations/monthly_revenue_trend.png` — outlier-corrected monthly revenue trend.
- The generated SCR narrative and its numerical validation results, printed by `narrator/generate_narrative.py`.

The SQL scripts produce their reports in MySQL Workbench. The Python scripts generate the analysis outputs, visualizations, and narrative as described above.
