## Scrapping_airlines.py

Automates a browser session using Selenium to:
- **Log in** to a flight tracking site.
- **Scrape** aircraft details and flight history for multiple airlines.
- **Save** the scraped data to CSV files.
- **Track progress** using a JSON file, enabling the script to resume without re-scraping data.

---

## validation_checker.py

Processes and validates the scraped data by:
- Reading the scraped flight data from the **Collection Folder**.
- Comparing the data against expected aircraft registrations listed in CSV files within the **Verify Folder**.
- Validating that each aircraft has sufficient flight history based on a predefined cutoff date.
- Updating the CSV files by removing entries with insufficient data.
- Saving unmatched registrations and airlines to:
  - A final CSV file.
  - A text file for further review.

---

### Folder Structure

- **Verify Folder**:  
  Contains CSV files with aircraft registration codes for verification checks.

- **Collection Folder**:  
  Holds all the scraped flight data for various airlines.

- **Output Folder**:  
  Stores the results of the validation process, including:
  - CSV file(s) for unmatched aircraft.
  - A text file for unmatched airlines.
