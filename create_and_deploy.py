#!/usr/bin/env python3
"""
Complete database setup: Create database if not exists, then deploy schema and data.

This script:
1. Connects to master database
2. Creates PineappleBytes database if it doesn't exist
3. Deploys schema and sample data directly

Supports both direct RDS connection and SSH tunnel connection.
"""

import os
import sys
import pyodbc
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Import schema from deploy_database (avoiding exec)
SCHEMA_SQL = """
-- ============================================================================
-- PineappleBites Database Schema
-- ============================================================================
-- This script creates all tables for the PineappleBites database.
-- Foreign key relationships are defined to ensure data integrity.
-- ============================================================================

-- Drop existing tables in reverse dependency order (if they exist)
IF OBJECT_ID('ticket_note', 'U') IS NOT NULL DROP TABLE ticket_note;
IF OBJECT_ID('ticket', 'U') IS NOT NULL DROP TABLE ticket;
IF OBJECT_ID('agreement', 'U') IS NOT NULL DROP TABLE agreement;
IF OBJECT_ID('configuration', 'U') IS NOT NULL DROP TABLE configuration;
IF OBJECT_ID('contact', 'U') IS NOT NULL DROP TABLE contact;
IF OBJECT_ID('resource', 'U') IS NOT NULL DROP TABLE resource;
IF OBJECT_ID('team', 'U') IS NOT NULL DROP TABLE team;
IF OBJECT_ID('company', 'U') IS NOT NULL DROP TABLE company;

-- ============================================================================
-- Table: company
-- ============================================================================
CREATE TABLE company (
    company_id INT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    location VARCHAR(500),
    department VARCHAR(100)
);

CREATE INDEX idx_company_department ON company(department);
CREATE INDEX idx_company_name ON company(company_name);

-- ============================================================================
-- Table: team
-- ============================================================================
CREATE TABLE team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(500) NOT NULL
);

CREATE INDEX idx_team_name ON team(team_name);

-- ============================================================================
-- Table: resource
-- ============================================================================
CREATE TABLE resource (
    resource_id INT PRIMARY KEY,
    resource_name VARCHAR(255) NOT NULL
);

CREATE INDEX idx_resource_name ON resource(resource_name);

-- ============================================================================
-- Table: contact
-- ============================================================================
CREATE TABLE contact (
    contact_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(50),
    extension VARCHAR(20),
    title VARCHAR(100),
    relationship VARCHAR(50),
    contact_type VARCHAR(50),
    email VARCHAR(255)
);

CREATE INDEX idx_contact_name ON contact(last_name, first_name);
CREATE INDEX idx_contact_email ON contact(email);
CREATE INDEX idx_contact_type ON contact(contact_type);

-- ============================================================================
-- Table: configuration
-- ============================================================================
CREATE TABLE configuration (
    configuration_id INT PRIMARY KEY,
    config_name VARCHAR(500) NOT NULL,
    config_type VARCHAR(100),
    status VARCHAR(50),
    serial_number VARCHAR(100),
    tag_number VARCHAR(50),
    model_number VARCHAR(50),
    purchased_date DATE
);

CREATE INDEX idx_config_type ON configuration(config_type);
CREATE INDEX idx_config_status ON configuration(status);
CREATE INDEX idx_config_tag ON configuration(tag_number);

-- ============================================================================
-- Table: agreement
-- ============================================================================
CREATE TABLE agreement (
    agreement_id INT PRIMARY KEY,
    agreement_type VARCHAR(50) NOT NULL,
    agreement_name VARCHAR(500) NOT NULL,
    amount DECIMAL(10,2),
    billing_cycle INT,
    date_start DATE,
    date_end DATE,
    status VARCHAR(50)
);

CREATE INDEX idx_agreement_type ON agreement(agreement_type);
CREATE INDEX idx_agreement_status ON agreement(status);
CREATE INDEX idx_agreement_dates ON agreement(date_start, date_end);

-- ============================================================================
-- Table: ticket
-- ============================================================================
CREATE TABLE ticket (
    ticket_id INT PRIMARY KEY,
    total_hours DECIMAL(5,2),
    age DECIMAL(5,1),
    status VARCHAR(50),
    schedule_flag VARCHAR(20),
    summary_description TEXT,
    priority VARCHAR(20),
    budget DECIMAL(10,2),
    ticket_type VARCHAR(50),
    subtype VARCHAR(50),
    item VARCHAR(50),
    date_entered DATE,
    team_name VARCHAR(200)
);

CREATE INDEX idx_ticket_status ON ticket(status);
CREATE INDEX idx_ticket_priority ON ticket(priority);
CREATE INDEX idx_ticket_type ON ticket(ticket_type);
CREATE INDEX idx_ticket_team ON ticket(team_name);
CREATE INDEX idx_ticket_date ON ticket(date_entered);

-- ============================================================================
-- Table: ticket_note
-- ============================================================================
CREATE TABLE ticket_note (
    note_id INT PRIMARY KEY,
    ticket_id INT,
    note_text TEXT,
    created_date DATETIME,
    author VARCHAR(100),
    FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_ticket_note_ticket_id ON ticket_note(ticket_id);
CREATE INDEX idx_ticket_note_created_date ON ticket_note(created_date);
"""

# Try to load sample data
SAMPLE_DATA_SQL = ""
data_file = 'sample_data.sql'
if os.path.exists(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        SAMPLE_DATA_SQL = f.read()
else:
    logger.warning(f"Sample data file '{data_file}' not found. Will create schema only.")


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


def build_connection_string(master: bool = False):
    """
    Build ODBC connection string from environment variables.
    
    Supports two configurations:
    1. SSH Tunnel (local port forwarding):
       - DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
       - Connects to localhost via tunnel
    2. Direct connection:
       - DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD
       - Connects directly to RDS
    
    Args:
        master: If True, connect to master database (for CREATE DATABASE)
        
    Returns:
        ODBC connection string for SQL Server
    """
    # Check for SSH tunnel configuration first (preferred if both exist)
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    
    if db_host and db_port and db_user and db_pass and db_name:
        # Using SSH tunnel - connect to localhost via forwarded port
        logger.info(f"Using SSH tunnel configuration: {db_host}:{db_port}")
        database = 'master' if master else db_name
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={db_host},{db_port};"
            f"DATABASE={database};"
            f"UID={db_user};"
            f"PWD={db_pass};"
            f"TrustServerCertificate=yes;"
            f"Connection Timeout=30;"
        )
        return conn_str
    
    # Fall back to direct RDS connection
    server = os.getenv('DB_SERVER')
    database = 'master' if master else os.getenv('DB_DATABASE', 'PineappleBytes')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    if not server:
        raise ValueError(
            "DB_SERVER environment variable not set. "
            "Please configure your .env file with the RDS endpoint "
            "or use SSH tunnel variables (DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)."
        )
    
    if not username or not password:
        raise ValueError(
            "DB_USERNAME and DB_PASSWORD must be set in .env file. "
            "SQL Server authentication is required for RDS."
        )
    
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
    )
    
    logger.info(f"Built direct connection string for server: {server}, database: {database}")
    return conn_str


def database_exists(cursor, db_name):
    """Check if database exists"""
    cursor.execute(
        "SELECT name FROM sys.databases WHERE name = ?",
        db_name
    )
    return cursor.fetchone() is not None


def create_database():
    """Create PineappleBytes database if it doesn't exist"""
    db_name = os.getenv('DB_DATABASE', 'PineappleBytes')
    
    # If using SSH tunnel, prefer DB_NAME
    db_name_ssh = os.getenv('DB_NAME')
    if db_name_ssh:
        db_name = db_name_ssh
    
    print(f"Connecting to master database on server: {os.getenv('DB_SERVER', 'via tunnel')}")
    
    try:
        # Sanitize database name
        db_name = sanitize_db_name(db_name)
        
        # Connect to master with autocommit for CREATE DATABASE
        conn = pyodbc.connect(build_connection_string(master=True), autocommit=True)
        cursor = conn.cursor()
        
        print("Connection to master established.")
        
        # Check if database already exists
        if database_exists(cursor, db_name):
            print(f"✅ Database '{db_name}' already exists. Skipping creation.")
        else:
            print(f"Creating database '{db_name}'...")
            # Use parameterized query not possible for DDL, so sanitize and bracket
            safe_name = db_name.replace(']', ']]')
            cursor.execute(f"CREATE DATABASE [{safe_name}]")
            print(f"✅ Database '{db_name}' created successfully.")
        
        conn.close()
        print("Connection to master closed.\n")
        
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    except ValueError as e:
        print(f"❌ Invalid database name: {e}")
        return False


def execute_schema(connection):
    """Execute schema creation"""
    logger.info("Executing schema deployment...")
    
    cursor = connection.cursor()
    
    # Split on GO statements
    commands = []
    current = []
    for line in SCHEMA_SQL.splitlines():
        if line.strip().upper() == 'GO':
            if current:
                commands.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        commands.append('\n'.join(current))
    
    # Execute each command
    success_count = 0
    errors = []
    
    for i, command in enumerate(commands, 1):
        try:
            cursor.execute(command)
            cursor.commit()
            success_count += 1
            logger.debug(f"Schema command {i} executed successfully")
        except pyodbc.Error as e:
            # Check if it's a "already exists" error, which is okay
            if "already exists" in str(e).lower():
                logger.warning(f"Object already exists (command {i}): {str(e)[:100]}")
                success_count += 1
            else:
                error_msg = f"Schema command {i} failed: {str(e)[:200]}"
                logger.error(error_msg)
                errors.append(error_msg)
    
    cursor.close()
    
    logger.info(f"Schema deployment complete: {success_count} commands executed, {len(errors)} errors")
    return len(errors) == 0, errors


def execute_data(connection):
    """Execute data inserts"""
    if not SAMPLE_DATA_SQL:
        logger.warning("No sample data to insert. Skipping.")
        return True, []
    
    logger.info("Executing data deployment...")
    
    cursor = connection.cursor()
    
    # Split on GO statements
    commands = []
    current = []
    for line in SAMPLE_DATA_SQL.splitlines():
        if line.strip().upper() == 'GO':
            if current:
                commands.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    if current:
        commands.append('\n'.join(current))
    
    # Execute INSERT commands
    success_count = 0
    total_rows = 0
    errors = []
    
    for i, command in enumerate(commands, 1):
        try:
            cursor.execute(command)
            total_rows += cursor.rowcount
            success_count += 1
            if i % 50 == 0:
                logger.info(f"Processed {i}/{len(commands)} insert commands...")
        except pyodbc.Error as e:
            error_msg = f"Data insert {i} failed: {str(e)[:200]}"
            logger.error(error_msg)
            errors.append(error_msg)
            continue
    
    cursor.commit()
    cursor.close()
    
    logger.info(f"Data deployment complete: {total_rows} rows inserted, {len(errors)} errors")
    return len(errors) == 0, errors


def deploy_schema_and_data():
    """Deploy schema and sample data"""
    logger.info("="*60)
    logger.info("DEPLOYING SCHEMA AND SAMPLE DATA")
    logger.info("="*60)
    
    try:
        # Get database name for connection
        db_name = os.getenv('DB_DATABASE', 'PineappleBytes')
        db_name_ssh = os.getenv('DB_NAME')
        if db_name_ssh:
            db_name = db_name_ssh
        
        # Connect to PineappleBytes database
        conn_str = build_connection_string(master=False)
        logger.info(f"Connecting to database: {db_name}")
        conn = pyodbc.connect(conn_str)
        logger.info("Connected successfully.")
        
        # Deploy schema
        schema_success, schema_errors = execute_schema(conn)
        
        # Deploy data
        data_success, data_errors = execute_data(conn)
        
        conn.close()
        logger.info("Database connection closed.")
        
        all_errors = schema_errors + data_errors
        
        if all_errors:
            logger.warning(f"Deployment completed with {len(all_errors)} errors")
            return False
        else:
            logger.info("✅ Deployment completed successfully!")
            return True
            
    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*60)
    print("PineappleBytes Database Setup")
    print("="*60)
    print()
    
    # Step 1: Create database if needed
    print("STEP 1: Database Creation")
    print("-"*60)
    if not create_database():
        print("\n❌ Database creation failed. Exiting.")
        sys.exit(1)
    
    print()
    
    # Step 2: Deploy schema and data
    print("STEP 2: Schema and Data Deployment")
    print("-"*60)
    if not deploy_schema_and_data():
        print("\n❌ Schema/data deployment failed. Exiting.")
        sys.exit(1)
    
    print()
    print("="*60)
    print("✅ ALL SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nYou can now run: python middleware_engine.py --company-id 26")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())