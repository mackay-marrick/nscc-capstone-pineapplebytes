#!/usr/bin/env python3
"""
Script to rename SQL Server database from PineappleBites to PineappleBytes.

This script connects to the master database and:
1. Checks which database name currently exists
2. Renames PineappleBites -> PineappleBytes only if needed
3. Ensures .env file is set to DB_DATABASE=PineappleBytes

Requires:
- Autocommit mode (SQL Server doesn't allow ALTER DATABASE in transactions)
- Connection to master database, not the target database
"""

import os
import pyodbc
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()


def sanitize_db_name(db_name: str) -> str:
    """
    Sanitize database name for use in DDL statements.
    
    Removes potentially dangerous characters and validates the name
    follows SQL Server identifier naming rules. This prevents SQL
    injection when database names must be interpolated into DDL.
    
    Args:
        db_name: Raw database name string
        
    Returns:
        Sanitized database name safe for DDL execution
        
    Raises:
        ValueError: If database name contains invalid characters
    """
    if not db_name:
        raise ValueError("Database name cannot be empty")
    
    # Strip whitespace
    db_name = db_name.strip()
    
    # Enforce length limits (1-128 characters for SQL Server)
    if len(db_name) > 128:
        raise ValueError(f"Database name too long: {len(db_name)} chars (max 128)")
    
    if len(db_name) < 1:
        raise ValueError("Database name cannot be empty")
    
    # Check for allowed characters only (alphanumeric, underscore)
    # This is a strict whitelist to prevent injection
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    for char in db_name:
        if char not in allowed_chars:
            raise ValueError(
                f"Database name contains invalid character: '{char}'. "
                f"Only alphanumeric and underscore allowed."
            )
    
    return db_name


def build_connection_string_master():
    """
    Build ODBC connection string to connect to master database.
    
    Uses environment variables:
    - DB_SERVER
    - DB_USERNAME (if empty, uses Windows Authentication)
    - DB_PASSWORD (if using SQL auth)
    
    Returns:
        ODBC connection string pointing to master database
    """
    server = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
    username = os.getenv('DB_USERNAME', '')
    password = os.getenv('DB_PASSWORD', '')
    
    if username and password:
        # SQL Server Authentication
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE=master;"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
    else:
        # Windows Authentication
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE=master;"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
    
    return conn_str

def database_exists(cursor, db_name):
    """Check if a database with the given name exists."""
    cursor.execute(
        "SELECT name FROM sys.databases WHERE name = ?",
        db_name
    )
    return cursor.fetchone() is not None

def rename_database():
    """
    Check current database name and rename if necessary.
    """
    connection_string = build_connection_string_master()
    
    print(f"Connecting to master database on server: {os.getenv('DB_SERVER')}")
    
    try:
        # Connect with autocommit=True (required for ALTER DATABASE)
        conn = pyodbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        
        print("Connection established. Checking database names...")
        
        # Check which databases exist (using sanitized hardcoded names)
        has_bites = database_exists(cursor, 'PineappleBites')
        has_bytes = database_exists(cursor, 'PineappleBytes')
        
        print(f"  PineappleBites exists: {has_bites}")
        print(f"  PineappleBytes exists: {has_bytes}")
        
        if has_bytes and not has_bites:
            print("\n✅ Database is already correctly named 'PineappleBytes'.")
            print("   No rename needed.")
        elif has_bites and not has_bytes:
            print("\nRenaming 'PineappleBites' to 'PineappleBytes'...")
            
            # Sanitize names (though they are hardcoded, validate for safety)
            old_name = sanitize_db_name('PineappleBites')
            new_name = sanitize_db_name('PineappleBytes')
            
            # Step 1: Force single user mode, rolling back any uncommitted transactions
            print("  Step 1: Setting PineappleBites to SINGLE_USER mode...")
            cursor.execute(f"ALTER DATABASE [{old_name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;")
            print("    ✓ Single user mode set")
            
            # Step 2: Rename the database
            print("  Step 2: Renaming database...")
            # Escape brackets in name (unlikely but safe)
            safe_old = old_name.replace(']', ']]')
            safe_new = new_name.replace(']', ']]')
            cursor.execute(f"ALTER DATABASE [{safe_old}] MODIFY NAME = [{safe_new}];")
            print("    ✓ Database renamed successfully")
            
            # Step 3: Set back to multi-user mode
            print("  Step 3: Setting PineappleBytes to MULTI_USER mode...")
            cursor.execute(f"ALTER DATABASE [{safe_new}] SET MULTI_USER;")
            print("    ✓ Multi-user mode restored")
            
            print("\n✅ Database rename completed successfully!")
        else:
            # Both exist or neither exists - ambiguous state
            if has_bites and has_bytes:
                print("\n⚠️  Both 'PineappleBites' and 'PineappleBytes' exist!")
                print("   Please resolve manually - cannot rename.")
            else:
                print("\n❌ Neither 'PineappleBites' nor 'PineappleBytes' exists on this server.")
                print("   Check database name or server connection.")
                raise RuntimeError("Target database not found")
        
    except pyodbc.Error as e:
        print(f"\n❌ Error during database operations: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connection closed.")

def update_env_file():
    """
    Ensure .env file contains DB_DATABASE=PineappleBytes.
    """
    env_path = '.env'
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Check if already set correctly
        if re.search(r'^\s*DB_DATABASE\s*=\s*PineappleBytes\s*$', content, re.MULTILINE):
            print(".env already contains DB_DATABASE=PineappleBytes")
            return
        
        # Replace any DB_DATABASE line
        new_content = re.sub(
            r'^\s*DB_DATABASE\s*=\s*.*$',
            'DB_DATABASE=PineappleBytes',
            content,
            flags=re.MULTILINE
        )
        
        with open(env_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Updated .env file: DB_DATABASE=PineappleBytes")
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        raise

if __name__ == "__main__":
    print("="*60)
    print("Database Rename Utility")
    print("="*60)
    
    # Step 1: Check and rename if needed
    rename_database()
    
    # Step 2: Update .env to ensure correct setting
    print("\nUpdating environment configuration...")
    update_env_file()
    
    print("\n" + "="*60)
    print("All done. Ready to run middleware_engine.py")
    print("="*60)