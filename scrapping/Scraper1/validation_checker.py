import os
import csv
import pandas as pd
# --- CONFIGURABLE PARTS ---
collection_folder = r"C:\Users\Lim Vi Shean\Downloads\Telegram Desktop\hello\hello\Collection"  # Update with the path to the Collection folder
verify_folder = r"C:\Users\Lim Vi Shean\Downloads\Telegram Desktop\hello\hello\Verify"  # Update with the path to the Verify folder
output_folder = os.path.join(os.getcwd(), "Output")
cutoff_date = pd.Timestamp("2024-01-31")


# Define the output file path
output_file = os.path.join(output_folder, "final_unmatched_aircraft.csv")
unmatched_airlines_file = os.path.join(output_folder, "unmatched_airlines.txt")
def read_aircraft_links(csv_file):
    """Read the aircraft registration codes from the verify CSV file."""
    registrations = set()
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if row:
                registrations.add(row[0].strip())  # Add the registration code
    return registrations

def read_aircraft_data(csv_file):
    """Read the aircraft data from the collection CSV file and store it in a dictionary."""
    aircraft_data = {}
    airline_name = ""
    airline_code = ""
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        for row in reader:
            if row:
                registration = row[1].strip()
                airline_code = row[0].strip()  # The airline code
                airline_name = row[4].strip()  # The airline name (from 'Airline' column)
                aircraft_data[registration] = row  # Store the whole row for matching
                rows.append(row)  # Keep track of all rows for later modifications
    return headers, airline_code, airline_name, aircraft_data, rows

def validate_aircraft_registration(aircraft_data, registration):
    """Validate whether an aircraft meets the criteria of flight history."""
    if registration not in aircraft_data:
        return False, "Does not exist"

    row = aircraft_data[registration]
    # Assuming 'DATE' is column index 10
    flight_dates = pd.to_datetime(row[10].split(';'), errors='coerce')

    # Check if the earliest flight date is <= cutoff_date
    if flight_dates.min() > cutoff_date:
        return False, "Less data"

    return True, ""
def write_unmatched_data(unmatched_data):
    """Write the unmatched data (registration, airline code, operator, and reason) into a final CSV file."""
    # Ensure the output folder exists, and create it if it doesn't
    os.makedirs(output_folder, exist_ok=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Airline Code", "Aircraft Registration", "Airline", "Reason"])  # Write headers
        for row in unmatched_data:
            writer.writerow(row)
    print(f"Unmatched aircraft registrations saved to {output_file}")

def write_unmatched_airlines(unmatched_data):
    """Write the unmatched airlines to a text file."""
    unmatched_airlines = set((row[2], row[0]) for row in unmatched_data)  # Airline name and code
    with open(unmatched_airlines_file, 'w', encoding='utf-8') as file:
        for airline_name, airline_code in unmatched_airlines:
            file.write(f"Airline: {airline_name}, Airline Code: {airline_code}\n")
    print(f"Unmatched airlines saved to {unmatched_airlines_file}")

def process_folder(folder_name, all_unmatched_data):
    """Process a specific airline folder."""
    # File paths
    links_csv_file = os.path.join(verify_folder, folder_name, f"{folder_name}_aircraft_links.csv")
    data_csv_file = os.path.join(collection_folder, folder_name, f"{folder_name}_aircraft_data.csv")

    # Step 1: Read aircraft registration links
    registrations = read_aircraft_links(links_csv_file)

    # Step 2: Read the aircraft data CSV and store it in a dictionary
    headers, airline_code, airline_name, aircraft_data, rows = read_aircraft_data(data_csv_file)

    # Step 3: Find unmatched registrations and remove rows with "Less data"
    unmatched = []
    valid_rows = []
    for registration in registrations:
        valid, reason = validate_aircraft_registration(aircraft_data, registration)
        if not valid:
            unmatched.append([airline_code, registration, airline_name, reason])  # Save airline code + registration + airline name + reason
            if reason == "Less data":
                rows = [row for row in rows if row[1].strip() != registration]  # Remove rows with "Less data"

    # Step 4: Write back the updated CSV without rows having "Less data"
    with open(data_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the header row
        writer.writerows(rows)  # Write the remaining rows

    if unmatched:
        all_unmatched_data.extend(unmatched)

# --- MAIN EXECUTION FLOW ---
def main():
    all_unmatched_data = []

    # Loop through each folder in the Collection folder
    for folder_name in os.listdir(collection_folder):
        folder_path = os.path.join(collection_folder, folder_name)
        
        # Ensure the folder exists in both 'Collection' and 'Verify'
        if os.path.isdir(folder_path) and os.path.isdir(os.path.join(verify_folder, folder_name)):
            print(f"Processing folder: {folder_name}")
            process_folder(folder_name, all_unmatched_data)
        else:
            print(f"Skipping folder {folder_name} (missing in either Collection or Verify folder)")

    # Write all unmatched data to the final CSV file
    if all_unmatched_data:
        write_unmatched_data(all_unmatched_data)
        write_unmatched_airlines(all_unmatched_data)
    else:
        print("No unmatched aircraft registrations found.")

# Run the main function
if __name__ == "__main__":
    main()
