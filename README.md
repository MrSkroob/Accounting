# Setup
Either: import CSV files (see below) or create an empty database and add things manually.

# If you want to add things manually:
1. Ensure that any "PE.db" does not exist.
2. Run "init_database.py" once. (located under "Utils")

# If you want to convert a CSV file to a .db file:

1. Create a ConvertedCSVs folder and ImportedCSVs folder (if they don't exist!) and parent them under the Utils folder. 
2. Place the CSV you want to convert under "ImportedCSVs".
3. Replace `csv_path` with "ImportedCSVs/" + the CSV file name
4. Replace `db_type` with either "Periods" (if it is a Period database) or "Payments" (if it is a Payment database). NOTE: IMPORT BOTH PERIOD AND PAYMENTS AT THE SAME TIME, SO THEY'RE IN THE SAME DATABASE.
5. Run the code.
6. Under "ConvertedCSVs" there should be a database called "PE.db"
