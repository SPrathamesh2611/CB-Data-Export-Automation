import os
import pyodbc
import pandas as pd
from datetime import datetime, timedelta

# Step 1: Establish SQL connection
def fetch_data_from_sql(start_date, end_date):
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER={Your server Name};"
        "DATABASE=smf;"
        "UID={Your username};"
        "PWD={Your Password}"
    )
    query = f"exec udp_CBDataSubmissionAll '{start_date}','{end_date}'"
    
    # Fetch the result into a pandas DataFrame
    df = pd.read_sql(query, conn)
    
    
    # Export the result to the original CSV file
    df.to_csv(r'D:\final cb project\original_file\CB_original_{end_date}.csv', sep='|', index=False, header=False)
    
    conn.close()

# Step 2: Calculate today's and yesterday's dates in DDMMYYYY format
def get_dates():
    today = datetime.now().strftime('%d%m%Y')
    yesterday = (datetime.now() - timedelta(1)).strftime('%d%m%Y')
    return today, yesterday

# Step 3: Read startdate and enddate from an external file
def read_query_dates(file_path='D:/final cb project/date_config.txt'):
    start_date = None
    end_date = None
    with open(file_path, 'r') as f:
        for line in f:
            if 'startdate' in line:
                start_date = line.split('=')[1].strip()  # Extract the start date
            elif 'enddate' in line:
                end_date = line.split('=')[1].strip()    # Extract the end date
    return start_date, end_date

# Step 4: Generate CSV files with dynamic headers and filenames
def create_csv_files(today, end_date,yesterday):
    headers = [
        f"HDRHMMFI1.9MFI0000079SVASTI                                  {end_date}{today}S01SVASTI123                     INHOUSE                       INHOUSE                       ",
        f"HDRHMMFI1.9MF8324    SVASTIMFPL                              {end_date}{yesterday}   Password1                                                                           FUTURE",
        f"HDRHMMFI1.9027FZ00106    SVASTIMFPL                              {end_date}{today}   Password1                                                                           FUTURE"
    ]
    
    # Read the original CSV content
    with open(r'D:\final cb project\original_file\CB_original_{end_date}.csv', 'r') as original_file:
        original_data = original_file.read()
    
    # Create three files with respective headers and append the original data
    file_info = [
        (rf'D:\final cb project\Highmark_Files\Highmark_{end_date}.csv', headers[0]),
        (rf'D:\final cb project\Cibil_Files\Cibil_{end_date}.csv', headers[1]),
        (rf'D:\final cb project\Equifax_Files\Equifax_{end_date}.csv', headers[2])
    ]
    
    for filename, header in file_info:
        with open(filename, 'w') as new_file:
            new_file.write(header + '\n')
            new_file.write(original_data)
        
        # If it's the second file, append an extra footer
        if 'Highmark' in filename:
            with open(filename, 'a') as new_file:
                new_file.write(f"TRLHMMFI1.9MFI0000079")
        
        # If it's the third file, append the footer as well
        if 'Cibil' in filename:
            with open(filename, 'a') as new_file:
                new_file.write(f"TRLHMMFI1.9MF8324                     END")
                
                
                

# Step 5: Function to rename file extensions
def rename_to_cdf(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Split the file path into name and extension
        base_name, ext = os.path.splitext(file_path)
        if ext.lower() == ".csv":
            # Form the new file name with .cdf extension
            new_file_path = f"{base_name}.cdf"
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"File renamed to: {new_file_path}")
            return new_file_path
        else:
            print(f"File extension is not '.csv'. Skipping renaming for: {file_path}")
    else:
        print(f"File does not exist: {file_path}")
    return None

# Step 6:Example usage
def rename_generated_files(end_date):
    files_to_rename = [
        rf'D:\final cb project\Highmark_Files\Highmark_{end_date}.csv',
        rf'D:\final cb project\Cibil_Files\Cibil_{end_date}.csv',
        rf'D:\final cb project\Equifax_Files\Equifax_{end_date}.csv'
    ]
    
    for file_path in files_to_rename:
        rename_to_cdf(file_path)


# Step 7: Main function to orchestrate the steps
def main():
    print("Starting SQL query execution...")
    
    # Read the query dates from the external file
    start_date, end_date = read_query_dates()
    if start_date and end_date:
        print(f"Query dates read: Start Date = {start_date}, End Date = {end_date}")
        fetch_data_from_sql(start_date, end_date)
        print("SQL query executed and data exported to CB_original.csv.")
    else:
        print("Error: Start date or end date not found in the config file.")
        return
    
    today, yesterday = get_dates()
    print(f"Dates calculated: Today = {today}, Yesterday = {yesterday}")
    
    end_date = datetime.strptime(end_date, '%d-%b-%y').strftime('%d%m%Y')	#convert into DDMMYYYY

    create_csv_files(today, end_date,yesterday)
    print("All files generated successfully!")
    
    #Rename the generated CSV files to .cdf
    rename_generated_files(end_date)
    print("All files renamed to .cdf successfully!")

if __name__ == '__main__':
    main()





