from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import (
    HourPredictionRequest,
    ShiftPredictionRequest,
    FestivalHourPredictionRequest,
    FestivalShiftPredictionRequest
)

from backend.predict import (
    predict_hour,
    predict_shift
)

from backend.festival_predict import (
    predict_festival_hour,
    predict_festival_shift,
    AVAILABLE_FESTIVALS
)

app = FastAPI(

    title="Metro Crowd Prediction API",

    description="Metro Crowd Prediction",

    version="1.0"

)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ==========================================================
# HOME
# ==========================================================

@app.get("/")

def home():

    return {

        "project":

        "Metro Crowd Prediction and Staff Allocation System",

        "model":

        "XGBoost",

        "status":

        "Running"

    }

# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():

    return {

        "status":"Healthy",

        "model":"Loaded"

    }

# ==========================================================
# GET ALL LINES
# ==========================================================

import pandas as pd

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

@app.get("/lines")

def get_lines():

    lines = sorted(

        ROUTE["line"].unique().tolist()

    )

    return {

        "lines": lines

    }
    
# ==========================================================
# GET STATIONS OF A LINE
# ==========================================================

@app.get("/stations/{line}")

def get_stations(line: str):

    stations = (

        ROUTE[
            ROUTE["line"].str.upper() == line.upper()
        ]

        .sort_values("sequence")

        [[
            "station",
            "station_name",
            "sequence"
        ]]

    )

    return {

        "line": line.upper(),

        "total_stations": len(stations),

        "stations": stations.to_dict(
            orient="records"
        )

    }
    
# ==========================================================
# HOURLY PREDICTION
# ==========================================================

@app.post("/predict-hour")
def hourly_prediction(
    request: HourPredictionRequest
):

    try:

        prediction = predict_hour(

            line=request.line,

            date=request.date,

            hour=request.hour

        )

        grouped = group_by_station(
            prediction
        )

        return {

            "success": True,

            "line": request.line,

            "date": request.date,

            "hour": request.hour,

            "total_stations": len(grouped),

            "results": grouped

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }
        
# ==========================================================
# SHIFT PREDICTION
# ==========================================================

@app.post("/predict-shift")
def shift_prediction(
    request: ShiftPredictionRequest
):

    try:

        prediction = predict_shift(

            line=request.line,

            date=request.date,

            shift=request.shift

        )

        grouped = group_by_station(
            prediction
        )

        return {

            "success": True,

            "line": request.line,

            "date": request.date,

            "shift": request.shift,

            "total_stations": len(grouped),

            "results": grouped

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }
        
from collections import defaultdict

# ==========================================================
# GROUP RESULTS BY STATION
# ==========================================================

from collections import defaultdict

def group_by_station(predictions):

    grouped = defaultdict(list)

    for row in predictions:

        grouped[row["station"]].append({

            "booking_counter": row["booking_counter"],

            "predicted_passengers": row["predicted_passengers"],

            "available_staff": row["available_staff"],

            "required_staff": row["required_staff"],

            "staff_gap": row["staff_gap"],

            "status": row["status"]

        })

    results = []

    for station, counters in grouped.items():

        station_name = ROUTE.loc[
            ROUTE["station"] == station,
            "station_name"
        ].iloc[0]

        results.append({

            "station": station,

            "station_name": station_name,

            "booking_counters": counters

        })

    return results


# ==========================================================
# GET AVAILABLE FESTIVALS
# ==========================================================

@app.get("/festivals")

def get_festivals():

    return {
        "festivals": AVAILABLE_FESTIVALS
    }

# ==========================================================
# FESTIVAL HOURLY PREDICTION (STATION WISE)
# ==========================================================

@app.post("/festival/predict-hour")
def festival_hourly_prediction(
    request: FestivalHourPredictionRequest
):

    try:

        results = predict_festival_hour(
            line=request.line,
            date=request.date,
            hour=request.hour,
            festival_name=request.festival_name
        )

        return {
            "success": True,
            "line": request.line,
            "date": request.date,
            "hour": request.hour,
            "festival_name": request.festival_name,
            "total_stations": len(results),
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

# ==========================================================
# FESTIVAL SHIFT PREDICTION (STATION WISE)
# ==========================================================

@app.post("/festival/predict-shift")
def festival_shift_prediction(
    request: FestivalShiftPredictionRequest
):

    try:

        results = predict_festival_shift(
            line=request.line,
            date=request.date,
            shift=request.shift,
            festival_name=request.festival_name
        )

        return {
            "success": True,
            "line": request.line,
            "date": request.date,
            "shift": request.shift,
            "festival_name": request.festival_name,
            "total_stations": len(results),
            "results": results
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }