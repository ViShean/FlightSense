import os
import pandas as pd

def checkForNonJan():
    # Directory containing the CSV files
    data_folder = "data/"
    results = []

    # Loop through all files in the folder
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):  # Check if the file is a CSV
            file_path = os.path.join(data_folder, file)
            
            # Load the dataset
            df = pd.read_csv(file_path)
            
            # Strip spaces from planeID for consistency
            df['planeID'] = df['planeID'].str.strip()
            
            # Identify planeIDs that have "Jan 2024" entries
            planeIDs_with_jan2024 = df[df['DATE'].str.contains("Jan 2024", case=False, na=False)]['planeID'].unique()
            
            # Identify all unique planeIDs in the dataset
            all_planeIDs = df['planeID'].unique()
            
            # Find planeIDs without "Jan 2024" entries
            planeIDs_without_jan2024 = [plane for plane in all_planeIDs if plane not in planeIDs_with_jan2024]
            
            # Store results for the current file
            results.append({
                "file_name": file,
                "total_planeIDs": len(all_planeIDs),
                "planeIDs_without_jan2024": len(planeIDs_without_jan2024),
                "planeIDs_with_jan2024": len(planeIDs_with_jan2024),
                "planeIDs_without_jan2024_list": planeIDs_without_jan2024
            })

    # Convert results to a DataFrame for better readability
    results_df = pd.DataFrame(results)
    print (results_df) 
    # Save the results to a CSV file 
    results_df.to_csv("data/results.csv", index=False) 


#! wont work cos its row based, it looks at row 1 , see dont have jan 2024 , then it will print out the planeID 
#! but the planeID might have jan 2024 in another row 
# print ("testing ")

# planeIDs_without_jan2024123 = df[~df['DATE'].str.contains("Jan 2024", case=False, na=False)]['planeID'].unique()
# print (planeIDs_without_jan2024123) 
# print (len(planeIDs_without_jan2024123))

# RescrapeAirline("singapore-airlines_sq-sia") 

def checkDFsforonerecord():
    df = pd.read_csv("data/air-japan_nq-ajx.csv") 
    # find if there is any planeID with 1 record only 
    planeID_with_one_record = df['planeID'].value_counts() 
    planeID_with_one_record = planeID_with_one_record[planeID_with_one_record == 1] 
    print (planeID_with_one_record) 

checkDFsforonerecord()