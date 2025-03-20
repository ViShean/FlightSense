# FlightSense

## Overview
The datasets in this repository contain flight records for various airlines. Each dataset represents one year’s worth of flight history for all registered planes of a given airline.

## Data Source
This data has been collected using Flightradar24 and extracted through our custom Python script with Selenium automation.

## Structure
- Each airline has its own subfolder.
- Inside each subfolder, there is a CSV file containing detailed flight records.
- If a dataset exceeds a certain size, it is split into smaller parts to ensure manageability.
- To abide by GitHub's file limit, the CSVs have been split into chunks.

## Usage
This dataset can be used for:
- Analyzing flight patterns and trends.
- Monitoring airline performance over the past year.
- Conducting research on aircraft utilization.

## Merging CSV Files
Please run the `Airlines_Raw_Data_Management` Python notebook provided:
1. Execute **Cell 1** to install dependencies and load necessary functions.
2. Execute **Cell 3** to merge split CSV files back in subfolders.

## Disclaimer

This dataset belongs to P5 - Group 14, FlightSense. Unauthorized redistribution or commercial use is not permitted.

## Note
This dataset was extracted and processed using a Python-based automation script leveraging Selenium to scrape data from Flightradar24.

