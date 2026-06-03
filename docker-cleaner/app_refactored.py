import pandas as pd


def file_loader(file_path):
    """Load a CSV file into a pandas dataframe."""
    return pd.read_csv(file_path)


def remove_blank_rows(df):
    """Remove rows where every column is blank."""
    return df.dropna(how="all").copy()


def duplicate_check(df):
    """Return duplicate row count."""
    return int(df.duplicated().sum())


def na_check(df):
    """Return missing value counts by column."""
    return df.isna().sum().to_frame("missing_count")


def data_enrich(df, checkout_col, returned_col):
    """
    Calculate the number of days between checkout and returned dates.
    Adds the result as a new column called days_borrowed.
    """
    df = df.copy()
    df["days_borrowed"] = (df[returned_col] - df[checkout_col]).dt.days
    return df


def clean_books_data(df):
    """Clean the books dataframe and set correct data types."""
    df = remove_blank_rows(df)

    df["Books"] = df["Books"].astype("string").str.strip()
    df["Days allowed to borrow"] = df["Days allowed to borrow"].astype("string").str.strip()

    df["Id"] = pd.to_numeric(df["Id"], errors="coerce").astype("Int64")
    df["Customer ID"] = pd.to_numeric(df["Customer ID"], errors="coerce").astype("Int64")

    df["Book checkout"] = (
        df["Book checkout"]
        .astype("string")
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    df["Book Returned"] = (
        df["Book Returned"]
        .astype("string")
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    df["Book checkout"] = pd.to_datetime(
        df["Book checkout"],
        errors="coerce",
        dayfirst=True
    )

    df["Book Returned"] = pd.to_datetime(
        df["Book Returned"],
        errors="coerce",
        dayfirst=True
    )

    df = data_enrich(df, "Book checkout", "Book Returned")

    return df


def clean_customers_data(df):
    """Clean the customers dataframe and set correct data types."""
    df = remove_blank_rows(df)

    df["Customer ID"] = pd.to_numeric(
        df["Customer ID"],
        errors="coerce"
    ).astype("Int64")

    df["Customer Name"] = (
    df["Customer Name"]
    .astype("string")
    .str.strip()
    )

    return df


def split_valid_invalid_books(df):
    """
    Split books data into valid and invalid dataframes.

    Invalid if:
    - any column contains null
    - checkout date is missing/invalid
    - returned date is missing/invalid
    - checkout or returned date is before 2023 or after 2026
    """
    date_columns = ["Book checkout", "Book Returned"]

    null_mask = df.isna().any(axis=1)

    invalid_date_mask = pd.Series(False, index=df.index)

    for col in date_columns:
        invalid_date_mask = (
            invalid_date_mask
            | df[col].isna()
            | (df[col].dt.year < 2023)
            | (df[col].dt.year > 2026)
        )

    invalid_mask = null_mask | invalid_date_mask

    invalid_df = df[invalid_mask].copy()
    valid_df = df[~invalid_mask].copy()

    return valid_df, invalid_df


def split_valid_invalid_customers(df):
    """Split customers into valid and invalid dataframes based on null values."""
    invalid_mask = df.isna().any(axis=1)

    invalid_df = df[invalid_mask].copy()
    valid_df = df[~invalid_mask].copy()

    return valid_df, invalid_df


def save_to_csv(df, file_path):
    """Save dataframe to CSV without the index."""
    df.to_csv(file_path, index=False)
                                                                                                                                                        
                                        