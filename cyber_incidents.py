import sqlite3
from app.data.db import connect database
import pandas as pd



def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database
    """
 #Connection to the database   
    conn=connect_database()
    cursor=conn.cursor()

    insert_sql="""
    INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
 #Executing and committing with cursor   
    cursor.execute(insert_sql,(date,incident_type,severity,status,description,reported_by))
    cursor.connection.commit()
#Returning cursor.lastrowid
    return cursor.lastrowid
    pass

def get_all_incidents(conn):
    """
    Retrieving all incidents from the database.
    """
    #Using pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    df=pd.read_sql_query("SELECT * FROM cyber_incidents",conn)
    #Returning as dataframe
    return df
    pass

def update_incident_status(conn, incident_id, new_status):
    """
    Updating the status of an incident.
    """
    # Writing UPDATE SQL to update cyber incidents
    cursor=conn.cursor

    update_sql="""
    UPDATE cyber_incidents 
    SET status=?
    WHERE id=?"""
    # Executing and committing
    cursor.execute(update_sql,(new_status,incident_id))
    conn.commit()
    # Returning cursor.rowcount
    return cursor.rowcount
    pass


def delete_incident(conn, incident_id):
    """  
    Deleting an incident from the database.  
    
    """  
    # DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    sql = "DELETE FROM cyber_incidents WHERE id = ?"
    #Execting and commiting
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (incident_id,))
        conn.commit()
        
        # Returning the number of rows deleted
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e


