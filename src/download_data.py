"""Download the raw data used by the project into data/raw/.

Run from the repository root:
    python src/download_data.py

Files that are already in data/raw/ are skipped, so it is safe to run again.
"""

from pathlib import Path

import pandas as pd
import requests

# Folder where the raw files are saved (relative to the repository root)
RAW_DIR = Path("data/raw")

# Files to download: name on disk, source URL and period covered
FILES = [
    {
        "name": "yellow_tripdata_2024-01.parquet",
        "url": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
        "period": "2024-01",
    },
    {
        "name": "yellow_tripdata_2024-02.parquet",
        "url": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet",
        "period": "2024-02",
    },
    {
        "name": "yellow_tripdata_2024-03.parquet",
        "url": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet",
        "period": "2024-03",
    },
    {
        "name": "taxi_zone_lookup.csv",
        "url": "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv",
        "period": "reference table",
    },
]


def main() -> None:
    # 1. Create data/raw/ if it does not exist yet
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    log_rows = []

    # 2. Go through the files one by one
    for file_info in FILES:
        destination = RAW_DIR / file_info["name"]

        # 2a. Already downloaded: skip it
        if destination.exists():
            print(f"Skipping {file_info['name']} (already downloaded)")

        # 2b. Not downloaded yet: download it
        else:
            print(f"Downloading {file_info['name']} ...")
            response = requests.get(file_info["url"], timeout=120)

            # Stop with a clear error if the link is broken (404, 403...)
            response.raise_for_status()

            # Save under a temporary name first, and rename only at the end.
            # If the script is interrupted, no half-written file is left
            # with the final name (which step 2a would wrongly skip).
            temp_path = RAW_DIR / (file_info["name"] + ".part")
            temp_path.write_bytes(response.content)
            temp_path.rename(destination)

        # 2c. Record origin, period and size of the file
        size_mb = round(destination.stat().st_size / 1_000_000, 1)
        log_rows.append(
            {
                "file_name": file_info["name"],
                "source_url": file_info["url"],
                "period": file_info["period"],
                "size_mb": size_mb,
            }
        )

    # 3. Save the download log (one row per file) in data/raw/download_log.csv
    #    Each dictionary becomes a row; its keys become the columns.
    log_path = RAW_DIR / "download_log.csv"
    log_table = pd.DataFrame(log_rows)
    log_table.to_csv(log_path, index=False)  # index=False: no extra 0,1,2... column

    print(f"Done. Download log saved to {log_path}")


if __name__ == "__main__":
    main()