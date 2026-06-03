from pathlib import Path

from app_refactored import (
    file_loader,
    clean_books_data,
    clean_customers_data,
    split_valid_invalid_books,
    split_valid_invalid_customers,
    save_to_csv,
)

input_dir = Path("/app/data")
output_dir = Path("/data/cleaned")

output_dir.mkdir(parents=True, exist_ok=True)

books_raw = file_loader(input_dir / "03_Library Systembook.csv") 
customers_raw = file_loader(input_dir / "03_Library SystemCustomers.csv")

books_clean = clean_books_data(books_raw) 
customers_clean = clean_customers_data(customers_raw)

books_valid, books_invalid = split_valid_invalid_books(books_clean)
customers_valid, customers_invalid = split_valid_invalid_customers(customers_clean)

save_to_csv(books_valid, output_dir / "books_valid.csv") 
save_to_csv(books_invalid, output_dir / "books_invalid.csv") 
save_to_csv(customers_valid, output_dir / "customers_valid.csv") 
save_to_csv(customers_invalid, output_dir / "customers_invalid.csv")

print("Data cleaner completed successfully.") 
print(f"Books valid rows: {len(books_valid)}") 
print(f"Books invalid rows: {len(books_invalid)}") 
print(f"Customers valid rows: {len(customers_valid)}") 
print(f"Customers invalid rows: {len(customers_invalid)}") 
print("Cleaned files written to Docker volume at /data/cleaned")

