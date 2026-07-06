import pandas as pd

print("=" * 60)
print("MERGING TRANSACTION DATA")
print("=" * 60)

# --------------------------------------------------
# Read Processed Files
# --------------------------------------------------

paperqr = pd.read_csv(
    "data/processed/paperqr.csv"
)

issue = pd.read_csv(
    "data/processed/card_issue.csv"
)

recharge = pd.read_csv(
    "data/processed/card_recharge.csv"
)

# --------------------------------------------------
# Convert Date Column
# --------------------------------------------------

paperqr["date"] = pd.to_datetime(paperqr["date"])

issue["date"] = pd.to_datetime(issue["date"])

recharge["date"] = pd.to_datetime(recharge["date"])

# --------------------------------------------------
# Merge PaperQR + Issue
# --------------------------------------------------

merged = pd.merge(

    paperqr,

    issue,

    on=[
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour"
    ],

    how="outer"

)

# --------------------------------------------------
# Merge Recharge
# --------------------------------------------------

merged = pd.merge(

    merged,

    recharge,

    on=[
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour"
    ],

    how="outer"

)

# --------------------------------------------------
# Replace Missing Values
# --------------------------------------------------

merged["paper_qr"] = merged["paper_qr"].fillna(0)

merged["card_issue"] = merged["card_issue"].fillna(0)

merged["card_recharge"] = merged["card_recharge"].fillna(0)

# --------------------------------------------------
# Convert to Integer
# --------------------------------------------------

merged["paper_qr"] = merged["paper_qr"].astype(int)

merged["card_issue"] = merged["card_issue"].astype(int)

merged["card_recharge"] = merged["card_recharge"].astype(int)

# --------------------------------------------------
# Total Passengers
# --------------------------------------------------

merged["passengers"] = (

    merged["paper_qr"]

    + merged["card_issue"]

    + merged["card_recharge"]

)

# --------------------------------------------------
# Sort Data
# --------------------------------------------------

merged = merged.sort_values(

    by=[

        "station",

        "booking_counter",

        "post_code",

        "date",

        "hour"

    ]

).reset_index(drop=True)

# --------------------------------------------------
# Save
# --------------------------------------------------

merged.to_csv(

    "data/processed/merged_transactions.csv",

    index=False

)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nMerge Completed Successfully\n")

print("Rows :", len(merged))

print("Stations :", merged["station"].nunique())

print("Booking Counters :", merged["booking_counter"].nunique())

print("Post Codes :", merged["post_code"].nunique())

print("\n")

print(merged.head(20))

print("\n")

print("Saved File : data/processed/merged_transactions.csv")

print("=" * 60)

# import pandas as pd

# df = pd.read_csv("data/processed/merged_transactions.csv")

# duplicates = df.duplicated(
#     subset=[
#         "station",
#         "booking_counter",
#         "post_code",
#         "date",
#         "hour"
#     ]
# ).sum()

# print("Duplicate Rows :", duplicates)
# print(df.isnull().sum())
# print(sorted(df["hour"].unique()))
# print(df["passengers"].describe())