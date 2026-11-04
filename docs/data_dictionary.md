# Data Dictionary

Reference for the raw data used in this project. Field definitions and codes follow the official TLC documentation; observations marked **(observed)** come from reading the files with Spark.

## Sources

| Dataset | File(s) in `data/raw/` | Period | Rows |
|---|---|---|---|
| Yellow Taxi Trip Records (Parquet) | `yellow_tripdata_2024-01.parquet`, `-02`, `-03` | Jan–Mar 2024 | Jan: 2,964,624 (Feb and Mar: see profiling) |
| Taxi Zone Lookup (CSV) | `taxi_zone_lookup.csv` | Reference table | — |

- Portal: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- Official field definitions: [Data Dictionary – Yellow Taxi Trip Records](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) (version dated March 18, 2025)
- General caveats: [TLC Trip Record User Guide](https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf)
- Download details (source URL, size) are recorded by `src/download_data.py` in `data/raw/download_log.csv`.

## Trip record fields

Spark types are as read from the January 2024 file **(observed)**. The staging name is the column in `trips_clean`; "—" means the field is not used in the MVP.

| Raw field | Spark type | Description | Staging name |
|---|---|---|---|
| `VendorID` | integer | TPEP provider that supplied the record (codes below) | `vendor_id` |
| `tpep_pickup_datetime` | timestamp_ntz | Date and time the meter was started | `pickup_ts` |
| `tpep_dropoff_datetime` | timestamp_ntz | Date and time the meter was stopped | `dropoff_ts` |
| `passenger_count` | long | Number of passengers; **entered by the driver** | `passenger_count` |
| `trip_distance` | double | Trip distance in miles, recorded by the taximeter | `trip_distance` |
| `RatecodeID` | long | Final rate code in effect at the end of the trip (codes below) | `ratecode_id` |
| `store_and_fwd_flag` | string | `Y` = record held in vehicle memory before sending (no server connection); `N` = sent directly | — |
| `PULocationID` | integer | TLC Taxi Zone where the meter was started | `pu_location_id` |
| `DOLocationID` | integer | TLC Taxi Zone where the meter was stopped | `do_location_id` |
| `payment_type` | long | How the passenger paid (codes below) | `payment_type` |
| `fare_amount` | double | Time-and-distance fare calculated by the meter | `fare_amount` |
| `extra` | double | Miscellaneous extras and surcharges | — |
| `mta_tax` | double | Tax automatically triggered by the metered rate in use | — |
| `tip_amount` | double | Tip amount; **credit card tips only, cash tips are not included** | `tip_amount` |
| `tolls_amount` | double | Total of all tolls paid in the trip | — |
| `improvement_surcharge` | double | Surcharge assessed at flag drop (since 2015) | — |
| `total_amount` | double | Total charged to passengers; **does not include cash tips** | `total_amount` |
| `congestion_surcharge` | double | NYS congestion surcharge collected for the trip | — |
| `Airport_fee` | double | Fee for pickups at LaGuardia and JFK airports only | — |

Not present in 2024 files: `cbd_congestion_fee` (MTA Congestion Relief Zone charge, started January 5, 2025).

## Code values

**VendorID**

| Code | Provider |
|---|---|
| 1 | Creative Mobile Technologies, LLC |
| 2 | Curb Mobility, LLC |
| 6 | Myle Technologies Inc |
| 7 | Helix |

**RatecodeID**

| Code | Rate |
|---|---|
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau or Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |
| 99 | Null/unknown |

**payment_type**

| Code | Payment |
|---|---|
| 0 | Flex Fare trip |
| 1 | Credit card |
| 2 | Cash |
| 3 | No charge |
| 4 | Dispute |
| 5 | Unknown |
| 6 | Voided trip |

## Taxi Zone Lookup

Maps `PULocationID` / `DOLocationID` to readable locations. Expected columns: `LocationID`, `Borough`, `Zone`, `service_zone` (to be confirmed when the table is loaded in staging). The TLC user guide states that location IDs range from 1 to 263; rows outside this range and IDs without a match are checked in staging. Taxi zones approximate neighborhoods and are only roughly based on NYC Neighborhood Tabulation Areas.

## Known limitations

1. **Accuracy is not guaranteed.** The data is submitted by technology providers, not created by the TLC, and the TLC states it cannot guarantee its accuracy.
2. **Cash tips are not recorded.** `tip_amount` and `total_amount` exclude cash tips, so tip analysis is restricted to credit card payments (`payment_type = 1`).
3. **Passenger count is driver-entered** and may be less reliable than system-generated fields.
4. **Timestamps have no time zone.** Pickup and dropoff are `timestamp_ntz` **(observed)**: New York wall-clock time as recorded by the meter. They are not shifted by Spark's session time zone, so derived hours and dates are in New York local time.
5. **Schema can change between periods.** The official dictionary names the field `airport_fee`, while the January 2024 file has `Airport_fee` **(observed)**. Names and types are compared across the three months during profiling.
6. **Codes may appear that are not in the dictionary,** or new vendor codes may not appear at all. Code distributions are checked during profiling.
7. **Records are updated periodically** (the user guide mentions every six months), so a later download of the same month may differ. Compare sizes in `download_log.csv`.