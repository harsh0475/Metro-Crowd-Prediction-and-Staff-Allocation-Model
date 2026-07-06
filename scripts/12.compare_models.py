import pandas as pd

print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

# =====================================================
# LOAD METRICS
# =====================================================

xgb = pd.read_csv(
    "models/xgboost_metrics.csv"
)

lgb = pd.read_csv(
    "models/lightgbm_metrics.csv"
)

# =====================================================
# COMBINE
# =====================================================

comparison = pd.concat(
    [xgb, lgb],
    ignore_index=True
)

# =====================================================
# SORT BY R² SCORE
# =====================================================

comparison = comparison.sort_values(
    by="R2",
    ascending=False
).reset_index(drop=True)

# =====================================================
# ROUND VALUES
# =====================================================

comparison["MAE"] = comparison["MAE"].round(2)

comparison["RMSE"] = comparison["RMSE"].round(2)

comparison["R2"] = comparison["R2"].round(4)

comparison["Training_Time"] = comparison["Training_Time"].round(2)

comparison["Prediction_Time"] = comparison["Prediction_Time"].round(4)

# =====================================================
# SAVE
# =====================================================

comparison.to_csv(
    "models/model_comparison.csv",
    index=False
)

# =====================================================
# DISPLAY
# =====================================================

print()

print(comparison)

print()

print("=" * 70)

best = comparison.iloc[0]

print("BEST MODEL")

print("=" * 70)

print()

print(f"Model            : {best['Model']}")

print(f"R² Score         : {best['R2']}")

print(f"MAE              : {best['MAE']}")

print(f"RMSE             : {best['RMSE']}")

print(f"Training Time    : {best['Training_Time']} sec")

print(f"Prediction Time  : {best['Prediction_Time']} sec")

print()

print("=" * 70)

print("RANKING")

print("=" * 70)

for i, row in comparison.iterrows():

    print(

        f"{i+1}. {row['Model']}   "

        f"(R²={row['R2']}, "

        f"MAE={row['MAE']}, "

        f"RMSE={row['RMSE']})"

    )

print()

print("Comparison saved to")

print("models/model_comparison.csv")

print("=" * 70)