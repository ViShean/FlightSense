# Flight Data Scraper

## Overview

This Python script is designed to scrape airline fleet data from [FlightRadar24](https://www.flightradar24.com/data/airlines/). Specifically, it scrapes detailed flight information for a given airline, extracts aircraft details, and saves the data into CSV files. The scraper works by first logging into the website, then navigating through the aircraft's details and flight history, gathering the relevant information.

The scraper handles multiple airlines and processes the data into clean CSV files, which can later be used for analysis or other purposes.

## Prerequisites

Before using this scraper, you will need to install the necessary dependencies:

```bash
pip install selenium tqdm pandas
```

Additionally, you will need a working installation of the Chrome WebDriver. You can download it from here.

Ensure that the chromedriver binary is in your system's PATH or specify its path directly in the script.

## Folder Structure  
The script assumes the following folder structure:
```project/
│
├── data/                    # Folder where the final CSV files will be stored
├── flights.csv              # CSV file that contains the flight data (if it exists)
├── scraper.py               # The main Python scraper script
└── UnScrapable.csv          # File to log planes that cannot be scraped
```

## Folder Details:
data/: This folder will hold the CSV files for each airline, named in the format {operator}_{airline}.csv.
flights.csv: This file stores flight information for all planes scraped, appending new data with each run. If the file does not exist, the script will create it.
UnScrapable.csv: This file logs any aircraft that the scraper cannot retrieve data for after a specified number of attempts.  

## Input Data 
1. Airline to Scrape:
The airlineToScrape list defines the airlines to scrape. You need to provide the airline code (e.g., jl-jal for Japan Airlines). This list can be expanded to include additional airlines.

```
airlineToScrape = ['jl-jal', 'sq-sia', 'nq-ajx']
```  
2. Login Credentials:
The script requires login credentials to access the flight data. Replace the following placeholders in the login method with valid credentials:

```
self.login("your_email@example.com", "your_password")
```



## Workflow
1. Login:
The script first logs into FlightRadar24 using the provided credentials.

2. Extract Aircraft Overview Information:
After logging in, the script navigates to the airline's fleet page, collects the list of aircraft, and extracts each aircraft's details, including its type code, operator, code, Mode S, serial number, and age.

3. Scraping Aircraft Details:
For each aircraft, the script navigates to its specific details page and attempts to retrieve flight history. It will keep loading earlier flights until no more data is available or a timeout occurs. If an aircraft's data cannot be retrieved after several attempts, it is logged in UnScrapable.csv.

4. Data Collection and Saving:
Flight data is collected and saved in a CSV file for each airline. The data for each plane is stored in the format:

- ```planeID```
- ```aircraftTypeCode```
- ```operator```
- ```code```
- ```modeS```
- ```serialNumber```
- ```age```
- Flight details such as date, departure, arrival, flight number, and status.
5. Final Output:  
After processing all the aircraft, the script renames the flights.csv file to the airline’s name, e.g., japan-airlines_jl-jal.csv, and saves it in the data/ folder.

Handling Errors:
If the scraper encounters issues with a particular aircraft (e.g., it cannot load data), the aircraft ID is logged in UnScrapable.csv.

## How to Use
1. **Update Airline List**:
Modify the ```airlineToScrape``` list to include the airline(s) you want to scrape.

2. **Run the Script**:
Run the script by executing:
```
python scraper.py
```
3. **Check Output**:
The scraped flight data will be saved in the data/ folder with filenames corresponding to the airline. If there were any issues scraping certain aircraft, they will be logged in UnScrapable.csv.


## Customization
- **Login Credentials**: You need to modify the `login` method with your own username and password for FlightRadar24.
- **Max Retry Attempts**: The script will retry loading data for a plane up to 100 times. If it still fails to retrieve the data, the plane ID is logged in `UnScrapable.csv`.
- **Airlines to Scrape**: You can add more airline codes to the `airlineToScrape` list to scrape additional fleets.
## Limitations
The script is designed for scraping flight data from FlightRadar24's fleet pages. If the structure of the website changes, the script may need adjustments.
The login method currently only works with FlightRadar24 and may need to be adjusted for other sites.