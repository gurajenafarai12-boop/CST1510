import pandas as pd
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Inserting a new cyber incident into the database.
    
    """
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    
    incident_id = cursor.lastrowid
    cursor.close()
    
    return incident_id

def get_all_incidents(conn):
    """
    Retrieving all incidents from the database.
"""
    # Reading all incidents into a DataFrame
    
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY timestamp DESC", conn)
    #Returning as dataframe
    
    return df   

def update_incident_status(conn, incident_id, new_status):
    """
    Updating the status of an incident.
    
    """
    
    # Updating sql and parameters
    update_sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    # Executing and committing
    cursor = conn.cursor()
    cursor.execute(update_sql, (new_status, incident_id))
    conn.commit()
    # Returning rowcount
    rows_updated=cursor.rowcount
    conn.close()
    return rows_updated
    pass

def delete_incident(conn, incident_id):
    """
    Deleting an incident from the database.
    """
    
    # Delete an incident where id matches
    delete_sql = "DELETE FROM cyber_incidents WHERE id = ?"
    # Executing and committing
    cursor=conn.cursor()
    cursor.execute(delete_sql,(incident_id,))
    conn.commit()
    # Returning rowcount
    rows_deleted= cursor.rowcount
    
    return rows_deleted

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

if __name__ == "__main__":
    conn = connect_database()
    

    print("\n Incidents by Type:")
    df_by_type = get_incidents_by_type_count(conn)
    print(df_by_type)

    print("\n High Severity Incidents by Status:")
    df_high_severity = get_high_severity_by_status(conn)
    print(df_high_severity)

    print("\n Incident Types with Many Cases (>5):")
    df_many_cases = get_incident_types_with_many_cases(conn, min_count=5)
    print(df_many_cases)

    conn.close()


