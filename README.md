# NYC Taxi SQL Analytics

> 🚧 **Work in progress.** This README describes the project's goals and planned structure. Findings, charts and the dashboard will be added as each stage is completed.

SQL-first analysis of ~9 million NYC Yellow Taxi trips (January–March 2024), built on Apache Spark. The project answers business questions about **when** people take taxis, **where** trips start and end, and **what is associated with higher fares and tips**, using a layered data pipeline that can be rebuilt from scratch with two commands.

## Business questions

1. **Demand over time:** How does trip volume vary by day, hour and day of week? How do weekdays compare to weekends?
2. **Geography:** Which zones and routes concentrate the most trips, and which generate the most revenue?
3. **Fares and tips:** How do fares relate to distance, time of day and payment type? What drives tip percentage on card payments?

## Data

| Dataset | Source | Period |
|---|---|---|
| Yellow Taxi Trip Records (Parquet) | [NYC Taxi & Limousine Commission (TLC)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | Jan–Mar 2024 |
| Taxi Zone Lookup (CSV) | NYC TLC | — |

Known limitations of the source data are documented in [`docs/data_dictionary.md`](docs/data_dictionary.md). The most important one: **cash tips are not recorded** in `tip_amount`, so tip analysis is restricted to card payments.

## Architecture

The pipeline follows a layered design (equivalent to Bronze / Silver / Gold), so it can later be migrated to dbt and an orchestrator without being rebuilt:

```
raw (TLC Parquet + CSV)
  └─► staging   cleaned, typed and enriched trips (trips_clean)
        └─► marts   small aggregated tables for the dashboard
              └─► Power BI
```

- **Spark SQL** is the main language. All transformations live in `.sql` files.
- **PySpark** is used only to read files, run the `.sql` files in order and write the results.
- Every cleaning rule is documented and justified in [`docs/cleaning_rules.md`](docs/cleaning_rules.md), and the number of rows removed by each rule is reported.

## Tech stack

- Apache Spark (local mode) · Spark SQL · PySpark
- Python (pandas, pyarrow, matplotlib, Jupyter)
- Power BI Desktop

## Repository structure

```
nyc-taxi-sql-analytics/
├── data/                # not versioned (raw/, staging/, marts/)
├── sql/
│   ├── staging/         # cleaning and enrichment
│   ├── marts/           # aggregated tables for the dashboard
│   └── analysis/        # business-question queries
├── src/
│   ├── spark_session.py # shared Spark configuration
│   ├── download_data.py # downloads raw data from the TLC
│   └── build.py         # runs the full pipeline
├── notebooks/
├── dashboard/
├── images/
├── docs/                # data dictionary and cleaning rules
├── requirements.txt
└── README.md
```

## How to run

> Setup instructions will be finalized once the environment stage is complete.

Requirements: Python 3.10+ and Java (JDK 17). On Windows, WSL2 is recommended.

```bash
pip install -r requirements.txt
python src/download_data.py   # download raw data into data/raw/
python src/build.py           # rebuild staging and marts from scratch
```

## Roadmap

- [ ] Environment setup and data download
- [ ] Data exploration and quality assessment
- [ ] Staging layer and reproducible pipeline
- [ ] Business-question SQL queries
- [ ] Marts for the dashboard
- [ ] Power BI dashboard
- [ ] Findings, limitations and final documentation

**Future (phase 2):** dbt models, orchestration and data-quality tests.