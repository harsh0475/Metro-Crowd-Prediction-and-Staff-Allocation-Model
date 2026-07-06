import pandas as pd

print("=" * 70)
print("AGGREGATING POST CODES TO BOOKING COUNTERS")
print("=" * 70)

# -------------------------------------------------------
# Read merged transaction data
# -------------------------------------------------------

df = pd.read_csv(
    "data/processed/merged_transactions.csv"
)

print("\nOriginal Rows :", len(df))

# -------------------------------------------------------
# Aggregate
# -------------------------------------------------------

booking_counter_df = (

    df.groupby(

        [

            "station",

            "booking_counter",

            "date",

            "hour"

        ],

        as_index=False

    )

    .agg(

        {

            "paper_qr": "sum",

            "card_issue": "sum",

            "card_recharge": "sum",

            "passengers": "sum"

        }

    )

)

# -------------------------------------------------------
# Sort
# -------------------------------------------------------

booking_counter_df = booking_counter_df.sort_values(

    [

        "station",

        "booking_counter",

        "date",

        "hour"

    ]

).reset_index(drop=True)

# -------------------------------------------------------
# Save
# -------------------------------------------------------

booking_counter_df.to_csv(

    "data/processed/booking_counter_transactions.csv",

    index=False

)

# -------------------------------------------------------
# Summary
# -------------------------------------------------------

print()

print("Aggregation Completed Successfully")

print()

print("Rows :", len(booking_counter_df))

print("Stations :", booking_counter_df["station"].nunique())

print("Booking Counters :", booking_counter_df["booking_counter"].nunique())

print()

print(booking_counter_df.head(20))

print()

print("Saved : data/processed/booking_counter_transactions.csv")

print("=" * 70)