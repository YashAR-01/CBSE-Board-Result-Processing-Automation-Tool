# CBSE Board Result Processing & Automation Tool

A Python tool that automates the cleaning, structuring, and sorting of bulk CBSE board result data supplied to schools as raw text files. It converts messy text dumps into clean, queryable MySQL tables and exportable CSVs.

## Objective

CBSE sends bulk result data to schools in a raw, unstructured text format. This project automates the otherwise manual process of cleaning that data, organizing it by student and subject, computing performance metrics, and exporting sorted, ready-to-use CSV files — removing the need for manual spreadsheet work.

## Features

- Parses and cleans raw CBSE result text files
- Automatically maps subject codes to subject names
- Loads structured data into a MySQL database
- Classifies students into streams (Science, Med_Science, Commerce, Arts) based on subjects taken
- Computes **BEST_4** and **ALL_SUB** performance scores per student
- Computes **QPI** (Quality Performance Index) stream-wise and overall
- Generates stream-wise result tables
- Exports CSVs sorted by BEST_4, ALL_SUB, or Roll Number
- Interactive menu for selecting tables and export options

## Prerequisites

- Python 3.x
- MySQL Server installed and running locally
- mysql-connector-python package

## Required Files

Place these files in the same directory as the script before running:

| File | Description |
|---|---|
| `sample.txt` | Raw board result data as received from CBSE |
| `list of codes.csv` | Mapping of subject codes to subject names (2 columns: code, subject name) |


2. Ensure `sample.txt` and `list of codes.csv` are present in the project directory.

## Outputs

- `result.csv` and stream-wise CSVs (e.g. `Science_result.csv`, `Commerce_result.csv`) containing:
  - Roll number, gender, name, stream
  - Subject-wise marks and grades
  - BEST_4 and ALL_SUB scores

## Future Additions

- Subject-wise pass percentage and distribution charts
- Visualizations (graphs/dashboards) built on top of the existing processed data

## Note

Change your credentials for mysql connector i.e host,username and password before running the programs
