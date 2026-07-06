import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "features"
    / "festival_features.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "models"
)

MODEL_DIR.mkdir(exist_ok=True)

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)

# =====================================
# ENCODE
# =====================================

encoders = {}

for col in [
    "Location",
    "TimeSlot"
]:

    le = LabelEncoder()

    df[col] = le.fit_transform(
        df[col]
    )

    encoders[col] = le

joblib.dump(
    encoders,
    MODEL_DIR / "festival_label_encoders.pkl"
)

# =====================================
# DROP UNUSED COLUMNS
# =====================================

drop_cols = [

    "Date",

    "Festival_Name",

    "Festival_Stage",

    "Token_Count",

    "Paper_QR",

    "Card_Issue",

    "Card_Recharge",

    "Passengers"
]

X = df.drop(
    columns=drop_cols
)

y = df["Passengers"]

print("\nFeatures:")
print(X.columns.tolist())

# =====================================
# SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42
)

# =====================================
# MODEL
# =====================================

model = XGBRegressor(

    n_estimators=600,

    learning_rate=0.05,

    max_depth=8,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42
)

print("\nTraining Festival Model...")

model.fit(
    X_train,
    y_train
)

# =====================================
# EVALUATION
# =====================================

preds = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    preds
)

rmse = (
    mean_squared_error(
        y_test,
        preds
    ) ** 0.5
)

r2 = r2_score(
    y_test,
    preds
)

print("\n========== RESULTS ==========")

print(f"MAE  : {mae:.2f}")

print(f"RMSE : {rmse:.2f}")

print(f"R²   : {r2:.4f}")

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(
    model,
    MODEL_DIR / "festival_xgboost_model.pkl"
)

print(
    "\nFestival Model Saved Successfully"
)