import sqlite3
from app.data.db import connect_database
import pandas as pd



def insert_ticket(conn, ticket_id, priority, status, category, subject, description, 
                  created_date, resolved_date=None, assigned_to=None):
    """
    Insert a new ticket into the database
    """
 #Connection to the database   
    conn=connect_database()
    cursor=conn.cursor()

    insert_sql="""
    INSERT INTO it_tickets (ticket_id, priority, status, category, subject, description, 
     created_date, resolved_date, assigned_to)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
 #Executing and committing with cursor   
    cursor.execute(insert_sql,(ticket_id, priority, status, category, subject, description, 
     created_date, resolved_date, assigned_to))
    conn.commit()
#Returning cursor.lastrowid
    return cursor.lastrowid
    pass

def get_all_tickets(conn):
    """
    Retrieving all tickets from the database.
    """
    #Using pd.read_sql_query("SELECT * FROM it_tickets", conn)
    df=pd.read_sql_query("SELECT * FROM it_tickets",conn)
    #Returning as dataframe
    return df
    pass

def update_ticket_status(conn, ticket_id, new_status,resolved_date=None):
    """
    Updating the status of an ticket.
    """
    # Writing UPDATE SQL to update cyber incidents
    cursor=conn.cursor
    if resolved_date :
    
     update_sql="""
     UPDATE it_tickets
     SET status=?, resolved_date=?
     WHERE ticket_id=?"""
     # Executing and committing
     cursor.execute(update_sql,(new_status,resolved_date,ticket_id))
    else:
        update_sql="""
        UPDATE it_tickets
        SET status=?
        WHERE ticket_id=?"""
        # Executing and committing
        cursor.execute(update_sql,(new_status,ticket_id))
    
    
    conn.commit()
    # Returning cursor.rowcount
    return cursor.rowcount
    pass


def delete_ticket(conn, ticket_id):
    """  
    Deleting an incident from the database.  
    
    """  
    # DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    sql = "DELETE FROM it_tickets WHERE ticket_id = ?"
    #Execting and commiting
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (ticket_id,))
        conn.commit()
        
        # Returning the number of rows deleted
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    
def get_ticket_by_priority(conn):
    """
    Count tickets by priority.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT priority, COUNT(*) as count
    FROM it_tickets
    GROUP BY priority
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_open_tickets(conn):
    """
    Get all open tickets
    """
    query = """
    SELECT ticket_id,priority,category,subject,created_date
    FROM it_tickets
    WHERE status != 'Resolved' and status != 'Closed'
    ORDER BY created_date DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_tickets_assigned_to(conn, assigned_to):
    """
    Get all tickets assigned to a specific person
    """
    query = """
    SELECT ticket_id,priority,category,subject,status,created_date,resolved_date
    FROM it_tickets
    WHERE assigned_to = ?
    ORDER BY created_date DESC
    """
    df = pd.read_sql_query(query, conn, params=(assigned_to,))
    return df




