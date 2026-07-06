import joblib
import pandas as pd
import math

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


def get_stations_of_line(line):

    stations = ROUTE[ROUTE["line"] == line]

    stations = stations.sort_values("sequence")

    return stations["station"].tolist()


# =====================================================
# LOAD FESTIVAL MODEL
# =====================================================

print("Loading Festival XGBoost Model...")

FESTIVAL_MODEL = joblib.load(
    "models/festival_xgboost_model.pkl"
)

print("Loading Festival Encoders...")

FESTIVAL_ENCODERS = joblib.load(
    "models/festival_label_encoders.pkl"
)

# =====================================================
# LOAD FESTIVAL CALENDAR
# =====================================================

FESTIVAL_CALENDAR = pd.read_csv(
    "data/raw/festival_calendar.csv"
)

FESTIVAL_CALENDAR["Mahalaya"] = pd.to_datetime(
    FESTIVAL_CALENDAR["Mahalaya"],
    format="%d-%m-%y"
)

FESTIVAL_CALENDAR["Dashami"] = pd.to_datetime(
    FESTIVAL_CALENDAR["Dashami"],
    format="%d-%m-%y"
)

# =====================================================
# AVAILABLE FESTIVALS
# =====================================================

FESTIVAL_CODES = {
    "Durga_Puja": 1,
    "Christmas": 2,
    "New_Year": 3
}

AVAILABLE_FESTIVALS = list(FESTIVAL_CODES.keys())

# =====================================================
# SHIFT HOURS (Morning / Evening / Night)
# =====================================================

FESTIVAL_SHIFT_HOURS = {
    "Morning": [6, 7, 8, 9, 10, 11, 12, 13],
    "Evening": [14, 15, 16, 17, 18, 19, 20, 21, 22],
    "Night": [23, 0, 1, 2, 3, 4, 5]
}

# =====================================================
# STAFF CAPACITY (passengers handled per staff member)
# =====================================================

STAFF_CAPACITY = 1800

# =====================================================
# HELPERS
# =====================================================

def get_time_slot(hour):
    if hour < 12:
        return "Morning"
    elif hour < 17:
        return "Afternoon"
    return "Evening"


def get_peak_hour(hour):
    return int((8 <= hour <= 10) or (17 <= hour <= 20))


def get_festival_code(name):
    return FESTIVAL_CODES.get(name, 0)


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


# =====================================================
# REQUIRED STAFF
# =====================================================

def required_staff(passengers):
    return max(1, math.ceil(passengers / STAFF_CAPACITY))


# =====================================================
# CORE PREDICTION (STATION WISE, HOURLY)
# =====================================================

def predict_festival_crowd(station, date_str, hour, festival_name):

    date = pd.to_datetime(date_str)

    year = date.year
    month = date.month
    day = date.day
    day_of_week = date.dayofweek
    week_of_year = int(date.isocalendar().week)
    quarter = date.quarter
    weekend = 1 if day_of_week >= 5 else 0

    peak_hour = get_peak_hour(hour)
    time_slot = get_time_slot(hour)

    days_to_dashami = -1
    days_from_mahalaya = -1
    festival_week = -1
    pre_puja_weekend = 0
    stage_code = 20

    if festival_name == "Durga_Puja":

        row = FESTIVAL_CALENDAR[FESTIVAL_CALENDAR["Year"] == year]

        if not row.empty:

            mahalaya = row.iloc[0]["Mahalaya"]
            dashami = row.iloc[0]["Dashami"]

            days_to_dashami = (dashami - date).days
            days_from_mahalaya = (date - mahalaya).days

            if days_to_dashami > 14:
                festival_week = 0
            elif days_to_dashami > 7:
                festival_week = 1
            elif days_to_dashami >= 0:
                festival_week = 2
            else:
                festival_week = 3

            if festival_week in [0, 1] and weekend == 1:
                pre_puja_weekend = 1

            stage_code = get_stage_code(days_to_dashami)

    try:
        station_encoded = FESTIVAL_ENCODERS["Location"].transform([station])[0]
    except ValueError:
        raise ValueError(
            f"Station '{station}' is not recognized by the festival model."
        )

    timeslot_encoded = FESTIVAL_ENCODERS["TimeSlot"].transform([time_slot])[0]

    X = pd.DataFrame({
        "Location": [station_encoded],
        "Hour": [hour],
        "Year": [year],
        "Month": [month],
        "Day": [day],
        "DayOfWeek": [day_of_week],
        "WeekOfYear": [week_of_year],
        "Quarter": [quarter],
        "Weekend": [weekend],
        "PeakHour": [peak_hour],
        "TimeSlot": [timeslot_encoded],
        "Festival_Code": [get_festival_code(festival_name)],
        "Days_To_Dashami": [days_to_dashami],
        "Days_From_Mahalaya": [days_from_mahalaya],
        "Festival_Week": [festival_week],
        "Festival_Stage_Code": [stage_code],
        "PrePujaWeekend": [pre_puja_weekend]
    })

    prediction = FESTIVAL_MODEL.predict(X)[0]

    return max(0, int(round(prediction)))


# =====================================================
# HOURLY PREDICTION - WHOLE LINE, STATION WISE
# =====================================================

def predict_festival_hour(line, date, hour, festival_name):

    if festival_name not in AVAILABLE_FESTIVALS:
        raise ValueError(
            f"Unknown festival '{festival_name}'. Available: {AVAILABLE_FESTIVALS}"
        )

    stations = get_stations_of_line(line)

    results = []

    for station in stations:

        passengers = predict_festival_crowd(
            station=station,
            date_str=date,
            hour=hour,
            festival_name=festival_name
        )

        station_name = ROUTE.loc[
            ROUTE["station"] == station, "station_name"
        ].iloc[0]

        results.append({
            "station": station,
            "station_name": station_name,
            "predicted_passengers": passengers,
            "required_staff": required_staff(passengers)
        })

    return results


# =====================================================
# SHIFT PREDICTION - WHOLE LINE, STATION WISE
# =====================================================

def predict_festival_shift(line, date, shift, festival_name):

    if festival_name not in AVAILABLE_FESTIVALS:
        raise ValueError(
            f"Unknown festival '{festival_name}'. Available: {AVAILABLE_FESTIVALS}"
        )

    if shift not in FESTIVAL_SHIFT_HOURS:
        raise ValueError("Shift must be Morning, Evening or Night")

    stations = get_stations_of_line(line)
    hours = FESTIVAL_SHIFT_HOURS[shift]

    results = []

    for station in stations:

        total_passengers = 0

        for hour in hours:
            total_passengers += predict_festival_crowd(
                station=station,
                date_str=date,
                hour=hour,
                festival_name=festival_name
            )

        station_name = ROUTE.loc[
            ROUTE["station"] == station, "station_name"
        ].iloc[0]

        results.append({
            "station": station,
            "station_name": station_name,
            "predicted_passengers": total_passengers,
            "required_staff": required_staff(total_passengers)
        })

    return results