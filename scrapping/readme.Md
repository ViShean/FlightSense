## Scrapping_airlines.py
Automates a browser session with Selenium to log in to a flight tracking site, scrape aircraft details and flight history for multiple airlines, and save the data to CSV files. It tracks progress in a JSON file so it can resume without re-scraping data.

## validaiton_checker.py
Reads the scraped aircraft data from the collection folders and compares it against a list of expected aircraft registrations from verification files. It validates whether each aircraft has enough flight history (using a cutoff date) and then updates the CSV files by removing entries with insufficient data. Unmatched registrations and airlines are saved to a final CSV and a text file for further review.

**Verify Folder**: Contains CSV files with aircraft registration codes for verification checks.\n
**Collection Folder**: Holds all the scraped flight data for various airlines. \n
**Output Folder**: Stores the results of the validation process, including CSV files for unmatched aircraft and a text file for unmatched airlines.\n 
