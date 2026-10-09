import pandas as pd
import json
from pathlib import Path

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
NARRATOR_DIR = BASE_DIR / "narrator"

NARRATOR_DIR.mkdir(exist_ok=True)

# ============================================================
# TASK 1 - LOAD AND INSPECT DATA
# ============================================================

customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
raw_orders = pd.read_csv(DATA_DIR / "orders.csv")

print("TASK 1 - DATA INSPECTION")
print("Customers shape:", customers.shape)
print("Products shape:", products.shape)
print("Orders shape:", raw_orders.shape)

# Keep raw data untouched for reconciliation
orders = raw_orders.copy()

# ============================================================
# RAW REVENUE - USED LATER FOR RECONCILIATION
# ============================================================

raw_revenue_df = orders.merge(
    products,
    on="product_id",
    how="left"
)

raw_revenue_df["discount_pct"] = raw_revenue_df["discount_pct"].fillna(0)

raw_revenue_df["order_value"] = (
    raw_revenue_df["quantity"]
    * raw_revenue_df["price"]
    * (1 - raw_revenue_df["discount_pct"] / 100)
)

raw_total_revenue = round(raw_revenue_df["order_value"].sum(), 2)

# ============================================================
# TASK 2 - STANDARDIZE PAYMENT METHOD
# ============================================================

print("\nTASK 2 - PAYMENT METHOD CLEANING")

print("Before cleaning:")
print(orders["payment_method"].unique())

orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

print("After cleaning:")
print(orders["payment_method"].unique())

print(orders["payment_method"].value_counts())

# ============================================================
# TASK 3 - REMOVE DUPLICATES
# ============================================================

print("\nTASK 3 - DUPLICATE REMOVAL")

natural_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

duplicate_mask = orders.duplicated(
    subset=natural_key,
    keep="first"
)

print("Duplicate order IDs:")
print(orders.loc[duplicate_mask, "order_id"].tolist())

orders_clean = orders.loc[~duplicate_mask].copy()

print("Before:", orders.shape)
print("After:", orders_clean.shape)

# ============================================================
# TASK 4 - HANDLE MISSING VALUES
# ============================================================

print("\nTASK 4 - MISSING VALUES")

orders_clean["discount_pct"] = orders_clean["discount_pct"].fillna(0)

rating_median = orders_clean["rating"].median()
print("Rating median:", rating_median)

orders_clean["rating"] = orders_clean["rating"].fillna(rating_median)

print("Remaining missing values:")
print(orders_clean[["discount_pct", "rating"]].isnull().sum())

# ============================================================
# TASK 5 - MERGE DATASETS AND CALCULATE ORDER VALUE
# ============================================================

print("\nTASK 5 - MERGE AND ORDER VALUE")

orders_merged = orders_clean.merge(
    products,
    on="product_id",
    how="left"
)

orders_merged = orders_merged.merge(
    customers,
    on="customer_id",
    how="left"
)

orders_merged["order_value"] = (
    orders_merged["quantity"]
    * orders_merged["price"]
    * (1 - orders_merged["discount_pct"] / 100)
)

cleaned_total_revenue = round(
    orders_merged["order_value"].sum(),
    2
)

duplicate_reconciliation_delta = round(
    raw_total_revenue - cleaned_total_revenue,
    2
)

print("Raw total revenue:", raw_total_revenue)
print("Cleaned total revenue:", cleaned_total_revenue)
print("Duplicate reconciliation delta:", duplicate_reconciliation_delta)

# ============================================================
# TASK 6 - IQR OUTLIER DETECTION
# ============================================================

print("\nTASK 6 - IQR OUTLIERS")

Q1 = orders_merged["quantity"].quantile(0.25)
Q3 = orders_merged["quantity"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

orders_merged["is_outlier"] = (
    (orders_merged["quantity"] < lower_bound)
    | (orders_merged["quantity"] > upper_bound)
)

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

print(
    orders_merged.loc[
        orders_merged["is_outlier"],
        ["order_id", "quantity", "is_outlier"]
    ]
)

# ============================================================
# TASK 7 - PAYMENT METHOD RETURN RATE
# ============================================================

print("\nTASK 7 - RETURN RATE BY PAYMENT METHOD")

return_rates = (
    orders_merged
    .groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .round(1)
)

print(return_rates)

# ============================================================
# TASK 8 - MULTI-LEVEL SEGMENTATION
# ============================================================

print("\nTASK 8 - PAYMENT METHOD + CITY TIER")

segment_rates = (
    orders_merged
    .groupby(["payment_method", "city_tier"])["returned"]
    .agg(["count", "mean"])
)

segment_rates["return_rate_pct"] = (
    segment_rates["mean"] * 100
).round(1)

print(segment_rates[["count", "return_rate_pct"]])

highest_risk_segment = segment_rates["return_rate_pct"].idxmax()
highest_risk_rate = float(
    segment_rates["return_rate_pct"].max()
)

print(
    "Highest-risk segment:",
    highest_risk_segment,
    "at",
    highest_risk_rate,
    "%"
)

# ============================================================
# TASK 9 - CORRELATION ANALYSIS
# ============================================================

print("\nTASK 9 - CORRELATION MATRIX")

corr_columns = [
    "rating",
    "returned",
    "discount_pct",
    "quantity"
]

corr_matrix = orders_merged[corr_columns].corr()

print(corr_matrix.round(2))

def correlation_strength(r):
    absolute_r = abs(r)

    if absolute_r < 0.2:
        return "negligible"
    elif absolute_r < 0.4:
        return "weak"
    elif absolute_r < 0.7:
        return "moderate"
    else:
        return "strong"

pairs = [
    ("rating", "returned"),
    ("rating", "discount_pct"),
    ("rating", "quantity"),
    ("returned", "discount_pct"),
    ("returned", "quantity"),
    ("discount_pct", "quantity")
]

print("\nPairwise interpretation:")

for col1, col2 in pairs:
    r = corr_matrix.loc[col1, col2]

    print(
        f"{col1} vs {col2}: "
        f"r = {r:.2f} → "
        f"{correlation_strength(r)}"
    )

discount_return_r = corr_matrix.loc[
    "discount_pct",
    "returned"
]

if abs(discount_return_r) < 0.2:
    print(
        "\nHypothesis: Higher discounts reduce returns → "
        f"Busted (r = {discount_return_r:.2f})"
    )

# ============================================================
# TASK 10 - MONTHLY REVENUE TREND
# ============================================================

print("\nTASK 10 - MONTHLY REVENUE")

orders_merged["order_date"] = pd.to_datetime(
    orders_merged["order_date"]
)

orders_merged["year_month"] = (
    orders_merged["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_with_outliers = (
    orders_merged
    .groupby("year_month")["order_value"]
    .sum()
    .round(2)
)

monthly_without_outliers = (
    orders_merged[~orders_merged["is_outlier"]]
    .groupby("year_month")["order_value"]
    .sum()
    .round(2)
)

print("Monthly revenue including outliers:")
print(monthly_with_outliers)

print("\nMonthly revenue excluding outliers:")
print(monthly_without_outliers)

true_peak_month = monthly_without_outliers.idxmax()
outlier_inflated_month = monthly_with_outliers.idxmax()

print(
    "\nTrue peak month:",
    true_peak_month
)

print(
    "Outlier-inflated month:",
    outlier_inflated_month
)

# ============================================================
# PART 3 - TASK 1
# GENERATE narrator/findings.json
# ============================================================

findings = {
    "cleaned_total_revenue_inr": cleaned_total_revenue,

    "raw_total_revenue_inr": raw_total_revenue,

    "duplicate_reconciliation_delta_inr":
        duplicate_reconciliation_delta,

    "return_rate_by_payment": {
        "COD": float(return_rates["COD"]),
        "CARD": float(return_rates["CARD"]),
        "UPI": float(return_rates["UPI"])
    },

    "highest_risk_segment": {
        "payment_method": highest_risk_segment[0],
        "city_tier": int(highest_risk_segment[1]),
        "return_rate_pct": highest_risk_rate
    },

    "true_peak_month": {
        "month": true_peak_month,
        "revenue_inr": float(
            monthly_without_outliers[true_peak_month]
        )
    },

    "outlier_inflated_month": {
        "month": outlier_inflated_month,
        "apparent_revenue_inr": float(
            monthly_with_outliers[outlier_inflated_month]
        ),
        "corrected_revenue_inr": float(
            monthly_without_outliers[outlier_inflated_month]
        )
    }
}

findings_path = NARRATOR_DIR / "findings.json"

with open(findings_path, "w", encoding="utf-8") as file:
    json.dump(findings, file, indent=4)

print("\n======================================")
print("TASK 1 COMPLETED")
print("findings.json created at:")
print(findings_path)
print("======================================")


