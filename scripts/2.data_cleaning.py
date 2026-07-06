import pandas as pd

INPUT_FILE = "data/raw/Passenger_Data.xlsx"
OUTPUT_FILE = "data/raw/Passenger_Data_Cleaned.xlsx"

REMOVE_TERMINALS = [
    "BCSD81",
    "BCSD82",
    "CCSC82",
    "CCSC83",
    "CCSC91",
    "CPSA82",
    "CPSA83",
    "HWHM82",
    "HWHM83",
    "HWHM84",
    "HWHM86",
    "HWHM87",
    "HWHM88",
    "HWHM89",
    "HWHM91",
    "HWMM81",
    "HWMM82",
    "HWMM83",
    "HWMM84",
    "HWMM85",
    "HWMM91",
    "KBAR81",
    "KBBR81",
    "KBBR82",
    "KBCR81",
    "KBCR82",
    "KBEL81",
    "KCEN81",
    "KCEN82",
    "KCWC81",
    "KCWC82",
    "KCWC83",
    "KDCM81",
    "KDMI83",
    "KDMI84",
    "KDMI85",
    "KDMI86",
    "KDSW81",
    "KDSW82",
    "KDSW83",
    "KESA82",
    "KESA83",
    "KESA91",
    "KESP81",
    "KESP82",
    "KESP83",
    "KESP84",
    "KESP85",
    "KESP86",
    "KESP89",
    "KESP90",
    "KESP91",
    "KESP92",
    "KGPK81",
    "KGTN81",
    "KJHD81",
    "KJPK81",
    "KJPK82",
    "KJRO83",
    "KKHG81",
    "KKHG82",
    "KKHG83",
    "KKHG84",
    "KKNZ81",
    "KKNZ82",
    "KKSK81",
    "KKSK82",
    "KKVS81",
    "KKVS82",
    "KMDI81",
    "KMHR81",
    "KMJH82",
    "KMJH83",
    "KMSN81",
    "KMUK81",
    "KMUK82",
    "KNBN81",
    "KNOA81",
    "KNTJ81",
    "KPSK81",
    "KRSB81",
    "KRSB82",
    "KRSB83",
    "KRSD81",
    "KRSD82",
    "KRSD83",
    "KSHO81",
    "KSHY81",
    "KSHY82",
    "KSKB81",
    "KSKB82",
    "KSKD81",
    "KSKD82",
    "KTKP81",
    "KTKP82",
    "KTRT81",
    "KTRT82",
    "MKNA81",
    "MKNA83",
    "MKNA84",
    "MKNA85",
    "MKNA91",
    "PBGB81",
    "PBGB82",
    "PBGB83",
    "PBGB91",
    "SDHM81",
    "SDHM82",
    "SDHM83",
    "SDHM84",
    "SDHM85",
    "SDHM86",
    "SDHM91",
    "SSSA82",
    "SSSA83",
    "SSSA91",
    "SVSA81",
    "SVSA82",
    "SVSA83",
    "SVSA84",
    "SVSA85",
    "SVSA91",
    "WHWHM1",
    "WHWMM1",
    "WMKNA1"
]

sheets = {}

for sheet in ["PAPERQR", "ISSUE", "RECHARGE"]:

    df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

    before = len(df)

    df = df[
        ~df["TERMINAL_CODE"].isin(REMOVE_TERMINALS)
    ]

    after = len(df)

    print(
        f"{sheet}: Removed {before-after} rows"
    )

    sheets[sheet] = df

with pd.ExcelWriter(OUTPUT_FILE) as writer:
    for sheet_name, df in sheets.items():
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

print(f"\nSaved: {OUTPUT_FILE}")