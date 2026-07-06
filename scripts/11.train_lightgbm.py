import os
import time
import joblib
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from lightgbm import LGBMRegressor

# =====================================================
# CREATE MODELS FOLDER
# =====================================================

os.makedirs("models", exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

print("=" * 70)
print("LIGHTGBM MODEL TRAINING")
print("=" * 70)

df = pd.read_csv(
    "data/features/final_dataset.csv"
)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(
    [
        "date",
        "station",
        "booking_counter",
        "hour"
    ]
).reset_index(drop=True)

# =====================================================
# FEATURES
# =====================================================

FEATURES = [

    "station",

    "booking_counter",

    "year",

    "quarter",

    "month",

    "week_of_year",

    "day",

    "day_of_week",

    "is_weekend",

    "is_month_start",

    "is_month_end",

    "hour",

    "shift",

    "time_slot",

    "peak_hour"

]

TARGET = "passengers"

# =====================================================
# ENCODE CATEGORICAL FEATURES
# =====================================================

categorical_columns = [

    "station",

    "booking_counter",

    "shift",

    "time_slot"

]

encoder = OrdinalEncoder()

df[categorical_columns] = encoder.fit_transform(
    df[categorical_columns]
)

joblib.dump(
    encoder,
    "models/lightgbm_encoder.pkl"
)

joblib.dump(
    FEATURES,
    "models/lightgbm_feature_columns.pkl"
)

# =====================================================
# TIME BASED SPLIT
# =====================================================

split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index]

test_df = df.iloc[split_index:]

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

print()

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

print()

print(
    "Training Period :",
    train_df["date"].min().date(),
    "to",
    train_df["date"].max().date()
)

print(
    "Testing Period  :",
    test_df["date"].min().date(),
    "to",
    test_df["date"].max().date()
)

# =====================================================
# MODEL
# =====================================================

model = LGBMRegressor(

    n_estimators=800,

    learning_rate=0.03,

    max_depth=8,

    num_leaves=31,

    subsample=0.9,

    colsample_bytree=0.9,

    random_state=42

)

# =====================================================
# TRAIN
# =====================================================

print()
print("Training Model...")

start_train = time.time()

model.fit(
    X_train,
    y_train
)

end_train = time.time()

# =====================================================
# PREDICT
# =====================================================

print("Predicting...")

start_predict = time.time()

predictions = model.predict(
    X_test
)

end_predict = time.time()

# =====================================================
# METRICS
# =====================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    "models/lightgbm_model.pkl"
)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

importance = pd.DataFrame({

    "Feature": FEATURES,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

importance.to_csv(

    "models/lightgbm_feature_importance.csv",

    index=False

)

# =====================================================
# SAVE METRICS
# =====================================================

metrics = pd.DataFrame({

    "Model": ["LightGBM"],

    "MAE": [mae],

    "RMSE": [rmse],

    "R2": [r2],

    "Training_Time": [end_train - start_train],

    "Prediction_Time": [end_predict - start_predict]

})

metrics.to_csv(

    "models/lightgbm_metrics.csv",

    index=False

)

# =====================================================
# RESULTS
# =====================================================

print()

print("=" * 70)
print("RESULTS")
print("=" * 70)

print()

print(f"MAE              : {mae:.2f}")
print(f"RMSE             : {rmse:.2f}")
print(f"R² Score         : {r2:.4f}")

print()

print(f"Training Time    : {end_train-start_train:.2f} sec")
print(f"Prediction Time  : {end_predict-start_predict:.4f} sec")

print()

print("=" * 70)
print("TOP 10 IMPORTANT FEATURES")
print("=" * 70)

print(
    importance.head(10)
)

print()

print("Files Saved")

print()

print("models/lightgbm_model.pkl")
print("models/lightgbm_encoder.pkl")
print("models/lightgbm_feature_columns.pkl")
print("models/lightgbm_feature_importance.csv")
print("models/lightgbm_metrics.csv")

print("=" * 70)