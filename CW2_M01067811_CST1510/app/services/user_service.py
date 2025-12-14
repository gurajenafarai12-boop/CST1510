import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username,insert_user
from app.data.schema import create_users_table
import sqlite3
import pandas as pd


#Register user function
def register_user(username, password, role='user'):
    """Register a new user with hashed password and role."""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    """Register new user with password hashing."""
    # Hashing password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Inserting into database
    if insert_user(username, password_hash, role):
        return True, f"User '{username}' registered successfully."
    else:
        return False, "Failed to register user."

#Login user function
def login_user(username, password):
    """Login user by verifying username and password."""
    conn = connect_database()
    cursor = conn.cursor()
    
    # Finding user
    user = get_user_by_username(conn, username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    try:
        stored_hash = stored_hash.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
         return True, f"Login successful! Welcome {username}."
        else:
         return False, "Incorrect password."
    except Exception as e:
        return False, f"Error verifying password: {e}"


DATA_DIR = Path(__file__).parent / "data"

#Migrating users from text file to database
def migrate_users_from_file(conn, filepath='DATA/users.txt'):
    """Migrate users from a text file into the users table."""
    filepath = Path(filepath)
#Checking if file exists
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return 0
    
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        lines=f.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('username'):
                continue
            
            # Parse line: username,password_hash
            parts = line.split(', ')
            if len(parts) >= 2:
                username = parts[0].strip()
                password_hash = parts[1].strip()
                role='user'  # Default role

                print(f"Processing user: {username}, role: {role}")
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")


#Veryfying that users were migrated successfully
def fetch_all_users(conn):
    """Return all users as a list of tuples (id, username, role)."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    return cursor.fetchall()


    



