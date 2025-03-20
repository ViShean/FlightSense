Below is a sample README that explains what the script does:

---

# Flight Data Scraper

This Python script is designed to scrape aircraft data from a flight tracking website (flightradar24.com) for various airlines. It automates the following processes:

## Overview

- **Automated Browser Interaction:** Uses Selenium to simulate a human-like browsing session to log in, navigate pages, and interact with website elements.
- **Data Extraction:** Scrapes aircraft details and flight history from each aircraft’s dedicated page.
- **Progress Tracking:** Saves progress in a JSON file to resume scraping without duplicating work.
- **CSV Output:** Writes the extracted data to CSV files for each airline based on its airline code.

## Key Features

1. **Configuration:**
   - **Output Directory & Files:** Specify where the scraped data and progress file will be stored.
   - **Airline List:** Reads a list of airline codes from a text file.
   - **Chromedriver Path:** Update the script with the correct path to the Chromedriver executable.

2. **Login and Session Management:**
   - Implements a login flow with error handling to manage issues like maintenance messages or failed logins.
   - Uses Selenium’s WebDriver and waits to ensure the page elements are available before interaction.
   - Detects and handles website maintenance interruptions by refreshing the page and retrying.

3. **Scraping Logic:**
   - **Aircraft Links:** The script collects all aircraft links for a given airline by parsing the fleet page.
   - **Data Extraction:** For each aircraft, the script navigates to the aircraft’s page, scrolls in a human-like manner, and clicks on elements (e.g., "Load earlier flights") to reveal historical flight data.
   - **HTML Parsing:** Uses BeautifulSoup to parse the page source and extract aircraft information (such as aircraft name, airline, operator, type code, etc.) and flight history details.
   - **CSV Writing:** Data is written to a CSV file corresponding to each airline, ensuring that duplicate entries (based on aircraft registration) are skipped.

4. **Progress Saving:**
   - Progress is tracked and stored in a JSON file so that if the script is interrupted, it can resume without re-scraping data that has already been collected.
   - After processing each aircraft, the progress is updated and saved.

5. **Tab Management:**
   - The script manages multiple browser tabs to efficiently switch between airlines.
   - It opens a new tab for the next airline once data scraping for the current airline is complete, then closes the previous tab to conserve resources.

## Usage

1. **Update Paths:**  
   - Set the `base_output_dir`, `airline_list_file`, and `chromedriver_path` to match your environment.

2. **Run the Script:**  
   - Execute the script using Python. It will open a browser window, perform the login process, and start scraping data for each airline.
   - Progress is continuously saved in the `progress.json` file located in the output directory.

3. **Review Output:**  
   - Scraped data for each airline is saved in a CSV file within a subdirectory named after the airline code.
   - Check the CSV files and the progress JSON file to verify the scraping process.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup (bs4)
- Chrome and Chromedriver

## Notes

- **Error Handling:** The script includes error handling for maintenance messages and retries when elements are not clickable.
- **Human-like Behavior:** Implements random delays and incremental scrolling to mimic human interaction and avoid potential scraping blocks.

---

This README should provide users with a clear understanding of what the script does and how to configure and run it. Feel free to adjust any sections to better fit your project specifics!
