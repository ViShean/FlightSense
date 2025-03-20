# FlightSense

## Overview
This folder contains processed datasets used for training sequential models and a utility notebook for managing Parquet files.

## Usage

### CLEANED_V6.1
**Purpose:** Contains data that has been preprocessed and cleaned.  
**Usage:** This dataset is used for training the **departure model**.  
**Details:** All necessary cleaning and feature engineering for departure prediction has been completed.

### CLEANED_V9.1
**Purpose:** Contains data that is enhanced with predictions from the departure model.  
**Usage:** This dataset is used for training the **arrival model**.  
**Details:** The arrival model dataset includes additional features, such as the prediction outputs from the departure model, to improve the arrival prediction accuracy.

### Parquet_Data_Management.ipynb
This notebook splits large Parquet files into smaller chunks for easier management. To merge the split files back into a single dataset, simply run the **first and third cells** in the notebook.

## Note
To abide by GitHub's file size limit, the Parquet datasets have been split into smaller chunks. Use the provided notebook to restore the full dataset when needed.

## Data Source
The data was collected from Flightradar24 using a custom Python script with Selenium automation.

## Disclaimer
This dataset belongs to **P5 - Group 14, FlightSense**. Unauthorized redistribution or commercial use is not permitted.

## Note
This dataset was extracted and processed using a Python-based automation script leveraging Selenium to scrape data from Flightradar24.

