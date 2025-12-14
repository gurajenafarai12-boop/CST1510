"""
Database Manager service for SQLite operations
"""
import sqlite3
import pandas as pd
from typing import List, Tuple, Optional

class DatabaseManager:
    """Handles all database operations using OOP"""
    
    def __init__(self, db_path: str = "DATA/intelligence_platforms.db"):
        self.db_path = db_path
    
    def connect(self) -> sqlite3.Connection:
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: Tuple = ()) :
        """Execute INSERT, UPDATE, DELETE queries"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor
    #Fetchiung all rows from query
    def fetch_all(self, query: str, params: Tuple = ()) :
        """Fetch all rows from query"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    #Fetching a single row from query
    def fetch_one(self, query: str, params: Tuple = ()) :
        """Fetch single row from query"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result
    #Fetching results as pandas dataframe
    def fetch_dataframe(self, query: str, params: Tuple = ()) :
        """Fetch results as pandas DataFrame"""
        conn = self.connect()
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    #Getting row count for any table
    def get_table_count(self, table_name: str) -> int:
        """Get row count for any table"""
        result = self.fetch_one(f"SELECT COUNT(*) FROM {table_name}")
        return result[0] if result else 0
    
    def __str__(self) -> str:
        """String representation"""
        return f"DatabaseManager(db_path='{self.db_path}')"