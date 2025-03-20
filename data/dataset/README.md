# Dataset Versions & Parquet Management

This repository contains processed datasets used for training sequential models and a utility notebook for managing Parquet files.

## CLEANED_V6.1
**Purpose:** Contains data that has been preprocessed and cleaned.  
**Usage:** This dataset is used for training the **departure model**.  
**Details:** All necessary cleaning and feature engineering for departure prediction has been completed.

## CLEANED_V9.1
**Purpose:** Contains data that is enhanced with predictions from the departure model.  
**Usage:** This dataset is used for training the **arrival model**.  
**Details:** The arrival model dataset includes additional features, such as the prediction outputs from the departure model, to improve the arrival prediction accuracy.

## Parquet_Data_Management.ipynb
This notebook splits large Parquet files into smaller chunks for easier management. To merge the split files back into a single dataset, simply run the **first and third cells** in the notebook.
