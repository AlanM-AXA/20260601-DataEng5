# 20260601-DataEng5

Data Engineering Apprenticeship Activity 5 project.

Scenario: Library wants to automate their data usage and analysis. The solution should automatically take the source data, transform it, validate it, and make it ready for analysis.

User Story / Backlog: As a user, I want to reduce the number of manual tasks I am required to do so that it will free up time in my schedule.

Solution Diagram: guidance/solution_diagram.pdf

Trainer's GitHub: https://github.com/niroshsuthagar-QA/20260601-DE5M5/tree/main

---

## Project Overview

This project demonstrates a small end-to-end data engineering workflow using Python, pandas, unit testing, Docker, Docker volumes, GitHub Actions, Power BI, and Apache Airflow.

The project uses two source CSV files:

- Library book borrowing data
- Library customer data

The pipeline loads the raw CSV files, cleans the data, validates the data, separates valid and invalid records, creates dashboard-ready outputs, and supports automated testing and containerisation.

---

## Project Structure

```text
20260601-DataEng5/
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── app/
│   ├── app_refactored.py
│   ├── dashboard_metrics.py
│   ├── requirements.txt
│   └── data/
│       ├── 03_Library Systembook.csv
│       ├── 03_Library SystemCustomers.csv
│       ├── books_valid.csv
│       ├── books_invalid.csv
│       ├── customers_valid.csv
│       ├── customers_invalid.csv
│       ├── books_with_customers.csv
│       ├── dataset_summary.csv
│       └── pipeline_metrics.csv
│
├── archive/
│   ├── eda.ipynb
│   └── eda2.ipynb
│
├── docker_demo/
│   ├── Dockerfile
│   ├── calc.py
│   ├── hello.py
│   └── run_calculator.py
│
├── docker_volume_demo/
│   ├── Dockerfile
│   └── hello-volume.py
│
├── docker-cleaner/
│   ├── Dockerfile
│   ├── app_refactored.py
│   ├── requirements.txt
│   ├── run_cleaner.py
│   └── data/
│
├── airflow_demo/
│   ├── docker-compose.yaml
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   └── config/
│
├── guidance/
│   └── solution_diagram.pdf
│
├── tests_demo/
│   ├── calc.py
│   ├── tests_level1.py
│   └── tests_level2.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Main Data-Cleaning Application

The main reusable data-cleaning code is stored in:

```text
app/app_refactored.py
```

This file contains functions for:

- Loading CSV files
- Removing blank rows
- Checking duplicate records
- Checking missing values
- Cleaning book data
- Cleaning customer data
- Converting date columns
- Calculating days borrowed
- Splitting valid and invalid records
- Saving cleaned outputs to CSV

The main cleaned output files are stored in:

```text
app/data/
```

---

## Data Cleaning Rules

Book records are treated as invalid if they contain:

- Any null values
- Missing or invalid dates
- Dates before 2023
- Dates after 2026

The book data is also enriched with a calculated `days_borrowed` column.

The output files include:

```text
app/data/books_valid.csv
app/data/books_invalid.csv
app/data/customers_valid.csv
app/data/customers_invalid.csv
```

---

## Unit testing
Automated tests were created using Python `unittest`.

The test files are stored in:

```text
tests_demo/
```

The calculator test file is:

```text
tests_demo/tests_level1.py
```

The data-cleaning test file is:

```text
tests_demo/tests_level2.py
```

The data-cleaning tests check:

- File loading
- Blank row removal
- Duplicate checking
- Missing value checking
- Date conversion
- Days borrowed calculation
- Valid and invalid record splitting

Run the tests locally with:

```powershell
python -m unittest discover -s tests_demo
```

---

## Docker workflow
### Docker Calculator Demo

A simple Docker container was created in:

```text
docker_demo/
```

This container runs a calculator script that calculates:

```text
144 / 12 = 12
```

This demonstrated how to package and run simple Python code inside Docker.

### Docker Volume Demo

A Docker volume demo was created in:

```text
docker_volume_demo/
```

This container writes a timestamped text file to a mounted Docker volume at:

```text
/data/logs/hello.txt
```

This proved that data written to a Docker volume persists after the container finishes.

### Docker Cleaner App

A Docker container was also created for the data-cleaning application in:

```text
docker-cleaner/
```

This container:

1. Loads the raw library CSV files.
2. Runs the cleaning and validation logic.
3. Splits valid and invalid records.
4. Writes four cleaned CSV files into a mounted Docker volume.

The cleaned files are written to:

```text
/data/cleaned
```

---

## GitHub Actions CI Pipeline

A GitHub Actions workflow was added in:

```text
.github/workflows/python-app.yml
```

The workflow runs automatically when changes are pushed to GitHub.

It performs the following steps:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from the root `requirements.txt`.
4. Runs the unit tests in `tests_demo`.

The latest GitHub Actions workflow run passed successfully.

---

## Power BI Dashboard

Dashboard-ready output files were created using:

```text
app/dashboard_metrics.py
```

This script creates:

```text
app/data/dataset_summary.csv
app/data/pipeline_metrics.csv
app/data/books_with_customers.csv
```

These files were loaded into Power BI to create a dashboard showing:

- Number of records processed
- Number of records dropped
- Books and customer data
- Pipeline execution time

A calculated column was also added in Power BI to check the return status:

- If `days_borrowed` is negative, the record is marked as `Check dates`
- Otherwise, the record is marked as `Returned`

A separate measures table was also created in Power BI to organise the dashboard measures.

---

## Apache Airflow Stretch Task

Apache Airflow was run on the virtual machine using Docker Compose.

The Airflow setup is stored in:

```text
airflow_demo/
```

The setup included:

- Creating the required Airflow folders
- Adding the Docker Compose file
- Creating the `.env` file
- Running the Airflow initialisation step
- Starting the Airflow services using Docker Compose
- Accessing the Airflow web interface

Commands used included:

```powershell
docker compose up airflow-init
docker compose up -d
docker compose ps
```

The Airflow web interface loaded successfully at:

```text
http://localhost:8080
```

Login to the Airflow web UI was successful.

Airflow is a workflow orchestration tool. In this project, it could be used to schedule and monitor the data-cleaning pipeline rather than running the Python scripts manually.

---

## Useful Commands

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run tests:

```powershell
python -m unittest discover -s tests_demo
```

Run the dashboard metrics script:

```powershell
python app\dashboard_metrics.py
```

Run the Docker cleaner app:

```powershell
cd docker-cleaner
docker build -t cleanerapp .
docker run --rm -v cleanerdata:/data cleanerapp
```

Run Airflow:

```powershell
cd airflow_demo
docker compose up -d
```

Stop Airflow:

```powershell
docker compose down
```

---

## Summary of Work Completed

During this project, I completed the following:

1. Loaded raw CSV data using Python and pandas.
2. Cleaned and validated the library book and customer datasets.
3. Separated valid and invalid records.
4. Refactored notebook logic into reusable Python functions.
5. Created automated unit tests for the data-cleaning logic.
6. Organised the project folder structure.
7. Created Docker containers for Python scripts and the data-cleaning app.
8. Used Docker volumes to persist output data.
9. Added a GitHub Actions CI pipeline to run tests automatically.
10. Created dashboard-ready CSV outputs.
11. Built a simple Power BI dashboard.
12. Ran Apache Airflow locally using Docker Compose.
13. Committed and pushed the completed work to GitHub.
