import pandas as pd

# Read PAPERQR sheet
df = pd.read_excel(
    "data/raw/Passenger_Data_Cleaned.xlsx",
    sheet_name="PAPERQR"
)

# Extract station code from terminal code
df["station"] = df["TERMINAL_CODE"].str[:4]

# Get unique terminals
terminals = (
    df[["TERMINAL_CODE", "station"]]
    .drop_duplicates()
    .sort_values(["station", "TERMINAL_CODE"])
    .reset_index(drop=True)
)

# Rename columns
terminals.columns = [
    "terminal_code",
    "station"
]

print(f"Total terminals: {len(terminals)}")
print(f"Total stations: {terminals['station'].nunique()}")

print("\nFirst 20 terminals:")
print(terminals.head(20))

# Save
terminals.to_excel(
    "data/master/all_terminals_PaperQR.xlsx",
    index=False
)

print(
    "\nSaved to data/master/all_terminals_PaperQR.xlsx"
)