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
- `notebooks/01-ingestion.ipynb` runs the ETL; `notebooks/02-exploration.ipynb` reads the Parquet via DuckDB (`SELECT ... FROM '../data/landing/data.parquet'`) into `df` and does EDA (sweetviz, placeholder-value detection, `claimEventId` consistency, same-event time amplitude, spelling variants like `Collision (v2)`).
- The landing Parquet has 63,944 rows, while the brief says ~119k claims. Not yet reconciled with the Excel source.
- Notebooks add `../scripts` to `sys.path` and import from it, so they must be run with `notebooks/` as the working directory. They are also written to run on Google Colab: they detect Colab, clone `damorim77/zurich-ds-fraud-assignment` and `pip install -r requirements.txt`.

## Commands

No build, lint or test setup exists. Dependencies: `pip install -r requirements.txt` (numpy, pandas, pyarrow, duckdb; notebooks also use sweetviz, matplotlib, seaborn, which are not pinned). Reading the `.xlsx` additionally needs `openpyxl`, also not listed.

Regenerate the Parquet from the repo root:

```
python -c "import sys; sys.path.insert(0,'scripts'); from etl import raw_to_landing; raw_to_landing()"
```

## Conventions

- Notebooks: all code, comments and markdown must be in English. `scripts/` still has Portuguese docstrings.
- One-off analysis in `02-exploration.ipynb` is written as plain top-level cells, not wrapped in functions.
- Reuse shared definitions instead of redefining them: `id_cols` (identifier-like columns, defined in the sweetviz cell) feeds the frequency plots and the placeholder diagnosis. Cells depend on run order.
- Never rebind `df` to a query result in a later cell (an earlier bug: the claim-event amplitude query overwrote it and broke the placeholder cell). Use a distinct name such as `df_events`.
- Analysis decisions are documented in the notebook but are often left open on purpose (e.g. spelling variants may be a model signal, so they are shown, not normalized). Do not normalize or drop data unprompted.
- `.ipynb` files are saved as JSON with indent 2, LF newlines, sorted keys and a trailing newline. Edit them with a script that round-trips `json.dumps(nb, indent=2, ensure_ascii=False) + "
"` and confirm the round trip is byte-identical before writing, to keep diffs small. Read with `encoding="utf8"` on Windows; the console may show accents garbled even when the file is fine.
- `duckdb` and `sweetviz` may not be installed in the local Python; the notebook is meant for Colab. For local checks, query the Parquet with pandas.
