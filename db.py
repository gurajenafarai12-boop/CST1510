import sqlite3
from pathlib import Path
import pandas as pd    

#Path definition
DATA_DIR   = Path("DATA")
DB_PATH    = DATA_DIR / "intelligence_platforms.db"
#Creating directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
print(" Imports successful.")
print(f"Data folder: {DATA_DIR.resolve()}")
print(f"Database will be created at:{DB_PATH.resolve()}")

#Connecting to the database
def connect_database(db_path=DB_PATH):
    """Connect to the SQLite database."""
    return sqlite3.connect(db_path)


#Loading CSV to table function
def load_csv_to_table(conn,csv_path,table_name):
    '''Loading a CSV file into a table using pandas'''
    #Checking if csv file exists
    file_path=Path(csv_path)
    if not file_path.exists():
        print(f"File {csv_path} does not exist")
        return -1
    #Reading CSV Using pandas
    try: 
        df=pd.read_csv(csv_path)
        print(f"Loaded CSV: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        print(f"Error reading CSV:{e}")
        return -1

    #Inserting data with df.to_sql
    try:
        rows_loaded=df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
    #Display message
        print(f"Sucess! Loaded {rows_loaded} rows into {table_name}")
        return rows_loaded
    except Exception as e:
        print(f"Error loading data into : {e}")
        return -1

    pass 
              
def load_all_csv_data(conn):
    """Load all CSV data into the database """
    csv_mappings = [
        ("DATA/cyber_incidents.csv", "cyber_incidents"),
        ("DATA/it_tickets.csv", "it_tickets"),
        ("DATA/datasets_metadata.csv", "datasets_metadata"),
    ]

    total_rows = 0
    for csv_path, table_name in csv_mappings:
        rows = load_csv_to_table(conn, csv_path, table_name)
        if rows > 0:
            total_rows += rows
        else:
            print(f"Failed to load data from {csv_path}")
        
    print(f" Total rows loaded from all CSVs: {total_rows}")
    return total_rows

if __name__ == "__main__":
    print("Import successful.")
    print(f"Data folder: {DATA_DIR.resolve()}")
    print(f"Database will be created at: {DB_PATH.resolve()}")