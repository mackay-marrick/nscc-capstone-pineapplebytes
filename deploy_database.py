#!/usr/bin/env python3
"""
Database Deployment Automation for AWS RDS SQL Server 2022

This script automates the deployment of the PineappleBites database schema and
sample data to an AWS RDS SQL Server instance.

Workflow:
1. Connect to the existing empty database using pyodbc
2. Execute schema.sql to create all table structures
3. Execute clean_data.sql to insert sample data
4. Verify deployment success

Prerequisites:
- Database 'PineappleBites' must already exist on the RDS instance
- Connection details configured in .env file:
  * DB_SERVER (RDS endpoint) OR DB_HOST/DB_PORT for SSH tunnel
  * DB_DATABASE (database name) OR DB_NAME for SSH tunnel
  * DB_USERNAME (username) OR DB_USER for SSH tunnel
  * DB_PASSWORD (password) OR DB_PASS for SSH tunnel
- Required packages: pyodbc, python-dotenv

Usage:
    python deploy_database.py
    python deploy_database.py --schema-only
    python deploy_database.py --data-only
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Tuple, List, Dict, Any

import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE SCHEMA DEFINITION
# ============================================================================

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


# ============================================================================
# DEPLOYMENT MANAGER
# ============================================================================

class DatabaseDeployer:
    """
    Handles database deployment operations to AWS RDS SQL Server.
    
    This class manages the connection, schema creation, and data insertion
    for the PineappleBites database.
    """
    
    def __init__(self):
        """Initialize deployer with connection details from environment"""
        self.connection = None
        self.connection_string = self._build_connection_string()
        
        # Statistics tracking
        self.stats = {
            'tables_created': 0,
            'rows_inserted': 0,
            'errors': []
        }
    
    def _build_connection_string(self) -> str:
        """
        Build ODBC connection string from environment variables.
        
        Supports two configurations:
        1. SSH Tunnel (local port forwarding):
           - DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
           - Connects to localhost via tunnel
        2. Direct connection:
           - DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD
           - Connects directly to RDS
        
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
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={db_host},{db_port};"
                f"DATABASE={db_name};"
                f"UID={db_user};"
                f"PWD={db_pass};"
                f"TrustServerCertificate=yes;"
                f"Connection Timeout=30;"
            )
            return conn_str
        
        # Fall back to direct RDS connection
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_DATABASE', 'PineappleBites')
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
        
        logger.info(f"Built direct connection string for RDS server: {server}, database: {database}")
        return conn_str
    
    def connect(self) -> None:
        """Establish connection to the RDS database"""
        try:
            logger.info("Connecting to database...")
            self.connection = pyodbc.connect(self.connection_string)
            logger.info("Successfully connected to database")
        except pyodbc.Error as e:
            error_msg = f"Failed to connect to database: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            raise
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def execute_schema(self, schema_sql: str) -> bool:
        """
        Execute schema creation SQL.
        
        Args:
            schema_sql: SQL string containing CREATE TABLE statements
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("=== DEPLOYING SCHEMA ===")
        
        try:
            cursor = self.connection.cursor()
            
            # Split on GO statements
            commands = []
            current = []
            for line in schema_sql.splitlines():
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
                        logger.error(f"Schema command {i} failed: {str(e)[:200]}")
                        self.stats['errors'].append(f"Schema command {i}: {str(e)[:200]}")
            
            cursor.close()
            self.stats['tables_created'] = success_count
            
            logger.info(f"Schema deployment complete: {success_count} commands executed")
            return len(self.stats['errors']) == 0
            
        except Exception as e:
            error_msg = f"Schema deployment failed: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
    
    def execute_data_inserts(self, data_sql: str) -> bool:
        """
        Execute data insertion SQL.
        
        Args:
            data_sql: SQL string containing INSERT statements
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("=== DEPLOYING DATA ===")
        
        try:
            cursor = self.connection.cursor()
            
            # Split on GO statements
            commands = []
            current = []
            for line in data_sql.splitlines():
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
            
            for i, command in enumerate(commands, 1):
                try:
                    cursor.execute(command)
                    total_rows += cursor.rowcount
                    success_count += 1
                    if i % 50 == 0:  # Progress logging every 50 commands
                        logger.info(f"Processed {i}/{len(commands)} insert commands...")
                except pyodbc.Error as e:
                    logger.error(f"Data insert {i} failed: {str(e)[:200]}")
                    self.stats['errors'].append(f"Data insert {i}: {str(e)[:200]}")
                    continue
            
            cursor.commit()
            cursor.close()
            
            self.stats['rows_inserted'] = total_rows
            logger.info(f"Data deployment complete: {total_rows} rows inserted")
            return len(self.stats['errors']) == 0
            
        except Exception as e:
            error_msg = f"Data deployment failed: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
    
    def verify_deployment(self) -> Dict[str, Any]:
        """
        Verify that tables exist and have data.
        
        Returns:
            Dictionary with verification results
        """
        logger.info("=== VERIFYING DEPLOYMENT ===")
        
        verification = {
            'timestamp': datetime.now().isoformat(),
            'tables': {},
            'total_rows': 0
        }
        
        expected_tables = ['company', 'team', 'resource', 'contact', 
                          'configuration', 'agreement', 'ticket', 'ticket_note']
        
        try:
            cursor = self.connection.cursor()
            
            for table in expected_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    verification['tables'][table] = {
                        'exists': True,
                        'row_count': count
                    }
                    verification['total_rows'] += count
                    logger.info(f"  {table}: {count} rows")
                except pyodbc.Error as e:
                    verification['tables'][table] = {
                        'exists': False,
                        'error': str(e)
                    }
                    logger.warning(f"  {table}: NOT FOUND or ERROR")
            
            cursor.close()
            
            logger.info(f"Verification complete: {verification['total_rows']} total rows across {len(expected_tables)} tables")
            return verification
            
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return verification
    
    def deploy_all(self, schema_sql: str, data_sql: str) -> bool:
        """
        Execute full deployment: schema + data.
        
        Args:
            schema_sql: SQL string with CREATE TABLE statements
            data_sql: SQL string with INSERT statements
            
        Returns:
            True if deployment successful, False otherwise
        """
        logger.info("="*60)
        logger.info("STARTING DATABASE DEPLOYMENT")
        logger.info("="*60)
        
        try:
            # Connect first
            self.connect()
            
            # Deploy schema
            schema_success = self.execute_schema(schema_sql)
            if not schema_success:
                logger.error("Schema deployment failed, aborting")
                return False
            
            # Deploy data
            data_success = self.execute_data_inserts(data_sql)
            if not data_success:
                logger.warning("Data deployment had errors, but continuing to verification")
            
            # Verify
            verification = self.verify_deployment()
            
            # Summary
            logger.info("="*60)
            logger.info("DEPLOYMENT SUMMARY")
            logger.info("="*60)
            logger.info(f"Tables created/verified: {self.stats['tables_created']}")
            logger.info(f"Total rows inserted: {self.stats['rows_inserted']}")
            logger.info(f"Total errors: {len(self.stats['errors'])}")
            
            if self.stats['errors']:
                logger.warning("Errors encountered during deployment:")
                for error in self.stats['errors'][:10]:  # Show first 10 errors
                    logger.warning(f"  - {error}")
                if len(self.stats['errors']) > 10:
                    logger.warning(f"  ... and {len(self.stats['errors']) - 10} more errors")
            
            success = len(self.stats['errors']) == 0
            if success:
                logger.info("✓ Deployment completed successfully!")
            else:
                logger.warning("✓ Deployment completed with errors")
            
            return success
            
        except Exception as e:
            logger.error(f"Deployment failed with exception: {str(e)}")
            self.stats['errors'].append(str(e))
            return False
        
        finally:
            self.disconnect()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for the deployment script"""
    parser = argparse.ArgumentParser(
        description='Deploy PineappleBites database to AWS RDS SQL Server'
    )
    parser.add_argument(
        '--schema-only',
        action='store_true',
        help='Deploy schema only (no data)'
    )
    parser.add_argument(
        '--data-only',
        action='store_true',
        help='Deploy data only (assumes schema exists)'
    )
    parser.add_argument(
        '--data-file',
        default='sample_data.sql',
        help='Path to data SQL file (default: sample_data.sql)'
    )
    parser.add_argument(
        '--output-verification',
        help='Path to save verification JSON report'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.schema_only and args.data_only:
        logger.error("Cannot use --schema-only and --data-only together")
        sys.exit(1)
    
    # Check if data file exists
    if not args.schema_only and not os.path.exists(args.data_file):
        logger.error(f"Data file not found: {args.data_file}")
        sys.exit(1)
    
    # Load data SQL if needed
    data_sql = ""
    if not args.schema_only:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            data_sql = f.read()
    
    # Create deployer
    deployer = DatabaseDeployer()
    
    try:
        success = False
        
        if args.schema_only:
            logger.info("Mode: Schema deployment only")
            deployer.connect()
            success = deployer.execute_schema(SCHEMA_SQL)
            deployer.disconnect()
            
        elif args.data_only:
            logger.info("Mode: Data deployment only")
            success = deployer.deploy_all("", data_sql)
            
        else:
            logger.info("Mode: Full deployment (schema + data)")
            success = deployer.deploy_all(SCHEMA_SQL, data_sql)
        
        # Save verification report if requested
        if args.output_verification and success:
            verification = deployer.verify_deployment()
            with open(args.output_verification, 'w') as f:
                json.dump(verification, f, indent=2)
            logger.info(f"Verification report saved to: {args.output_verification}")
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.warning("Deployment interrupted by user")
        deployer.disconnect()
        sys.exit(130)
    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}")
        deployer.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    main()