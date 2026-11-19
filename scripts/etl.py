from pathlib import Path
import shutil
import pandas as pd

ROOT_PATH    = Path(__file__).resolve().parents[1] / "data"
RAW_PATH     = ROOT_PATH / "raw"
LANDING_PATH = ROOT_PATH / "landing"

def raw_to_landing(overwrite=False):
    """Converts the raw Excel file to Parquet for faster analytics."""
    if LANDING_PATH.exists():
        if not overwrite:
            print("⚠️ Landing path already exists. Skipping conversion; pass overwrite=True to replace it.")
            return
        print("⚠️ Landing path already exists. Overwriting.")
        shutil.rmtree(LANDING_PATH)

    print("Reading source file")
    df = pd.read_excel(RAW_PATH / "latam_data_assignment.xlsx")

    df["deductibleType"] = df["deductibleType"].astype("string")

    LANDING_PATH.mkdir(parents=True)

    df.to_parquet(LANDING_PATH / "data.parquet", engine="pyarrow",
                  compression="zstd", index=False)
    print(f"✅ Done: {df.shape[0]} rows, {df.shape[1]} cols")
