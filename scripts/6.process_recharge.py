import pandas as pd

# -----------------------------
# Read Card Recharge Sheet
# -----------------------------
card_recharge = pd.read_excel(
    "data/raw/Passenger_Data.xlsx",
    sheet_name="RECHARGE"
)

# -----------------------------
# Read Post Master
# -----------------------------
master = pd.read_excel(
    "data/master/post_master.xlsx"
)

# -----------------------------
# Clean Text Columns
# -----------------------------
card_recharge["TERMINAL_CODE"] = (
    card_recharge["TERMINAL_CODE"]
    .astype(str)
    .str.strip()
    .str.upper()
)

master["post_code"] = (
    master["post_code"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# -----------------------------
# Merge
# -----------------------------
card_recharge = card_recharge.merge(
    master,
    left_on="TERMINAL_CODE",
    right_on="post_code",
    how="inner"
)

# -----------------------------
# Rename Columns
# -----------------------------
card_recharge.rename(
    columns={
        "TXN_DATE": "date",
        "TXN_HOUR": "hour",
        "TXN_COUNT": "card_recharge"
    },
    inplace=True
)

# -----------------------------
# Keep Required Columns
# -----------------------------
card_recharge = card_recharge[
    [
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour",
        "card_recharge"
    ]
]

# -----------------------------
# Sort
# -----------------------------
card_recharge = card_recharge.sort_values(
    [
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour"
    ]
)

# -----------------------------
# Save
# -----------------------------
card_recharge.to_csv(
    "data/processed/card_recharge.csv",
    index=False
)

print("Card_Recharge Processed Successfully")
print(card_recharge.head())

print("\nRows :", len(card_recharge))
print("Stations :", card_recharge["station"].nunique())