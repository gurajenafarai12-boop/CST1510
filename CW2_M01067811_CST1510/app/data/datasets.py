import sqlite3
from app.data.db import connect_database
import pandas as pd



def insert_dataset(conn, dataset_name, category, source, last_updated, records_count,file_size_mb):
    """
    Inserting metadata into the database
    """
 #Connection to the database   
    conn=connect_database()
    cursor=conn.cursor()

    insert_sql="""
    INSERT INTO datasets_metadata (dataset_name, category, source, last_updated, records_count, file_size_mb)
    VALUES (?, ?, ?, ?, ?, ?)
    """
 #Executing and committing with cursor   
    cursor.execute(insert_sql,(dataset_name, category, source, last_updated, records_count, file_size_mb))
    conn.commit()
#Returning cursor.lastrowid
    return cursor.lastrowid
    pass

def get_all_datasets(conn):
    """
    Retrieving all datasets from the database.
    """
    #Using pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    df=pd.read_sql_query("SELECT * FROM datasets_metadata",conn)
    #Returning as dataframe
    return df
    pass

def update_dataset(conn, dataset_id, new_category, new_source):
    """
    Updating the status of an dataset.
    """
    # Writing UPDATE SQL to update dataset category and source
    cursor=conn.cursor

    update_sql="""
    UPDATE datasets_metadata 
    SET category=?, source=?
    WHERE id=?"""
    # Executing and committing
    cursor.execute(update_sql,(new_category,new_source,dataset_id))
    conn.commit()
    # Returning cursor.rowcount
    return cursor.rowcount
    pass


def delete_dataset(conn, dataset_id):
    """  
    Deleting an dataset from the database.  
    
    """  
    # DELETE SQL: DELETE a dataset WHERE id = ?
    sql = "DELETE FROM datasets_metadata WHERE id = ?"
    #Execting and commiting
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (dataset_id,))
        conn.commit()
        
        # Returning the number of rows deleted
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    
def get_datasets_by_category_count(conn):
    """
    Count datasets by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM datasets_metadata
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_large_datasets(conn, min_size_mb=100):
    """
    Conuting datasets larger than min_size_mb.
    """
    query = """
    SELECT dataset_name, file_size_mb,category
    FROM datasets_metadata
    WHERE file_size_mb > ?
    ORDER BY file_size_mb DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_size_mb,))
    return df



