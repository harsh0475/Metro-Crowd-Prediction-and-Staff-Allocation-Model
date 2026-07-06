import joblib
import pandas as pd

from pathlib import Path

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "festival_xgboost_model.pkl"
)

ENCODER_PATH = (
    BASE_DIR
    / "models"
    / "festival_label_encoders.pkl"
)

CALENDAR_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "festival_calendar.csv"
)

# =====================================
# LOAD
# =====================================

model = joblib.load(MODEL_PATH)

encoders = joblib.load(
    ENCODER_PATH
)

calendar_df = pd.read_csv(
    CALENDAR_PATH
)

calendar_df["Mahalaya"] = pd.to_datetime(
    calendar_df["Mahalaya"],
    format="%d-%m-%y"
)

calendar_df["Dashami"] = pd.to_datetime(
    calendar_df["Dashami"],
    format="%d-%m-%y"
)

# =====================================
# HELPERS
# =====================================

def get_time_slot(hour):

    if hour < 12:
        return "Morning"

    elif hour < 17:
        return "Afternoon"

    return "Evening"


def get_peak_hour(hour):

    return int(

        (8 <= hour <= 10)

        or

        (17 <= hour <= 20)
    )


def get_festival_code(name):

    mapping = {

        "Durga_Puja": 1,

        "Christmas": 2,

        "New_Year": 3
    }

    return mapping.get(name, 0)


def get_stage_code(days_to_dashami):

    if days_to_dashami > 10:
        return 0

    elif days_to_dashami > 4:
        return 1

    elif days_to_dashami == 4:
        return 2

    elif days_to_dashami == 3:
        return 3

    elif days_to_dashami == 2:
        return 4

    elif days_to_dashami == 1:
        return 5

    elif days_to_dashami == 0:
        return 6

    return 7


# =====================================
# PREDICT
# =====================================

def predict_festival_crowd(

    station,
    date_str,
    hour,
    festival_name

):

    date = pd.to_datetime(
        date_str
    )

    year = date.year

    month = date.month

    day = date.day

    day_of_week = (
        date.dayofweek
    )

    week_of_year = int(
        date.isocalendar().week
    )

    quarter = (
        date.quarter
    )

    weekend = (
        1
        if day_of_week >= 5
        else 0
    )

    peak_hour = get_peak_hour(
        hour
    )

    time_slot = get_time_slot(
        hour
    )

    days_to_dashami = -1

    days_from_mahalaya = -1

    festival_week = -1

    pre_puja_weekend = 0

    stage_code = 20

    if festival_name == "Durga_Puja":

        row = calendar_df[
            calendar_df["Year"]
            == year
        ]

        if not row.empty:

            mahalaya = (
                row.iloc[0]["Mahalaya"]
            )

            dashami = (
                row.iloc[0]["Dashami"]
            )

            days_to_dashami = (
                dashami - date
            ).days

            days_from_mahalaya = (
                date - mahalaya
            ).days

            if days_to_dashami > 14:

                festival_week = 0

            elif days_to_dashami > 7:

                festival_week = 1

            elif days_to_dashami >= 0:

                festival_week = 2

            else:

                festival_week = 3

            if (
                festival_week in [0, 1]
                and weekend == 1
            ):
                pre_puja_weekend = 1

            stage_code = (
                get_stage_code(
                    days_to_dashami
                )
            )

    station_encoded = (
        encoders["Location"]
        .transform([station])[0]
    )

    timeslot_encoded = (
        encoders["TimeSlot"]
        .transform([time_slot])[0]
    )

    X = pd.DataFrame({

        "Location": [
            station_encoded
        ],

        "Hour": [hour],

        "Year": [year],

        "Month": [month],

        "Day": [day],

        "DayOfWeek": [
            day_of_week
        ],

        "WeekOfYear": [
            week_of_year
        ],

        "Quarter": [
            quarter
        ],

        "Weekend": [
            weekend
        ],

        "PeakHour": [
            peak_hour
        ],

        "TimeSlot": [
            timeslot_encoded
        ],

        "Festival_Code": [
            get_festival_code(
                festival_name
            )
        ],

        "Days_To_Dashami": [
            days_to_dashami
        ],

        "Days_From_Mahalaya": [
            days_from_mahalaya
        ],

        "Festival_Week": [
            festival_week
        ],

        "Festival_Stage_Code": [
            stage_code
        ],
        
        "PrePujaWeekend": [
            pre_puja_weekend
        ]
    })

    prediction = model.predict(X)[0]

    return max(
        0,
        int(round(prediction))
    )
    
import math

# =====================================
# REQUIRED STAFF
# =====================================

def required_staff(
    passengers
):

    return max(
        1,
        math.ceil(
            passengers / 1800
        )
    )


# =====================================
# SHIFT STAFF PREDICTION
# =====================================

def predict_shift_staff(

    station,
    date,
    shift,
    festival_name

):

    if shift == "Night":

        hours = [
            23,
            0,1,2,3,4,5
        ]

    elif shift == "Morning":

        hours = [
            6,7,8,9,
            10,11,12,13
        ]

    else:

        hours = [
            14,15,16,17,
            18,19,20,21,22
        ]

    total_passengers = 0

    for hour in hours:

        crowd = predict_festival_crowd(

            station=station,

            date_str=date,

            hour=hour,

            festival_name=festival_name

        )

        total_passengers += crowd

    staff = required_staff(
        total_passengers
    )

    return {

        "station": station,

        "festival": festival_name,

        "date": date,

        "shift": shift,

        "passengers": total_passengers,

        "required_staff": staff

    }