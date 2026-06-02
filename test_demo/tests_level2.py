import sys
import unittest
from pathlib import Path

import pandas as pd

# Allow this test file to import from the project root 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.app_refactored import (
    file_loader,
    remove_blank_rows,
    duplicate_check,
    na_check,
    data_enrich,
    clean_books_data,
    clean_customers_data,
    split_valid_invalid_books,
    split_valid_invalid_customers,
)


class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        self.books_path = PROJECT_ROOT / "data" / "03_Library Systembook.csv"
        self.customers_path = PROJECT_ROOT / "data" / "03_Library SystemCustomers.csv"

        self.books_raw = file_loader(self.books_path)
        self.customers_raw = file_loader(self.customers_path)

    def test_file_loader_loads_books_file(self):
        self.assertIsInstance(self.books_raw, pd.DataFrame)
        self.assertGreater(len(self.books_raw), 0)

    def test_file_loader_loads_customers_file(self):
        self.assertIsInstance(self.customers_raw, pd.DataFrame)
        self.assertGreater(len(self.customers_raw), 0)

    def test_remove_blank_rows_books(self):
        books_no_blank_rows = remove_blank_rows(self.books_raw)

        self.assertLess(len(books_no_blank_rows), len(self.books_raw))
        self.assertFalse(books_no_blank_rows.isna().all(axis=1).any())

    def test_duplicate_check_returns_integer(self):
        result = duplicate_check(self.books_raw)

        self.assertIsInstance(result, int)

    def test_na_check_returns_missing_count_column(self):
        result = na_check(self.books_raw)

        self.assertIn("missing_count", result.columns)

    def test_clean_books_data_adds_days_borrowed(self):
        books_clean = clean_books_data(self.books_raw)

        self.assertIn("days_borrowed", books_clean.columns)

    def test_clean_books_data_sets_date_types(self):
        books_clean = clean_books_data(self.books_raw)

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(books_clean["Book checkout"]))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(books_clean["Book Returned"]))

    def test_data_enrich_calculates_days_borrowed(self):
        test_df = pd.DataFrame({
        "checkout": pd.to_datetime(["2023-01-01"]),
        "returned": pd.to_datetime(["2023-01-10"])
        })

        result = data_enrich(test_df, "checkout", "returned")

        self.assertEqual(result.loc[0, "days_borrowed"], 9)

    def test_split_valid_invalid_books_row_counts_balance(self):
        books_clean = clean_books_data(self.books_raw)
        books_valid, books_invalid = split_valid_invalid_books(books_clean)

        self.assertEqual(len(books_clean), len(books_valid) + len(books_invalid))

    def test_books_valid_has_no_nulls(self):
        books_clean = clean_books_data(self.books_raw)
        books_valid, books_invalid = split_valid_invalid_books(books_clean)

        self.assertFalse(books_valid.isna().any().any())

    def test_books_valid_dates_are_between_2023_and_2026(self):
        books_clean = clean_books_data(self.books_raw)
        books_valid, books_invalid = split_valid_invalid_books(books_clean)

        self.assertTrue(books_valid["Book checkout"].dt.year.between(2023, 2026).all())
        self.assertTrue(books_valid["Book Returned"].dt.year.between(2023, 2026).all())

    def test_clean_customers_data_removes_blank_rows(self):
        customers_clean = clean_customers_data(self.customers_raw)

        self.assertFalse(customers_clean.isna().all(axis=1).any())

    def test_split_valid_invalid_customers_row_counts_balance(self):
        customers_clean = clean_customers_data(self.customers_raw)
        customers_valid, customers_invalid = split_valid_invalid_customers(customers_clean)

        self.assertEqual(len(customers_clean), len(customers_valid) + len(customers_invalid))


if __name__ == "__main__":
    unittest.main()