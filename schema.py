import pandas as pd
import sqlite3
from pathlib import Path


#Creating user table
def create_users_table(conn):
    """Create users table."""
    # Getting a cursor from the connection
    cursor = conn.cursor()
    # Writing CREATE TABLE IF NOT EXISTS SQL statement
    create_users_table="""
       CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                   role TEXT DEFAULT 'user',
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )"""
    # Executing the SQL statement
    cursor.execute(create_users_table)
    # Commiting the changes
    conn.commit()
    # Display for success message
    print("✅ Users table created successfully!")

#Creating cyber incidents table
def create_cyber_incidents_table(conn):
# Getting a cursor from the connection
    cursor=conn.cursor()
# Writing CREATE TABLE IF NOT EXISTS SQL statement
    create_table_sql="""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       incident_id TEXT UNIQUE NOT NULL,
       timestamp CURRENT_TIMESTAMP,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        category TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
#Executing the SQL statement
    cursor.execute(create_table_sql)
#Commiting the changes
    conn.commit()
#Dsiplay for success message  
    print("✅ Cyber Incidents table created successfully!")
    pass


def create_datasets_metadata_table(conn):
    #Getting a cursor from the connection
    cursor=conn.cursor()
    #Writing CREATE TABLE IF NOT EXISTS SQL statement
    create_table_sql="""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id INTEGER,
        dataset_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        rows TEXT,
        columns TEXT,
        uploaded_by TEXT,
        upload_date TEXT,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    #Executing the SQL statement
    cursor.execute(create_table_sql)
    #Commiting the changes
    conn.commit()
    print("✅ Datasets Metadata table created successfully!")
    pass


def create_it_tickets_table(conn):
    #Implement following the users table pattern
    cursor=conn.cursor()
    create_table_sql="""
     CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        description TEXT,
        status TEXT,
        assigned_to TEXT,
        created_at TEXT,
        resolution_time_hours INTEGER,
        created_at_db TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    #Executing the SQL statement
    cursor.execute(create_table_sql)
    #Commiting the changes
    conn.commit()
    print("✅ IT Tickets table created successfully!")
    pass

              
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)

    print("✅ All tables created successfully!")

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas
    """
    # Check if CSV file exists
    import os
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return 0
    
    try:
        # Read CSV using pandas
        df = pd.read_csv(csv_path)
        
        # Insert data into database
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"✅ Loaded {len(df)} rows from {csv_path} to {table_name} table")
        return len(df)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return 0

def load_all_csv_data(conn):
    """
    Load all CSV data into respective tables.
    Returns the total number of rows loaded.
    """
    csv_files = {
        "DATA/cyber_incidents.csv": "cyber_incidents",
        "DATA/datasets_metadata.csv": "datasets_metadata", 
        "DATA/it_tickets.csv": "it_tickets"
    }
    
    total_rows = 0
    for csv_file, table_name in csv_files.items():
        rows = load_csv_to_table(conn, csv_file, table_name)
        total_rows += rows
    
    return total_rows
