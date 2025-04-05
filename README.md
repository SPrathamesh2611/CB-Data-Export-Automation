CB Data Export Automation
This Python script automates the extraction, transformation, and export of CB (Credit Bureau) data from a SQL Server database, generates specific output files with formatted headers/footers, and renames the final outputs with a .cdf extension. It supports multiple credit bureau formats such as Highmark, CIBIL, and Equifax.

📁 Project Structure
arduino
CB-Data-Export-Automation/
    original_file/
        CB_original_{end_date}.csv
    Highmark_Files/
        Highmark_{end_date}.cdf
    Cibil_Files/
        Cibil_{end_date}.cdf
    Equifax_Files/
        Equifax_{end_date}.cdf
    date_config.txt       # Contains:startdate=01-Jan-25 & enddate=31-Jan-25
    cb_data_export.py     # Main script



⚙️ Features
Connects to a SQL Server using pyodbc.

Executes a stored procedure udp_CBDataSubmissionAll with start_date and end_date.

Exports data to CSV with pipe-delimiter |.

Adds custom headers and footers based on the credit bureau format.

Renames .csv files to .cdf.

Automatically reads dates from an external config file.


🧰 Requirements
Python 3.x

Modules: 
  pandas
  pyodbc

Install dependencies:
  pip install pandas pyodbc

🛠️ Usage
Update date_config.txt


startdate=01-Jan-25
enddate=31-Jan-25
Run the Script


python cb_data_export.py
Output

Original data saved in: original_file/CB_original_{end_date}.csv

Final output files (Highmark, Cibil, Equifax) are saved with .cdf extensions in their respective folders.

📌 Notes
Make sure the folder structure exists (original_file, Highmark_Files, etc.)

Edit SQL credentials before deployment (never commit sensitive info to public repositories).

Header/footer strings are hardcoded for specific bureau formats and should be updated if the format changes.

🧑‍💻 Author
Developed by PRATHAMESH SURVE.
