# Scraped Data Processing

## Overview

The goal of this notebook is to process and clean two datasets that were retrieved using two separate scrapers. Each scraper collected flight data, but the data had varying structures and fields. This notebook is designed to handle the data from both scrapers, clean and merge them into a unified dataset for further analysis.  

Due to storage limitations on GitHub, the actual data files will **NOT** be showcased here. This README will serve as a walkthrough of what the script is doing in processing and cleaning the datasets.

## Process Overview

1. **Processing Data from Scraper 1:**
   The data collected by Scraper 1 is the first to be processed. It is gathered in a single file, where all the flight-related information collected by Scraper 1 is consolidated into one dataset.

2. **Processing Data from Scraper 2:**
   Similarly, Scraper 2 collects its own set of flight data, which may differ in terms of the fields and structure. Once the data from Scraper 2 is collected, it is saved into a separate file for further processing.

3. **Cleaning and Merging the Data:**
   After both datasets have been prepared, the notebook cleans the data from both scrapers by:
   - Ensuring consistent data types.
   - Handling missing or inconsistent values.
   - Standardizing field names and structures.

   Once the datasets are cleaned, they are merged into a single unified dataset. The merging process ensures that relevant fields from both datasets are properly aligned, allowing for comprehensive analysis.

## Input Data

- **Scraper 1 Output:** Contains flight data collected by the first scraper.
- **Scraper 2 Output:** Contains flight data collected by the second scraper, which may have different fields and structures compared to the first scraper.

## Cleaning and Merging Process

The process involves the following steps:

1. **Collating Data from Scraper 1:**  
   All data collected by Scraper 1 is combined into one file. This ensures that the data is organized and ready for further processing.

2. **Collating Data from Scraper 2:**  
   Similarly, data from Scraper 2 is collated into a separate file. Since the data collected by this scraper may be in a different format or structure, it is stored separately before being cleaned and merged.

3. **Data Cleaning:**  
   Once the data from both scrapers is prepared, the next step is cleaning the data to ensure consistency. This includes:
   - Correcting data types for fields like dates, flight numbers, etc.
   - Handling any missing or inconsistent values in the datasets.
   - Standardizing column names and structures across both datasets.

4. **Merging the Data:**  
   After cleaning, the data from both scrapers is merged into a single dataset, ensuring that all relevant information is combined and aligned correctly.

5. **Processing the Data:**
   After the initial  cleaning phase, date time processing of ATA,ATD,STA,STD were initiated in Proj_Clean_3.ipynb

6. **Merging of weather data**
   After the processing of date times, weather data attained from meteo stat was merged into 1 dataset

7. **Further Cleaning**
   Data Types were then converted, null values were handled accordingly which differed for different models.

## Output

The final output is a single, cleaned, and merged dataset that combines the flight data from both scrapers. This dataset is ready for further analysis or visualization to explore trends, flight statuses, schedules, and other insights.

