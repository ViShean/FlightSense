## Scrapping_airlines.py
Automates a browser session with Selenium to log in to a flight tracking site, scrape aircraft details and flight history for multiple airlines, and save the data to CSV files. It tracks progress in a JSON file so it can resume without re-scraping data.

## Verification Checking Script
Reads the scraped aircraft data from the collection folders and compares it against a list of expected aircraft registrations from verification files. It validates whether each aircraft has enough flight history (using a cutoff date) and then updates the CSV files by removing entries with insufficient data. Unmatched registrations and airlines are saved to a final CSV and a text file for further review.
