from pathlib import Path
from datetime import datetime
import time
import pandas as pd

from app_refactored import (
    file_loader,
    clean_books_data,
    clean_customers_data,
    split_valid_invalid_books,
    split_valid_invalid_customers,
    save_to_csv,
)

start_time = time.perf_counter()

data_dir = Path(__file__).resolve().parent / "data"

books_raw = file_loader(data_dir / "03_Library Systembook.csv") 
customers_raw = file_loader(data_dir / "03_Library SystemCustomers.csv")

books_clean = clean_books_data(books_raw) 
customers_clean = clean_customers_data(customers_raw)

books_valid, books_invalid = split_valid_invalid_books(books_clean)
customers_valid, customers_invalid = split_valid_invalid_customers(customers_clean)

save_to_csv(books_valid, data_dir / "books_valid.csv") 
save_to_csv(books_invalid, data_dir / "books_invalid.csv") 
save_to_csv(customers_valid, data_dir / "customers_valid.csv") 
save_to_csv(customers_invalid, data_dir / "customers_invalid.csv")

books_with_customers = books_valid.merge(
    customers_valid,
    on="Customer ID",
    how="left"
)

save_to_csv(books_with_customers, data_dir / "books_with_customers.csv")

end_time = time.perf_counter()
execution_time = round(end_time - start_time, 4)

dataset_summary = pd.DataFrame([
    {
        "dataset": "Books",
        "raw_rows": len(books_raw),
        "blank_rows_removed": len(books_raw) - len(books_clean),
        "processed_rows": len(books_clean),
        "valid_rows": len(books_valid),
        "dropped_rows": len(books_invalid),
    },
    {
        "dataset": "Customers",
        "raw_rows": len(customers_raw),
        "blank_rows_removed": len(customers_raw) - len(customers_clean),
        "processed_rows": len(customers_clean),
        "valid_rows": len(customers_valid),
        "dropped_rows": len(customers_invalid),
    }
])

pipeline_metrics = pd.DataFrame([{
    "run_datetime": datetime.now(),
    "pipeline_execution_time_seconds": execution_time,
    "total_records_processed": dataset_summary["processed_rows"].sum(),
    "total_records_dropped": dataset_summary["dropped_rows"].sum(),
    "total_blank_rows_removed": dataset_summary["blank_rows_removed"].sum(),
    "total_valid_records": dataset_summary["valid_rows"].sum(),
}])

save_to_csv(dataset_summary, data_dir / "dataset_summary.csv") 
save_to_csv(pipeline_metrics, data_dir / "pipeline_metrics.csv")

print("Dashboard metric files created successfully.")
print(dataset_summary)
print(pipeline_metrics)