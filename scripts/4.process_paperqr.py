import pandas as pd

# -----------------------------
# Read Paper QR Sheet
# -----------------------------
paperqr = pd.read_excel(
    "data/raw/Passenger_Data.xlsx",
    sheet_name="PAPERQR"
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
paperqr["TERMINAL_CODE"] = (
    paperqr["TERMINAL_CODE"]
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
paperqr = paperqr.merge(
    master,
    left_on="TERMINAL_CODE",
    right_on="post_code",
    how="inner"
)

# -----------------------------
# Rename Columns
# -----------------------------
paperqr.rename(
    columns={
        "TXN_DATE": "date",
        "TXN_HOUR": "hour",
        "TXN_COUNT": "paper_qr"
    },
    inplace=True
)

# -----------------------------
# Keep Required Columns
# -----------------------------
paperqr = paperqr[
    [
        "station",
        "booking_counter",
        "post_code",
        "date",
        "hour",
        "paper_qr"
    ]
]

# -----------------------------
# Sort
# -----------------------------
paperqr = paperqr.sort_values(
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
paperqr.to_csv(
    "data/processed/paperqr.csv",
    index=False
)

print("PaperQR Processed Successfully")
print(paperqr.head())

print("\nRows :", len(paperqr))
print("Stations :", paperqr["station"].nunique())