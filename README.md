# Metro Crowd Prediction and Staff Allocation System

Metro Crowd Prediction and Staff Allocation System is an AI-powered transit analytics platform designed to forecast passenger demand and optimize workforce allocation across metro stations.

The system uses Machine Learning models to predict crowd volume at different metro lines and stations, helping transportation authorities improve operational efficiency, reduce congestion, and deploy staff where they are needed most.

---

## Project Highlights

* AI-based passenger crowd prediction
* Hourly demand forecasting
* Shift-wise crowd estimation
* Automated staff allocation recommendations
* Festival-aware crowd prediction
* Metro line and station analytics
* Interactive dashboard visualizations
* FastAPI-powered REST APIs
* Responsive React frontend
* Real-world transit data processing

---

## Core Features

### Crowd Prediction

Predict passenger traffic across metro stations using trained XGBoost models.

* Hourly crowd forecasting
* Shift-wise crowd forecasting
* Line-level predictions
* Station-level analysis
* Demand trend estimation

### Staff Allocation

Optimize workforce deployment based on predicted passenger volumes.

* Automated staffing recommendations
* Station-wise staff requirements
* Booking counter allocation
* Shift planning support
* Workforce optimization

### Festival Demand Forecasting

Estimate passenger demand during special events and festivals.

* Festival-aware predictions
* Holiday crowd analysis
* Event-based demand forecasting
* Dynamic staffing adjustments

### Metro Network Analytics

Access route and station information across metro lines.

* Metro line information
* Station lookup
* Route sequencing
* Operational insights

### Dashboard and Visualization

Visualize predictions and operational metrics through interactive charts.

* Passenger trend charts
* Crowd distribution analysis
* Staff allocation summaries
* Station-level insights
* Real-time API integration

---

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* Tailwind CSS
* Axios
* Recharts
* React Router

### Backend

* Python
* FastAPI
* Pydantic
* Pandas
* NumPy
* Joblib

### Machine Learning

* XGBoost
* Scikit-Learn
* Feature Engineering
* Data Preprocessing

### Data Sources

* Metro Route Dataset
* Station Staff Dataset
* Festival Calendar Dataset
* Historical Passenger Traffic Data

---

## System Architecture

```text
Frontend (React + Vite)
            |
            v
      FastAPI Backend
            |
            v
   XGBoost Prediction Models
            |
            v
    Metro Transit Datasets
```

---

## Prediction Modules

### Standard Predictions

* Hourly Crowd Prediction
* Shift-wise Crowd Prediction
* Line-Level Forecasting
* Staff Requirement Estimation

### Festival Predictions

* Festival Hour Prediction
* Festival Shift Prediction
* Special Event Forecasting
* Festival Staffing Recommendations

---

## API Endpoints

### General

* GET / → Project Information
* GET /health → Health Check

### Metro Information

* GET /lines → Available Metro Lines
* GET /stations/{line} → Stations of a Line

### Prediction APIs

* POST /predict-hour
* POST /predict-shift
* POST /festival/predict-hour
* POST /festival/predict-shift

---

## Project Structure

```text
Metro-Crowd-Prediction-System/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── predict.py
│   ├── festival_predict.py
│   ├── models/
│   └── data/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## Business Impact

This system helps transportation authorities:

* Improve passenger experience
* Reduce station congestion
* Optimize staff utilization
* Improve operational planning
* Support festival and event management
* Enable data-driven decision making

---

## Future Enhancements

* Real-time passenger tracking
* Live metro feed integration
* Weather-aware predictions
* Deep Learning forecasting models
* Multi-city metro support
* Automated scheduling engine
* Cloud deployment pipeline
* Mobile application support

---

## Author

Harshit Kumar Singh

GitHub:
https://github.com/harsh0475

---

## License

This project was developed for educational, research, and portfolio purposes.
