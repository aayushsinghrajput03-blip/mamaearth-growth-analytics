import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================================================
# 1. FIND PROJECT / DATA PATHS
# =========================================================

if "__file__" in globals():
    # When running as analysis/visualize.py from GitHub
    BASE_DIR = Path(__file__).resolve().parents[1]
else:
    # When running this code directly in Google Colab
    BASE_DIR = Path.cwd()


# GitHub has data/ folder.
# In Colab, CSVs may be directly in the current folder.
if (BASE_DIR / "data").exists():
    DATA_DIR = BASE_DIR / "data"
else:
    DATA_DIR = BASE_DIR


customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")


# =========================================================
# 2. OUTPUT FOLDER
# =========================================================

OUTPUT_DIR = BASE_DIR / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================================================
# 3. CLEAN PAYMENT METHOD
# =========================================================

orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)


# =========================================================
# 4. REMOVE DUPLICATES
# =========================================================

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

orders = orders.drop_duplicates(
    subset=natural_key,
    keep="first"
).copy()


# =========================================================
# 5. IMPUTE MISSING VALUES
# =========================================================

orders["discount_pct"] = orders["discount_pct"].fillna(0)

orders["rating"] = orders["rating"].fillna(
    orders["rating"].median()
)


# =========================================================
# 6. MERGE ORDERS + PRODUCTS + CUSTOMERS
# =========================================================

df = orders.merge(
    products,
    on="product_id",
    how="left"
)

df = df.merge(
    customers,
    on="customer_id",
    how="left"
)


# =========================================================
# 7. CALCULATE ORDER VALUE
# =========================================================

df["order_value"] = (
    df["quantity"]
    * df["price"]
    * (1 - df["discount_pct"] / 100)
)


# =========================================================
# 8. IDENTIFY OUTLIERS USING IQR
# =========================================================

Q1 = df["quantity"].quantile(0.25)
Q3 = df["quantity"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df["is_outlier"] = (
    (df["quantity"] < lower_bound)
    | (df["quantity"] > upper_bound)
)


# =========================================================
# TASK 11 — VISUALIZATION 1
# RETURN RATE BY PAYMENT METHOD
# =========================================================

return_rates = (
    df.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    return_rates.index,
    return_rates.values
)


# Add exact percentage to every bar
for bar, value in zip(bars, return_rates.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )


# Calculate COD vs CARD multiple
cod_rate = return_rates["COD"]
card_rate = return_rates["CARD"]
cod_multiple = round(cod_rate / card_rate)


ax.set_xlabel("Payment Method")
ax.set_ylabel("Return Rate (%)")

ax.set_title(
    f"COD Returns at {cod_rate:.1f}% — {cod_multiple}x Card"
)

plt.tight_layout()


# Save required PNG
plt.savefig(
    OUTPUT_DIR / "return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()


# =========================================================
# TASK 11 — VISUALIZATION 2
# OUTLIER-CORRECTED MONTHLY REVENUE
# =========================================================

df["order_date"] = pd.to_datetime(
    df["order_date"]
)

df["year_month"] = (
    df["order_date"]
    .dt.to_period("M")
    .astype(str)
)


# IMPORTANT:
# Exclude ONLY the flagged outliers from the
# monthly revenue visualization.
monthly_revenue = (
    df[~df["is_outlier"]]
    .groupby("year_month")["order_value"]
    .sum()
    .round(2)
)


# Find actual peak month
peak_month = monthly_revenue.idxmax()


fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue")

ax.set_title(
    f"Monthly Revenue Trend — Actual Peak: {peak_month}"
)

plt.xticks(rotation=45)

plt.tight_layout()


# Save required PNG
plt.savefig(
    OUTPUT_DIR / "monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
plt.close()


# =========================================================
# VERIFICATION OUTPUT
# =========================================================

print("==========================================")
print("TASK 11 COMPLETED")
print("==========================================")

print("\nPayment method return rates:")
print(return_rates.round(1))

print("\nOutlier-corrected monthly revenue:")
print(monthly_revenue)

print("\nActual peak month:", peak_month)

print("\nFiles created:")

print(
    OUTPUT_DIR / "return_rate_by_payment.png"
)
print(
    OUTPUT_DIR / "monthly_revenue_trend.png"
)

print("\nBoth visualizations generated successfully.")
