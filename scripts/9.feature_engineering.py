import pandas as pd

print("=" * 70)
print("FEATURE ENGINEERING")
print("=" * 70)

# =====================================================
# Read Dataset
# =====================================================

df = pd.read_csv(
    "data/processed/booking_counter_transactions.csv"
)

# =====================================================
# Convert Date
# =====================================================

df["date"] = pd.to_datetime(df["date"])

# =====================================================
# Date Features
# =====================================================

df["year"] = df["date"].dt.year

df["month"] = df["date"].dt.month

df["day"] = df["date"].dt.day

df["day_name"] = df["date"].dt.day_name()

df["day_of_week"] = df["date"].dt.dayofweek

df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

df["quarter"] = df["date"].dt.quarter

df["is_weekend"] = (
    df["day_of_week"] >= 5
).astype(int)

df["is_month_start"] = (
    df["date"].dt.is_month_start
).astype(int)

df["is_month_end"] = (
    df["date"].dt.is_month_end
).astype(int)

# =====================================================
# Hour Range
# =====================================================

def hour_range(hour):

    end = (hour + 1) % 24

    def convert(h):

        if h == 0:
            return "12 AM"

        if h < 12:
            return f"{h} AM"

        if h == 12:
            return "12 PM"

        return f"{h-12} PM"

    return f"{convert(hour)} - {convert(end)}"

df["hour_range"] = df["hour"].apply(hour_range)

# =====================================================
# Shift
# =====================================================

def shift(hour):

    if hour <= 14:
        return "Morning"

    return "Evening"

df["shift"] = df["hour"].apply(shift)

# =====================================================
# Time Slot
# =====================================================

def time_slot(hour):

    if 6 <= hour <= 8:
        return "Early Morning"

    elif 9 <= hour <= 11:
        return "Morning Peak"

    elif 12 <= hour <= 15:
        return "Afternoon"

    elif 16 <= hour <= 19:
        return "Evening Peak"

    return "Night"

df["time_slot"] = df["hour"].apply(time_slot)

# =====================================================
# Peak Hour
# =====================================================

def peak(hour):

    if hour in [7,8,9,10,17,18,19,20]:
        return 1

    return 0

df["peak_hour"] = df["hour"].apply(peak)

# =====================================================
# Festival Placeholder
# =====================================================

df["festival"] = "None"

# =====================================================
# Reorder Columns
# =====================================================

df = df[

[
    "station",
    "booking_counter",

    "date",

    "year",
    "quarter",
    "month",
    "week_of_year",
    "day",
    "day_name",
    "day_of_week",

    "is_weekend",
    "is_month_start",
    "is_month_end",

    "hour",
    "hour_range",
    "shift",
    "time_slot",
    "peak_hour",

    "festival",

    "paper_qr",
    "card_issue",
    "card_recharge",

    "passengers"
]

]

# =====================================================
# Sort
# =====================================================

df = df.sort_values(

[
    "station",
    "booking_counter",
    "date",
    "hour"
]

).reset_index(drop=True)

# =====================================================
# Save
# =====================================================

df.to_csv(

    "data/features/final_dataset.csv",

    index=False

)

# =====================================================
# Summary
# =====================================================

print()

print("Feature Engineering Completed")

print()

print("Rows :",len(df))

print("Stations :",df["station"].nunique())

print("Booking Counters :",df["booking_counter"].nunique())

print()

print(df.head())

print()

print("Saved : data/features/final_dataset.csv")

print("=" * 70)