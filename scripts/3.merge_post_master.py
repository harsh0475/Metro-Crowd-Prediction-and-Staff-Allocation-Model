import pandas as pd

# -----------------------------
# Read all three master files
# -----------------------------
paperqr = pd.read_excel(
    "data/master/all_post_code_PaperQR.xlsx"
)

issue = pd.read_excel(
    "data/master/all_post_code_Issue.xlsx"
)

recharge = pd.read_excel(
    "data/master/all_post_code_Recharge.xlsx"
)

# -----------------------------
# Function to clean text columns
# -----------------------------
def clean_text(df):

    # Keep post_code and station in uppercase
    for col in ["post_code", "station"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.upper()
        )

    # Keep booking_counter exactly as written
    df["booking_counter"] = (
        df["booking_counter"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    return df


paperqr = clean_text(paperqr)
issue = clean_text(issue)
recharge = clean_text(recharge)

# -----------------------------
# Add source column (optional)
# -----------------------------
paperqr["source"] = "PAPERQR"
issue["source"] = "ISSUE"
recharge["source"] = "RECHARGE"

# -----------------------------
# Merge all data
# -----------------------------
master = pd.concat(
    [paperqr, issue, recharge],
    ignore_index=True
)

stations_to_check = ["KBCR", "KBBR", "KTRT", "KKSK", "KSKB", "KTKP"]

for station in stations_to_check:
    print(f"\n===== {station} =====")
    print(master[master["station"] == station][
        ["post_code", "station", "booking_counter", "source"]
    ])

# -----------------------------
# Check for conflicts
# -----------------------------
conflicts = (
    master.groupby("post_code")["booking_counter"]
    .nunique()
)

conflict_codes = conflicts[conflicts > 1]

if len(conflict_codes) > 0:

    print("\nBooking Counter Conflicts Found:\n")

    print(
        master[
            master["post_code"].isin(
                conflict_codes.index
            )
        ].sort_values(
            ["post_code", "source"]
        )
    )

else:

    print("\nNo booking counter conflicts found.")

# -----------------------------
# Remove duplicate post codes
# -----------------------------
master = (
    master
    .drop_duplicates(subset="post_code")
    .sort_values(
        ["station", "booking_counter", "post_code"]
    )
    .reset_index(drop=True)
)

# Remove source column
master = master.drop(columns="source")

# -----------------------------
# Save Master
# -----------------------------
master.to_excel(
    "data/master/post_master.xlsx",
    index=False
)

# -----------------------------
# Summary
# -----------------------------
print("\n========== SUMMARY ==========")

print(
    "Total Stations :",
    master["station"].nunique()
)

print(
    "Total Booking Counters :",
    master["booking_counter"].nunique()
)

print(
    "Total Post Codes :",
    len(master)
)

print("\nMaster file created successfully!")

print("\nFirst 20 rows:\n")

print(master.head(20))

stations = sorted(master["station"].unique())

for station in stations:
    print(station)

# import pandas as pd

# # Read Metro Route
# route = pd.read_excel("data/raw/Metro_Route.xlsx")

# # Read Post Master
# master = pd.read_excel("data/master/post_master.xlsx")

# # Clean column names
# route.columns = route.columns.str.strip()
# master.columns = master.columns.str.strip()

# # Clean station codes
# route["Station Code"] = (
#     route["Station Code"]
#     .astype(str)
#     .str.strip()
#     .str.upper()
# )

# master["station"] = (
#     master["station"]
#     .astype(str)
#     .str.strip()
#     .str.upper()
# )

# route_stations = set(route["Station Code"].unique())
# master_stations = set(master["station"].unique())

# print("Stations in Route :", len(route_stations))
# print("Stations in Master:", len(master_stations))

# print("\nMissing in Master:")
# print(sorted(route_stations - master_stations))

# print("\nExtra in Master:")
# print(sorted(master_stations - route_stations))

