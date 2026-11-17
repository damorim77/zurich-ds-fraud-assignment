import pandas as pd
import os
import shutil

ROOT_PATH = f"../data"
RAW_PATH = f"{ROOT_PATH}/raw"
LANDING_PATH = f"{ROOT_PATH}/landing"

def raw_to_landing():
  """Runs excel conversion to parquet to enable faster analytical queries"""

  print("Reading source file")
  df = pd.read_excel(f'{RAW_PATH}/latam_data_assignment.xlsx')

  print("Treating mixed-types objects")
  # Convert mixed-type object columns to string to avoid PyArrow serialization issues
  if 'deductibleType' in df.columns:
    df['deductibleType'] = df['deductibleType'].astype(str)

  if os.path.exists(LANDING_PATH):
    print("Landing path already exists. Will be overwritten")
    shutil.rmtree(LANDING_PATH)
  
  print("Creating landing path")
  os.makedirs(LANDING_PATH, exist_ok=True)

  print("Saving parquet file to landing")
  df.to_parquet(f"{LANDING_PATH}/data.parquet", engine="pyarrow", compression="zstd", index=False)

  print("✅ Done")

