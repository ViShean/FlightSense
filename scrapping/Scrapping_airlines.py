import os
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import random

# --- CONFIGURABLE PARTS ---
base_output_dir = r"C:\Users\Lim Vi Shean\Downloads\Telegram Desktop\hello\hello\Collection"
airline_list_file = r"c:\Users\Lim Vi Shean\Downloads\Telegram Desktop\hello\hello\Output\unmatched_airlines.txt"  # TODO: Update path to the airline list file
progress_json_file = os.path.join(base_output_dir, "progress.json")

# Load or initialize progress tracking structure
if os.path.exists(progress_json_file):
    with open(progress_json_file, 'r') as f:
        progress_data = json.load(f)
else:
    progress_data = {}  # Structure: { airline_code: { "completed_registrations": [] } }

def save_progress():
    with open(progress_json_file, 'w') as f:
        json.dump(progress_data, f, indent=2)
    print(f"Progress saved to {progress_json_file}")

def load_airline_codes(filepath):
    airline_codes = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            for part in parts:
                part = part.strip()
                if part.startswith("Airline Code:"):
                    code = part.split("Airline Code:")[1].strip()
                    airline_codes.append(code)
    return airline_codes

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--log-level=3")

    chromedriver_path = r"C:\Users\G5\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Update path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome( options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def check_login_status(driver):
    try:
        gold_element = driver.find_element(By.XPATH, "//span[contains(text(), 'gold')]")
        return True
    except NoSuchElementException:
        return False

def login_flow(driver, wait, url, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            try:
                accept_button = wait.until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                accept_button.click()
                print("Clicked cookie consent.")
            except Exception:
                print("Cookie consent not found.")
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "auth-button")))
            login_button.click()
            print("Clicked login button.")
            email_input = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="email"]'))
            )
            email_input.send_keys("jinbethewhale@gmail.com")
            password_input = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="password"]')
            password_input.send_keys("jinbe22400149google")
            login_submit_button = driver.find_element(
                By.CSS_SELECTOR, 'button[data-testid="login__submit-button"]'
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", login_submit_button)
            time.sleep(1)
            login_submit_button.click()
            print("Submitted login form.")
            time.sleep(5)
            if "We'll be back shortly" in driver.page_source:
                print("Detected maintenance message. Retrying...")
                driver.refresh()
                time.sleep(5)
                attempts += 1
                continue
            else:
                break
        except Exception as e:
            if "We'll be back shortly" in driver.page_source:
                print("Maintenance message detected during exception. Retrying...")
                driver.refresh()
                time.sleep(5)
                attempts += 1
            else:
                print(f"Login error: {e}")
                attempts += 1


def check_if_registration_exists(filename, registration):
    """Check if the aircraft registration already exists in the CSV file."""
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:  # Open in read mode
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[1] == registration:  # Assuming registration is in column 1
                return True
    return False

def human_like_scroll_and_click(driver, element):
    # Get the element's location on the page
    location = element.location_once_scrolled_into_view
    current_position = driver.execute_script("return window.pageYOffset;")
    
    # Determine how far we need to scroll
    target_position = location['y']
    distance = target_position - current_position

    # Scroll in increments if distance is significant
    if abs(distance) > 300:  # threshold for incremental scrolling
        step = distance / 10.0  # break distance into 10 steps
        for _ in range(10):
            driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(random.uniform(0.2, 0.5))  # random small delay between scrolls
    else:
        # If close enough, scroll directly into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(random.uniform(0.2, 0.5))

    # Hover over the element before clicking
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.3, 0.7)).click().perform()

def scrape_one_aircraft_link(driver, wait, writer, csv_headers, aircraft_link, airlinecode):
    aircraft_registration = aircraft_link.split('/')[-1]
    full_url = f"https://www.flightradar24.com{aircraft_link}"
    print(f"\nScraping: {full_url}")
    driver.get(full_url)
    time.sleep(3)

    if "We'll be back shortly" in driver.page_source:
        driver.refresh()
        time.sleep(5)
        raise RuntimeError("Maintenance detected during aircraft page load.")

    max_retries = 3
    retry_count = 0
    while True:
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.ID, "btn-load-earlier-flights"))
            )
            human_like_scroll_and_click(driver, button)  # Use human-like behavior
            print("Clicked 'Load earlier flights' button.")
            time.sleep(random.uniform(1.5, 3))  # Random delay after click
            retry_count = 0
            if "We'll be back shortly" in driver.page_source:
                print("Maintenance message after clicking. Refreshing...")
                driver.refresh()
                time.sleep(5)
        except Exception as e:
            if "We'll be back shortly" in driver.page_source:
                driver.refresh()
                time.sleep(5)
            else:
                print("Click failed; checking button status...")
            try:
                button = driver.find_element(By.ID, "btn-load-earlier-flights")
                classes = button.get_attribute("class")
                if "loading" not in classes and (not button.is_enabled()):
                    print("No more flights to load.")
                    break
                time.sleep(2)
                if button.is_displayed():
                    retry_count += 1
                    print(f"Button visible but not clickable. Retry count = {retry_count}")
                    if retry_count >= max_retries:
                        raise RuntimeError("Max retries exceeded for 'load earlier flights'")
                    else:
                        continue
                else:
                    print("Button not displayed. Ending loop.")
                    break
            except Exception as e2:
                if isinstance(e2, RuntimeError):
                     raise RuntimeError("Max retries exceeded for 'load earlier flights'")
                else:
                    print("No more 'Load earlier flights' button found.")
                    break

    aircraft_page_source = driver.page_source
    aircraft_soup = BeautifulSoup(aircraft_page_source, 'html.parser')
    aircraft_info_div = aircraft_soup.find('div', id='cnt-aircraft-info')
    if aircraft_info_div:
        def safe_extract(label):
            try:
                return (
                    aircraft_info_div
                    .find('label', string=label)
                    .find_next('span')
                    .get_text(strip=True)
                )
            except AttributeError:
                return "N/A"

        aircraft_name = safe_extract('AIRCRAFT')
        airline = safe_extract('AIRLINE')
        operator = safe_extract('OPERATOR')
        type_code = safe_extract('TYPE CODE')
        mode_s = safe_extract('MODE S')
        serial_number = safe_extract('SERIAL NUMBER (MSN)')
        label_element_age = aircraft_info_div.find(
            'label',
            string=lambda string: string and 'age' in string.lower()
        )
        if label_element_age:
            span_element = label_element_age.find_next('span')
            age = span_element.get_text(strip=True) if span_element else "N/A"
        else:
            age = "N/A"
    else:
        print(f"No aircraft info found for {full_url}")
        aircraft_name = airline = operator = type_code = mode_s = serial_number = age = "N/A"

    table = aircraft_soup.find('table')
    if not table:
        print("No flight history table found.")
        return csv_headers

    if csv_headers is None:
        thead = table.find('thead')
        if thead:
            th_tags = thead.find_all('th')
            flight_headers = []
            for th in th_tags:
                if th.has_attr('class'):
                    if 'visible-xs' in th['class'] or 'visible-sm' in th['class']:
                        continue
                if th.get_text(strip=True):
                    flight_headers.append(th.get_text(strip=True))

            csv_headers = [
                "Airline Code",
                "Aircraft Registration",
                "Aircraft Link",
                "Aircraft",
                "Airline",
                "Operator",
                "Type Code",
                "Mode S",
                "Serial Number",
                "Age",
            ] + flight_headers + ["Color Code"]

            writer.writerow(csv_headers)
        else:
            print("No <thead> found. Skipping aircraft.")
            return csv_headers
    else:
        flight_headers_len = len(csv_headers) - 11

    tbody = table.find('tbody')
    if not tbody:
        print("No <tbody> found.")
        return csv_headers

    rows = tbody.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        row_data = []
        color_code = "N/A"

        for cell in cells:
            if cell.find('button'):
                continue
            if cell.has_attr('class'):
                classes = cell['class']
                if 'visible-xs' in classes or 'visible-sm' in classes:
                    continue
            state_block_div = cell.find('div', class_='state-block')
            if state_block_div:
                div_classes = state_block_div.get('class', [])
                possible_colors = [c for c in div_classes if c != 'state-block']
                if possible_colors:
                    color_code = possible_colors[0]
            text_val = cell.get_text(strip=True)
            if text_val:
                row_data.append(text_val)

        if not row_data:
            continue

        if csv_headers is not None:
            flight_headers_len = len(csv_headers) - 11
            if len(row_data) < flight_headers_len:
                row_data += [""] * (flight_headers_len - len(row_data))
            elif len(row_data) > flight_headers_len:
                row_data = row_data[:flight_headers_len]

        writer.writerow([airlinecode, aircraft_registration, full_url, aircraft_name, airline, operator, type_code, mode_s, serial_number, age] + row_data + [color_code])

    return csv_headers

# --- MAIN EXECUTION FLOW ---
all_airline_codes = load_airline_codes(airline_list_file)
driver, wait = create_driver()

for airlinecode in all_airline_codes:
    print(f"\nProcessing airline code: {airlinecode}")
    if airlinecode not in progress_data:
        progress_data[airlinecode] = {"completed_registrations": []}
    completed_registrations = set(progress_data[airlinecode]["completed_registrations"])

    output_dir = os.path.join(base_output_dir, airlinecode)
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{airlinecode}_aircraft_data.csv")

    url = f"https://www.flightradar24.com/data/airlines/{airlinecode}/fleet"

    while not check_login_status(driver):
        login_flow(driver, wait, url)

    driver.get(url)
    time.sleep(3)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    aircraft_links = [link['href'] for link in links if '/aircraft/' in link['href']]
    print(f"Total aircraft links found for {airlinecode}: {len(aircraft_links)}")

    csv_headers = None

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        for aircraft_link in aircraft_links:
            aircraft_registration = aircraft_link.split('/')[-1]

            if check_if_registration_exists(filename, aircraft_registration):
                print(f"Skipping already scraped registration: {aircraft_registration}")
                continue

            success = False
            while not success:
                try:
                    csv_headers = scrape_one_aircraft_link(driver, wait, writer, csv_headers, aircraft_link, airlinecode)
                    completed_registrations.add(aircraft_registration)
                    progress_data[airlinecode]["completed_registrations"] = list(completed_registrations)
                    save_progress()  # Save to JSON file
                    success = True

                except RuntimeError as ex:
                        print(f"[!] {ex}. Opening a new tab and closing the old one to retry...")
                        # Store the current window handle to close it later
                        old_window = driver.current_window_handle

                        # Open a new tab
                        driver.execute_script("window.open('');")
                        time.sleep(1)  # Brief pause to ensure new tab opens

                        # Switch to the new tab
                        new_window = [window for window in driver.window_handles if window != old_window][0]
                        driver.switch_to.window(new_window)

                        # Close the old tab
                        driver.switch_to.window(old_window)
                        driver.close()

                        # Switch back to the new tab now that old tab is closed
                        driver.switch_to.window(new_window)
                        # Retry loading the URL in the new tab
                        driver.get(url)
                        time.sleep(3)
                        # Re-login or reinitialize the session if needed on the new tab
                        while not check_login_status(driver):
                            login_flow(driver, wait, url)

                        

                except Exception as e:
                    print(f"[!] Other exception: {e}")
                    success = True
    print(f"\nAll data for airline {airlinecode} has been written to: {filename}")

    next_airline_exists = False
    for future_code in all_airline_codes[all_airline_codes.index(airlinecode)+1:]:
        next_airline_exists = True
        next_url = f"https://www.flightradar24.com/data/airlines/{future_code}/fleet"
        break

    if next_airline_exists:
        print(f"\nPreparing to switch to next airline tab...")
        old_window = driver.current_window_handle

        # Open a new tab
        driver.execute_script("window.open('');")
        time.sleep(1)

        # Identify the new tab handle
        new_window = [handle for handle in driver.window_handles if handle != old_window][0]

        # Switch to new tab
        driver.switch_to.window(new_window)

        # Close the old tab
        driver.switch_to.window(old_window)
        driver.close()

        # Switch back to the new tab
        driver.switch_to.window(new_window)

        # Load URL for the next airline
        driver.get(next_url)
        time.sleep(3)
    else:
        # No next airline; finish up
        print("No more airlines to process.")
driver.quit()

print("\nScraping complete for all airlines.")
