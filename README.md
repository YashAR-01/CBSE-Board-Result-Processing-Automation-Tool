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

### Sample Output — `result.csv` (default sort: Roll Number)

| RollNo | Gender | name | stream | English_Marks | English_Grade | Maths_Marks | Maths_Grade | Physics_Marks | Physics_Grade | Chemistry_Marks | Chemistry_Grade | Physical_Education_Marks | Physical_Education_Grade | Computer_Science_Marks | Computer_Science_Grade | Economics_Marks | Economics_Grade | Business_Studies_Marks | Business_Studies_Grade | Accounts_Marks | Accounts_Grade | Psychology_Marks | Psychology_Grade | Biology_Marks | Biology_Grade | BEST_4 | ALL_SUB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12111 | M | ABC D E F | Med_Science | 97 | A1 | | | 92 | A1 | 95 | A1 | 97 | A1 | | | | | | | | | | | 93 | A1 | 95.5 | 94.8 |
| 12145 | M | AB CD EF | Commerce | 80 | B2 | | | | | | | 84 | B1 | | | 80 | B1 | 92 | A1 | 66 | B2 | | | | | 84.0 | 80.4 |
| 12245 | M | ABCDEF | Commerce | 86 | B1 | 85 | A2 | | | | | | | | | 91 | A1 | 98 | A1 | 94 | A1 | | | | | 92.25 | 90.8 |
| 12305 | M | ABCDEF | Commerce | 91 | A2 | 98 | A1 | | | | | | | | | 93 | A1 | 98 | A1 | 98 | A1 | | | | | 96.75 | 95.6 |
| 12315 | M | ABCDEF | Science | 83 | B1 | 75 | A2 | 68 | B1 | 60 | C1 | 87 | A2 | | | | | | | | | | | | | 78.25 | 74.59 |
| 12325 | M | ABCDEF | Science | 95 | A1 | 73 | B1 | 61 | C1 | 67 | B2 | 89 | A2 | 85 | B1 | | | | | | | | | | | 85.5 | 78.33 |

### Sample Output — `Science_result.csv` (sorted by BEST_4, descending)

| RollNo | Gender | name | stream | English_Marks | English_Grade | Maths_Marks | Maths_Grade | Physics_Marks | Physics_Grade | Chemistry_Marks | Chemistry_Grade | Physical_Education_Marks | Physical_Education_Grade | Computer_Science_Marks | Computer_Science_Grade | BEST_4 | ALL_SUB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12335 | M | ABCDEF | Science | 96 | A1 | 98 | A1 | 68 | B1 | 95 | A1 | | | 98 | A1 | 96.75 | 91.0 |
| 12348 | M | ABCDEF | Science | 87 | A2 | 97 | A1 | 69 | B1 | 77 | B1 | 87 | A2 | | | 87.0 | 83.4 |
| 12325 | M | ABCDEF | Science | 95 | A1 | 73 | B1 | 61 | C1 | 67 | B2 | 89 | A2 | 85 | B1 | 85.5 | 78.33 |
| 12385 | M | ABCDEF | Science | 87 | A2 | 74 | B1 | 75 | A2 | 79 | B1 | 90 | A1 | | | 82.75 | 81.0 |
| 12365 | M | ABCDEF | Science | 97 | A1 | 73 | B1 | 66 | B2 | 60 | C1 | | | 87 | B1 | 80.75 | 76.59 |
| 12347 | M | ABC DEF | Science | 90 | A2 | 65 | B2 | 73 | B1 | 68 | B2 | 83 | B1 | | | 78.5 | 75.8 |

*Names and roll numbers above are placeholders — real student data should never be committed to a public repository.*

## Known Limitations
  - The parsing logic is written for CBSE's current result text format — if CBSE changes the structure/layout of the raw data, the cleaning step will likely break and need to be updated
  - Resets (`DROP DATABASE`) the database on every run — do not run against data you want to preserve without backing it up first

## Future Additions

- Subject-wise pass percentage and distribution charts
- Visualizations (graphs/dashboards) built on top of the existing processed data

## Note

Change your credentials for mysql connector in line 85 i.e host,username and password before running the programs
