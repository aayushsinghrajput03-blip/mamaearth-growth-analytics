# Mamaearth Growth Analytics

## Project Overview

This project analyzes Mamaearth's order data to understand revenue, customer orders, returns, and business risks.

The project has three stages:

1. SQL is used to create the database, load the raw data, and generate business reports.
2. Python is used to clean the data, analyze patterns, identify outliers, calculate return rates, and generate visualizations.
3. The verified Python findings are used to generate a Situation, Complication, and Resolution (SCR) business narrative.

Follow the steps below in order to reproduce the complete analysis.

## 1. SQL Analysis

Open MySQL Workbench.

### Step 1: Create the database tables

Open `sql/schema.sql` and run the complete file.

This creates three tables:

- `customers` — customer information
- `products` — product information
- `orders` — order information

### Step 2: Load the data

Open `sql/seed_data.sql` and run the complete file.

This loads the customer, product, and order data into the database.

The expected data counts are:

- 45 customers
- 16 products
- 180 orders

### Step 3: Generate SQL reports

Open `sql/reports.sql` and run the complete file.

This generates the required business reports, including revenue, order counts, customer spending, return rates, category performance, and loyalty tiers.

## 2. Python Analysis

The Python stage takes the raw CSV files from the `data` folder and performs the data cleaning and analysis required for the project.

### Step 1: Clean the data and perform analysis

Run:

    python analysis/clean_and_eda.py

This script:

- Loads the customer, product, and order CSV files.
- Checks the structure and quality of the data.
- Standardizes payment methods.
- Removes duplicate orders.
- Handles missing discounts and ratings.
- Calculates order values and total revenue.
- Detects unusual order quantities using the IQR method.
- Calculates return rates by payment method and customer city tier.
- Checks relationships between ratings, returns, discounts, and quantities.
- Calculates monthly revenue and identifies the true revenue peak after accounting for outliers.

At the end of the analysis, the verified findings are automatically saved to:

- narrator/findings.json

This JSON file passes the verified results from the Python analysis stage to the final GenAI narrative stage.

### Step 2: Generate visualizations

Run:

    python analysis/visualize.py

This script uses the cleaned analysis results to generate the required charts and saves them in:

    visualizations/

The generated charts are:

- `return_rate_by_payment.png`
- `monthly_revenue_trend.png`
  
## 3. GenAI Narrative

The final stage uses the verified findings from:

    narrator/findings.json

to generate a business narrative with three sections:

- Situation
- Complication
- Resolution

### Option A: Run with a Gemini API key

If you have a Gemini API key, set it as the `GEMINI_API_KEY` environment variable.

On Windows PowerShell, run:

    $env:GEMINI_API_KEY="YOUR_API_KEY"

Replace `YOUR_API_KEY` with your own Gemini API key.

Then run:

    python narrator/generate_narrative.py

Do not write or commit the API key into any project file or into GitHub.

### Option B: Run without an API key

An API key is not required.

Simply run:

    python narrator/generate_narrative.py

If no `GEMINI_API_KEY` is configured, the program automatically uses the deterministic offline fallback.

The offline fallback does not require an API key or network connection and generates the narrative directly from the verified findings.

## Complete Reproduction Order

Follow these steps from top to bottom to reproduce the complete project:

1. Run `sql/schema.sql`
2. Run `sql/seed_data.sql`
3. Run `sql/reports.sql`
4. Run `python analysis/clean_and_eda.py`
5. Confirm that `narrator/findings.json` has been created
6. Run `python analysis/visualize.py`
7. Run `python narrator/generate_narrative.py`

