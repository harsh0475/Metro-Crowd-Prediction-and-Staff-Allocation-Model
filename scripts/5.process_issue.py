import pandas as pd

# -----------------------------
# Read Card Issue Sheet
# -----------------------------
card_issue = pd.read_excel(
    "data/raw/Passenger_Data.xlsx",
    sheet_name="ISSUE"
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
card_issue["TERMINAL_CODE"] = (
    card_issue["TERMINAL_CODE"]
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
card_issue = card_issue.merge(
    master,
    left_on="TERMINAL_CODE",
    right_on="post_code",
    how="inner"
)

# -----------------------------
# Rename Columns
# -----------------------------
card_issue.rename(
    columns={
        "TXN_DATE": "date",
        "TXN_HOUR": "hour",
        "TXN_COUNT": "card_issue"
    },
    inplace=True
)

# -----------------------------
# Keep Required Columns
# -----------------------------
card_issue = card_issue[
    [
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour",
        "card_issue"
    ]
]

# -----------------------------
# Sort
# -----------------------------
card_issue = card_issue.sort_values(
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
card_issue.to_csv(
    "data/processed/card_issue.csv",
    index=False
)

print("Card_Issue Processed Successfully")
print(card_issue.head())

print("\nRows :", len(card_issue))
print("Stations :", card_issue["station"].nunique())