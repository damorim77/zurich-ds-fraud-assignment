# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Data-science take-home assignment: predict fraudulent motor insurance claims (~119k claims, 55 columns, one row per claim). The full brief and data dictionary are in `docs/Assignment_DS_Fraud.pdf` — read it before modelling. Key traps called out there:

- `fraudStatus` is the target basis, but empty means "never reviewed", not "clean". Classes 91 (rental car) and 90 (third-person) are never reviewed by design; "Not confirmed" is neither positive nor negative.
- Review selection is non-random (selection bias).
- Frequently repeated identifier values are dummy placeholders and should count as missing.
- The file is a post-hoc snapshot: some columns (e.g. `claimValue`, `claimStatus`) leak information not available at first notification (FNOL).
- Several claim rows can share one loss event (`claimEventId`); policies can be renewed/rewritten.
- Dates `hourOfEvent`, `vehManuYear`, `vehModelYear` have dummy date/month parts; `insuDateOfBirth`, `birthdate`, `driverDtOfBirth_claim` are birth years.

## Layout and data flow

- `data/raw/latam_data_assignment.xlsx` → (`scripts/etl.py::raw_to_landing`) → `data/landing/data.parquet` (zstd). Both are committed. `raw_to_landing()` deletes and recreates `data/landing/`, and casts `deductibleType` to pandas `string` so nulls survive Parquet.
- `scripts/utils.py` holds shared helpers (e.g. `get_frequency_table`, which appends a Total row).
- `notebooks/01-ingestion.ipynb` runs the ETL; `notebooks/02-exploration.ipynb` reads the Parquet via DuckDB (`SELECT ... FROM '../data/landing/data.parquet'`) and does EDA (sweetviz, placeholder-value detection, `claimEventId` consistency, same-event time amplitude).
- Notebooks add `../scripts` to `sys.path` and import from it, so they must be run with `notebooks/` as the working directory. They are also written to run on Google Colab: they detect Colab, clone `damorim77/zurich-ds-fraud-assignment` and `pip install -r requirements.txt`.

## Commands

No build, lint or test setup exists. Dependencies: `pip install -r requirements.txt` (numpy, pandas, pyarrow, duckdb; notebooks also use sweetviz, matplotlib, seaborn, which are not pinned). Reading the `.xlsx` additionally needs `openpyxl`, also not listed.

Regenerate the Parquet from the repo root:

```
python -c "import sys; sys.path.insert(0,'scripts'); from etl import raw_to_landing; raw_to_landing()"
```

## Conventions

- Code comments and docstrings are mixed English/Portuguese; notebook markdown is English.
- Several notebook cells contain non-ASCII characters (docstrings with accents); keep files UTF-8 and use `encoding="utf8"` when reading `.ipynb` with Python on Windows.
