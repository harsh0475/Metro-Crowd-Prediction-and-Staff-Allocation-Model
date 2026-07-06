import joblib
import pandas as pd
import math

from datetime import datetime

# =====================================================
# LOAD MODEL
# =====================================================

print("Loading XGBoost Model...")

MODEL = joblib.load(
    "models/xgboost_model.pkl"
)

print("Loading Encoder...")

ENCODER = joblib.load(
    "models/ordinal_encoder.pkl"
)

print("Loading Feature Columns...")

FEATURE_COLUMNS = joblib.load(
    "models/feature_columns.pkl"
)

# =====================================================
# LOAD ROUTE DATA
# =====================================================

ROUTE = pd.read_excel(
    "data/raw/Metro_Route.xlsx"
)

ROUTE.columns = ROUTE.columns.str.strip()

ROUTE = ROUTE.rename(columns={

    "Station Code": "station",

    "Station Name": "station_name",

    "Line": "line",

    "Sequence": "sequence"

})

# =====================================================
# LOAD STAFF DATA
# =====================================================

STAFF = pd.read_excel(
    "data/raw/Station_Staff.xlsx"
)

STAFF.columns = STAFF.columns.str.strip()

# Expected columns:
# station
# booking_counter
# shift
# available_staff
# is_manned

# =====================================================
# SHIFT HOURS
# =====================================================

SHIFT_HOURS = {

    "Morning":[
        6,7,8,9,10,
        11,12,13,14
    ],

    "Evening":[
        15,16,17,18,19,
        20,21,22,23
    ]

}

# =====================================================
# STAFF CAPACITY
# =====================================================

STAFF_CAPACITY = 1800

# =====================================================
# GET STATIONS OF A LINE
# =====================================================

def get_stations_of_line(line):

    stations = ROUTE[
        ROUTE["line"] == line
    ]

    stations = stations.sort_values(
        "sequence"
    )

    return stations["station"].tolist()

# =====================================================
# GET BOOKING COUNTERS OF A STATION
# =====================================================

def get_booking_counters(station):

    counters = STAFF[
        STAFF["station"] == station
    ]

    counters = counters[
        counters["is_manned"] == 1
    ]

    return sorted(
        counters["booking_counter"].unique()
    )

# =====================================================
# GET AVAILABLE STAFF
# =====================================================

def get_available_staff(
    station,
    booking_counter,
    shift
):

    row = STAFF[

        (STAFF["station"] == station)

        &

        (STAFF["booking_counter"] == booking_counter)

        &

        (STAFF["shift"] == shift)

    ]

    if len(row) == 0:

        return 0

    return int(
        row.iloc[0]["available_staff"]
    )

# =====================================================
# CREATE FEATURE ROW
# =====================================================

def create_features(
    station,
    booking_counter,
    date,
    hour
):

    date = pd.to_datetime(date)

    year = date.year

    quarter = date.quarter

    month = date.month

    week_of_year = date.isocalendar().week

    day = date.day

    day_of_week = date.dayofweek

    is_weekend = int(
        day_of_week >= 5
    )

    is_month_start = int(
        date.is_month_start
    )

    is_month_end = int(
        date.is_month_end
    )

    # Shift

    if hour <= 14:

        shift = "Morning"

    else:

        shift = "Evening"

    # Time Slot

    if 6 <= hour <= 8:

        time_slot = "Early Morning"

    elif 9 <= hour <= 11:

        time_slot = "Morning Peak"

    elif 12 <= hour <= 15:

        time_slot = "Afternoon"

    elif 16 <= hour <= 19:

        time_slot = "Evening Peak"

    else:

        time_slot = "Night"

    # Peak Hour

    if hour in [
        7,8,9,10,
        17,18,19,20
    ]:

        peak_hour = 1

    else:

        peak_hour = 0

    row = pd.DataFrame({

        "station":[station],

        "booking_counter":[booking_counter],

        "year":[year],

        "quarter":[quarter],

        "month":[month],

        "week_of_year":[week_of_year],

        "day":[day],

        "day_of_week":[day_of_week],

        "is_weekend":[is_weekend],

        "is_month_start":[is_month_start],

        "is_month_end":[is_month_end],

        "hour":[hour],

        "shift":[shift],

        "time_slot":[time_slot],

        "peak_hour":[peak_hour]

    })

    # Encode categorical columns

    categorical = [

        "station",

        "booking_counter",

        "shift",

        "time_slot"

    ]

    row[categorical] = ENCODER.transform(
        row[categorical]
    )

    return row[FEATURE_COLUMNS]


# =====================================================
# PREDICT HOURLY
# =====================================================

def predict_hour(
    line,
    date,
    hour
):

    stations = get_stations_of_line(line)

    results = []

    for station in stations:

        booking_counters = get_booking_counters(
            station
        )

        # Station without manned booking counter

        if len(booking_counters) == 0:

            results.append({

                "station": station,

                "booking_counter": "Not Manned",

                "predicted_passengers": 0,

                "available_staff": 0,

                "required_staff": 0,

                "staff_gap": 0,

                "status": "Not Manned"

            })

            continue

        # Predict each booking counter

        for booking_counter in booking_counters:

            features = create_features(

                station,

                booking_counter,

                date,

                hour

            )

            prediction = MODEL.predict(
                features
            )[0]

            prediction = max(
                0,
                round(float(prediction))
            )

            shift = (

                "Morning"

                if hour <= 14

                else "Evening"

            )

            available_staff = get_available_staff(

                station,

                booking_counter,

                shift

            )

            required_staff = max(
                1,
                math.ceil(prediction / STAFF_CAPACITY)
            )

            staff_gap = (

                available_staff

                -

                required_staff

            )

            if staff_gap >= 0:

                status = "Sufficient"

            else:

                status = "Shortage"

            results.append({

                "station": station,

                "booking_counter": booking_counter,

                "predicted_passengers": prediction,

                "available_staff": available_staff,

                "required_staff": required_staff,

                "staff_gap": staff_gap,

                "status": status

            })

    return results


# =====================================================
# PREDICT SHIFT
# =====================================================

def predict_shift(
    line,
    date,
    shift
):

    if shift not in SHIFT_HOURS:

        raise ValueError(
            "Shift must be Morning or Evening"
        )

    stations = get_stations_of_line(line)

    results = []

    hours = SHIFT_HOURS[shift]

    for station in stations:

        booking_counters = get_booking_counters(
            station
        )

        # Station without manned booking counter

        if len(booking_counters) == 0:

            results.append({

                "station": station,

                "booking_counter": "Not Manned",

                "predicted_passengers": 0,

                "available_staff": 0,

                "required_staff": 0,

                "staff_gap": 0,

                "status": "Not Manned"

            })

            continue

        for booking_counter in booking_counters:

            total_prediction = 0

            for hour in hours:

                features = create_features(

                    station,

                    booking_counter,

                    date,

                    hour

                )

                prediction = MODEL.predict(
                    features
                )[0]

                prediction = max(
                    0,
                    round(float(prediction))
                )

                total_prediction += prediction

            available_staff = get_available_staff(

                station,

                booking_counter,

                shift

            )

            required_staff = max(

                1,

                math.ceil(

                    total_prediction /

                    STAFF_CAPACITY

                )

            )

            staff_gap = (

                available_staff

                -

                required_staff

            )

            if staff_gap >= 0:

                status = "Sufficient"

            else:

                status = "Shortage"

            results.append({

                "station": station,

                "booking_counter": booking_counter,

                "predicted_passengers": total_prediction,

                "available_staff": available_staff,

                "required_staff": required_staff,

                "staff_gap": staff_gap,

                "status": status

            })

    return results


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    print("=" * 70)
    print("HOURLY PREDICTION")
    print("=" * 70)

    hourly = predict_hour(

        line="BLUE",

        date="2026-06-30",

        hour=8

    )

    hourly_df = pd.DataFrame(hourly)

    print(hourly_df.head(20))

    print()

    print("=" * 70)
    print("SHIFT PREDICTION")
    print("=" * 70)

    shift = predict_shift(

        line="BLUE",

        date="2026-06-30",

        shift="Morning"

    )

    shift_df = pd.DataFrame(shift)

    print(shift_df.head(20))

