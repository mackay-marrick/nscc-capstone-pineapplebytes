#!/usr/bin/env python3
"""
Phase 2 Python Middleware for PineappleBytes Data Pipeline

This module extracts client data from Microsoft SQL Server, tokenizes PII,
prepares JSON payloads, and sends them to an LLM via OpenRouter API.

Workflow:
1. Database Extraction: Execute separate, targeted queries (no massive joins)
2. Tokenization: Mask PII fields (names, phone numbers) with tokens
3. Payload Preparation: Format masked data into clean JSON structure
4. OpenRouter Integration: Send to LLM for summarization

Offline Mode:
If network connectivity is lost (e.g., school network blocking AWS RDS/OpenRouter),
the middleware can fall back to cached data from previous successful runs.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Third-party libraries (install via pip: pyodbc python-dotenv openai)
import pyodbc
from dotenv import load_dotenv
from openai import OpenAI

# Import cache manager
from cache_manager import CacheManager

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class CompanyProfile:
    """Complete company profile with related data"""
    company_id: int
    company_name: str
    location: str
    department: str
    contacts: List[Dict[str, Any]]
    agreements: List[Dict[str, Any]]
    tickets: List[Dict[str, Any]]


# ============================================================================
# DATABASE EXTRACTION (Separate Targeted Queries)
# ============================================================================

class DatabaseExtractor:
    """
    Handles connection to SQL Server and extraction of comprehensive company data.
    
    This class establishes a connection using pyodbc and executes separate,
    targeted queries to avoid Cartesian product/data fan-out.
    """
    
    def __init__(self, connection_string: str = None):
        """
        Initialize the database extractor.
        
        Args:
            connection_string: Optional ODBC connection string. If None, builds
                              from environment variables.
        """
        self.connection_string = connection_string or self._build_connection_string()
        self.connection = None
    
    def _build_connection_string(self) -> str:
        """
        Construct ODBC connection string from environment variables.
        
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
            )
            return conn_str
        
        # Fall back to direct RDS connection
        server = os.getenv('DB_SERVER', 'localhost\\SQLEXPRESS')
        database = os.getenv('DB_DATABASE', 'PineappleBytes')
        username = os.getenv('DB_USERNAME', '')
        password = os.getenv('DB_PASSWORD', '')
        
        if username and password:
            # SQL Server Authentication
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
                f"TrustServerCertificate=yes;"
            )
        else:
            # Windows Authentication
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
        
        logger.info(f"Built direct connection string for server: {server}, database: {database}")
        return conn_str
    
    def connect(self) -> None:
        """Establish database connection"""
        try:
            # Set timeout for connection (30 seconds)
            self.connection = pyodbc.connect(self.connection_string, timeout=30)
            logger.info("Successfully connected to SQL Server database")
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def extract_company_profile(self, company_id: int) -> CompanyProfile:
        """
        Extract a complete profile for a single company using separate queries.
        
        This method executes multiple targeted queries to avoid the Cartesian
        product problem that occurs with massive LEFT JOINs. Each related table
        is queried independently and results are assembled cleanly.
        
        Queries executed:
        1. Company base info
        2. Contacts (where company_id = ?)
        3. Agreements (where company_id = ?)
        4. Tickets (where company_id = ?)
        
        Args:
            company_id: The unique identifier of the company to extract
            
        Returns:
            CompanyProfile object containing all related data
            
        Raises:
            ValueError: If company_id not found or query fails
        """
        if not self.connection:
            self.connect()
        
        try:
            # Query 1: Company base data
            company = self._query_company(company_id)
            if not company:
                raise ValueError(f"Company with ID {company_id} not found")
            
            # Query 2: Contacts for this company
            contacts = self._query_contacts(company_id)
            
            # Query 3: Agreements for this company
            agreements = self._query_agreements(company_id)
            
            # Query 4: Tickets for this company
            tickets = self._query_tickets(company_id)
            
            # Build the CompanyProfile object
            profile = CompanyProfile(
                company_id=company['company_id'],
                company_name=company['company_name'],
                location=company['location'],
                department=company['department'],
                contacts=contacts,
                agreements=agreements,
                tickets=tickets
            )
            
            logger.info(
                f"Profile assembled: {len(contacts)} contacts, "
                f"{len(agreements)} agreements, {len(tickets)} tickets"
            )
            
            return profile
            
        except pyodbc.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def _query_company(self, company_id: int) -> Dict[str, Any]:
        """Query the company table for a single company"""
        query = """
        SELECT company_id, company_name, location, department
        FROM company
        WHERE company_id = ?
        """
        cursor = self.connection.cursor()
        cursor.execute(query, company_id)
        row = cursor.fetchone()
        
        if not row:
            return None
        
        columns = [desc[0] for desc in cursor.description]
        company = dict(zip(columns, row))
        logger.info(f"Retrieved company: {company['company_name']}")
        return company
    
    def _query_contacts(self, company_id: int) -> List[Dict[str, Any]]:
        """Query all contacts for a given company"""
        query = """
        SELECT 
            contact_id,
            first_name,
            last_name,
            phone_number,
            extension,
            title,
            relationship,
            contact_type,
            email
        FROM contact
        WHERE company_id = ?
        ORDER BY contact_id
        """
        cursor = self.connection.cursor()
        cursor.execute(query, company_id)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        contacts = []
        for row in rows:
            contact = dict(zip(columns, row))
            contacts.append(contact)
        
        logger.info(f"Retrieved {len(contacts)} contacts for company_id {company_id}")
        return contacts
    
    def _query_agreements(self, company_id: int) -> List[Dict[str, Any]]:
        """Query all agreements for a given company"""
        query = """
        SELECT 
            agreement_id,
            agreement_type,
            agreement_name,
            amount,
            billing_cycle,
            date_start,
            date_end,
            status as agreement_status
        FROM agreement
        WHERE company_id = ?
        ORDER BY agreement_id
        """
        cursor = self.connection.cursor()
        cursor.execute(query, company_id)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        agreements = []
        for row in rows:
            agreement = dict(zip(columns, row))
            # Convert date fields to string format
            if hasattr(agreement['date_start'], 'strftime'):
                agreement['date_start'] = agreement['date_start'].strftime('%Y-%m-%d')
            if hasattr(agreement['date_end'], 'strftime'):
                agreement['date_end'] = agreement['date_end'].strftime('%Y-%m-%d')
            # Convert amount to float if present
            if agreement['amount'] is not None:
                agreement['amount'] = float(agreement['amount'])
            agreements.append(agreement)
        
        logger.info(f"Retrieved {len(agreements)} agreements for company_id {company_id}")
        return agreements
    
    def _query_tickets(self, company_id: int) -> List[Dict[str, Any]]:
        """Query all tickets for a given company"""
        query = """
        SELECT 
            ticket_id,
            total_hours,
            age,
            status as ticket_status,
            schedule_flag,
            summary_description,
            priority,
            budget,
            ticket_type,
            subtype,
            item,
            date_entered,
            team_name
        FROM ticket
        WHERE company_id = ?
        ORDER BY ticket_id
        """
        cursor = self.connection.cursor()
        cursor.execute(query, company_id)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        tickets = []
        for row in rows:
            ticket = dict(zip(columns, row))
            # Convert numeric fields to float if present
            if ticket['total_hours'] is not None:
                ticket['total_hours'] = float(ticket['total_hours'])
            if ticket['age'] is not None:
                ticket['age'] = float(ticket['age'])
            if ticket['budget'] is not None:
                ticket['budget'] = float(ticket['budget'])
            # Convert date field to string format
            if hasattr(ticket['date_entered'], 'strftime'):
                ticket['date_entered'] = ticket['date_entered'].strftime('%Y-%m-%d')
            tickets.append(ticket)
        
        logger.info(f"Retrieved {len(tickets)} tickets for company_id {company_id}")
        return tickets


# ============================================================================
# TOKENIZATION (DATA MASKING)
# ============================================================================

class DataTokenizer:
    """
    Sanitizes extracted data by tokenizing Personally Identifiable Information (PII).
    
    This class identifies sensitive fields in contact data (names, phone numbers)
    and replaces them with generic tokens while maintaining a secure local mapping
    that could be used for de-tokenization if needed within the secure environment.
    """
    
    def __init__(self):
        """Initialize the tokenizer with an empty mapping dictionary"""
        # Local dictionary mapping tokens back to original values
        # Structure: {'[CLIENT_NAME_1]': {'first_name': 'John', 'last_name': 'Doe'}, ...}
        self.token_map: Dict[str, Dict[str, str]] = {}
        self.name_counter = 0
        self.phone_counter = 0
    
    def _generate_name_token(self) -> str:
        """Generate a unique token for a name"""
        self.name_counter += 1
        return f"[CLIENT_NAME_{self.name_counter}]"
    
    def _generate_phone_token(self) -> str:
        """Generate a unique token for a phone number"""
        self.phone_counter += 1
        return f"[CLIENT_PHONE_{self.phone_counter}]"
    
    def tokenize_contact(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tokenize PII fields in a single contact record.
        
        This method:
        1. Identifies name fields (first_name, last_name)
        2. Identifies phone fields (phone_number)
        3. Replaces with tokens and updates token_map
        
        Args:
            contact: Original contact dictionary
            
        Returns:
            New contact dictionary with PII replaced by tokens
        """
        tokenized = contact.copy()
        
        # Tokenize full name (first + last)
        full_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
        if full_name:
            name_token = self._generate_name_token()
            self.token_map[name_token] = {
                'first_name': contact.get('first_name', ''),
                'last_name': contact.get('last_name', '')
            }
            tokenized['first_name'] = '[REDACTED]'
            tokenized['last_name'] = '[REDACTED]'
            # Store original in token_map with token as key
            # We'll keep the token reference if needed later
            tokenized['_name_token'] = name_token  # Optional: track token
        
        # Tokenize phone number
        phone = contact.get('phone_number')
        if phone:
            phone_token = self._generate_phone_token()
            self.token_map[phone_token] = {
                'phone_number': phone,
                'extension': contact.get('extension', '')
            }
            tokenized['phone_number'] = '[REDACTED]'
            tokenized['extension'] = '[REDACTED]'
            tokenized['_phone_token'] = phone_token
        
        # Email might also be PII, but we'll leave it as-is for now
        # Could extend to tokenize email if required
        
        return tokenized
    
    def tokenize_profile(self, profile: CompanyProfile) -> Dict[str, Any]:
        """
        Tokenize all PII in a company profile.
        
        Processes the entire CompanyProfile:
        - Tokenizes all contacts in the profile
        - Returns a dictionary representation with masked data
        
        Args:
            profile: Complete company profile to sanitize
            
        Returns:
            Dictionary with masked PII, ready for JSON serialization
        """
        logger.info(f"Tokenizing profile for company: {profile.company_name}")
        
        # Tokenize all contacts
        tokenized_contacts = [
            self.tokenize_contact(contact) 
            for contact in profile.contacts
        ]
        
        # Build sanitized profile dictionary
        sanitized = {
            'company': {
                'company_id': profile.company_id,
                'company_name': profile.company_name,
                'location': profile.location,
                'department': profile.department
            },
            'contacts': tokenized_contacts,
            'agreements': profile.agreements,  # No PII in agreements typically
            'tickets': profile.tickets,        # May contain customer names in descriptions (out of scope)
            'metadata': {
                'total_contacts': len(tokenized_contacts),
                'total_agreements': len(profile.agreements),
                'total_tickets': len(profile.tickets),
                'tokenization_timestamp': self._get_current_timestamp()
            }
        }
        
        logger.info(
            f"Tokenization complete. Generated {self.name_counter} name tokens "
            f"and {self.phone_counter} phone tokens"
        )
        
        return sanitized
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_token_map(self, filepath: str = 'token_map.json') -> None:
        """
        Save the token mapping dictionary to a local file.
        
        WARNING: This file contains sensitive PII mappings and should be
        stored securely with appropriate access controls. Consider encrypting
        or using a secure secrets manager in production.
        
        Args:
            filepath: Path to save the token mapping JSON file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.token_map, f, indent=2)
            logger.info(f"Token mapping saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save token map: {e}")
            raise


# ============================================================================
# API PAYLOAD PREPARATION
# ============================================================================

class PayloadPreparer:
    """
    Formats masked data into a clean JSON payload optimized for LLM consumption.
    
    This class transforms the sanitized company profile into a well-structured
    JSON format that clearly presents the information while maintaining data
    privacy standards.
    """
    
    def prepare_payload(self, sanitized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare the final API payload structure.
        
        This method:
        1. Validates and formats the sanitized data
        2. Creates a clear hierarchical structure
        3. Adds any necessary metadata for the LLM
        
        Args:
            sanitized_data: Tokenized company profile dictionary
            
        Returns:
            Clean JSON-serializable dictionary ready for API submission
        """
        logger.info("Preparing API payload from sanitized data")
        
        payload = {
            'client_profile': {
                'company': sanitized_data['company'],
                'contacts': self._format_contacts(sanitized_data['contacts']),
                'agreements': self._format_agreements(sanitized_data['agreements']),
                'tickets': self._format_tickets(sanitized_data['tickets'])
            },
            'summary_context': {
                'data_completeness': self._assess_completeness(sanitized_data),
                'key_metrics': self._calculate_metrics(sanitized_data)
            }
        }
        
        payload_size = len(json.dumps(payload))
        logger.info(f"Payload prepared: {payload_size} characters")
        return payload
    
    def _format_contacts(self, contacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format contact list for clear presentation.
        
        Creates a simplified view focusing on roles and relationships.
        """
        formatted = []
        for contact in contacts:
            formatted.append({
                'contact_id': contact.get('contact_id'),
                'name': '[REDACTED]',  # Tokens replace actual names
                'title': contact.get('title'),
                'relationship': contact.get('relationship'),
                'contact_type': contact.get('contact_type'),
                'email': contact.get('email'),
                'phone': contact.get('phone_number')  # Already tokenized
            })
        return formatted
    
    def _format_agreements(self, agreements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format agreement data focused on business terms and status.
        """
        formatted = []
        for agreement in agreements:
            formatted.append({
                'agreement_id': agreement.get('agreement_id'),
                'type': agreement.get('agreement_type'),
                'name': agreement.get('agreement_name'),
                'value': agreement.get('amount'),
                'billing_cycle_days': agreement.get('billing_cycle'),
                'term_start': agreement.get('date_start'),
                'term_end': agreement.get('date_end'),
                'status': agreement.get('agreement_status')
            })
        return formatted
    
    def _format_tickets(self, tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format ticket data highlighting issues and service history.
        """
        formatted = []
        for ticket in tickets:
            formatted.append({
                'ticket_id': ticket.get('ticket_id'),
                'summary': ticket.get('summary_description'),
                'type': ticket.get('ticket_type'),
                'subtype': ticket.get('subtype'),
                'priority': ticket.get('priority'),
                'status': ticket.get('ticket_status'),
                'budget': ticket.get('budget'),
                'team_assigned': ticket.get('team_name'),
                'date_entered': ticket.get('date_entered')
            })
        return formatted
    
    def _assess_completeness(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess data completeness and identify missing critical information.
        """
        company = data.get('company', {})
        contacts = data.get('contacts', [])
        agreements = data.get('agreements', [])
        tickets = data.get('tickets', [])
        
        completeness = {
            'has_contacts': len(contacts) > 0,
            'has_agreements': len(agreements) > 0,
            'has_tickets': len(tickets) > 0,
            'contact_count': len(contacts),
            'agreement_count': len(agreements),
            'ticket_count': len(tickets),
            'missing_critical_info': []
        }
        
        # Check for missing critical business information
        if not contacts:
            completeness['missing_critical_info'].append('No contact records found')
        if not agreements:
            completeness['missing_critical_info'].append('No agreement records found')
        
        # Check if department is specified (critical for business categorization)
        if not company.get('department'):
            completeness['missing_critical_info'].append('Company department not specified')
        
        # Check for any active agreements
        active_agreements = [a for a in agreements if a.get('status') == 'Active']
        if not active_agreements and agreements:
            completeness['missing_critical_info'].append('No active agreements found')
        
        return completeness
    
    def _calculate_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate key metrics from the data for LLM context.
        """
        tickets = data.get('tickets', [])
        agreements = data.get('agreements', [])
        
        metrics = {
            'total_tickets': len(tickets),
            'open_tickets': len([t for t in tickets if t.get('status') == 'Open']),
            'total_agreements': len(agreements),
            'active_agreements': len([a for a in agreements if a.get('status') == 'Active']),
            'total_contract_value': sum(
                float(a.get('amount', 0)) for a in agreements if a.get('amount')
            )
        }
        
        # Add ticket priority breakdown if tickets exist
        if tickets:
            priorities = {}
            for ticket in tickets:
                priority = ticket.get('priority', 'Unknown')
                priorities[priority] = priorities.get(priority, 0) + 1
            metrics['ticket_priorities'] = priorities
        
        return metrics


# ============================================================================
# OPENROUTER API INTEGRATION
# ============================================================================

class OpenRouterClient:
    """
    Handles communication with OpenRouter API to send data to LLM.
    
    This client uses the OpenAI Python library but configures it to route
    through OpenRouter's gateway, allowing access to various models including
    the StepFun model specified.
    """
    
    def __init__(self):
        """
        Initialize the OpenRouter client with API key from environment.
        
        Requires OPENROUTER_API_KEY in .env file or environment variables.
        """
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        
        # Configure OpenAI client to use OpenRouter endpoint
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Specify the model as requested
        self.model = "stepfun/step-3.5-flash:free"
        
        # Token usage tracking
        self.total_tokens_used = 0
        self.api_calls_count = 0
        
        logger.info(f"OpenRouter client initialized with model: {self.model}")
    
    def generate_summary(self, payload: Dict[str, Any], system_prompt: str = None, timeout: int = 60) -> str:
        """
        Send payload to OpenRouter LLM and receive a summary.
        
        Args:
            payload: The prepared JSON payload containing client data
            system_prompt: Optional custom system prompt. If None, uses default.
            timeout: Timeout in seconds for the API call (default: 60)
            
        Returns:
            LLM-generated summary text
            
        Raises:
            Exception: If API call fails or times out
        """
        if system_prompt is None:
            system_prompt = (
                "Summarize this client data into a professional overview, "
                "highlighting any missing critical business information."
            )
        
        # Convert payload to JSON string for the API
        user_content = json.dumps(payload, indent=2)
        
        try:
            logger.info(f"Sending request to OpenRouter API (model: {self.model}, timeout: {timeout}s)")
            
            # Set timeout for the request using OpenAI client's timeout parameter
            import httpx
            timeout_config = httpx.Timeout(timeout)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_content
                    }
                ],
                temperature=0.7,  # Balanced creativity
                max_tokens=2000,  # Increased from 1000, lower than default to avoid reserving too many tokens
                timeout=timeout_config,
                extra_headers={
                    "HTTP-Referer": "https://github.com/mackay-marrick/nscc-capstone-pineapplebytes",
                    "X-Title": "PineappleBytes Middleware"
                }
            )
            
            # Extract the summary text and track token usage
            if response.choices and len(response.choices) > 0:
                summary = response.choices[0].message.content
                logger.info(f"Received summary response: {len(summary)} characters")
                
                # Track token usage if available in response
                if hasattr(response, 'usage') and response.usage:
                    tokens_used = response.usage.total_tokens
                    self.total_tokens_used += tokens_used
                    self.api_calls_count += 1
                    logger.info(f"API call used {tokens_used} tokens. Total this session: {self.total_tokens_used}")
                
                return summary
            else:
                logger.warning("Empty response received from API")
                return "No summary generated - empty response from API"
                
        except Exception as e:
            logger.error(f"OpenRouter API request failed: {e}")
            raise
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage statistics for this client instance"""
        return {
            'total_tokens': self.total_tokens_used,
            'api_calls': self.api_calls_count
        }
    
    def reset_token_usage(self) -> None:
        """Reset token usage counters"""
        self.total_tokens_used = 0
        self.api_calls_count = 0
        logger.info("Token usage counters reset")


# ============================================================================
# MAIN MIDDLEWARE ENGINE
# ============================================================================

class MiddlewareEngine:
    """
    Main orchestrator for the Phase 2 data pipeline middleware.
    
    This class coordinates the complete workflow:
    1. Extract data from database (using separate queries)
    2. Tokenize PII
    3. Prepare API payload
    4. Send to OpenRouter LLM
    5. Return summary
    
    Offline Mode:
    If network connectivity fails, the engine can fall back to cached data
    from previous successful runs (if available).
    
    Usage:
        engine = MiddlewareEngine()
        summary = engine.process_company(company_id=26)
    """
    
    def __init__(self, db_connection_string: str = None, enable_cache: bool = True):
        """
        Initialize middleware engine with optional database connection string.
        
        Args:
            db_connection_string: Optional custom ODBC connection string
            enable_cache: Whether to enable offline cache fallback (default: True)
        """
        self.extractor = DatabaseExtractor(db_connection_string)
        self.tokenizer = DataTokenizer()
        self.payload_preparer = PayloadPreparer()
        self.api_client = OpenRouterClient()
        self.cache_manager = CacheManager() if enable_cache else None
        self.offline_mode_used = False
    
    def process_company(self, company_id: int, save_token_map: bool = True, force_offline: bool = False) -> str:
        """
        Complete end-to-end processing for a single company.
        
        This method executes the full pipeline:
        1. Extract company profile from database (separate queries)
        2. Tokenize all PII in the data
        3. Prepare clean JSON payload
        4. Send to OpenRouter LLM
        5. Return the generated summary
        
        If network connectivity fails and cache is enabled, it will attempt to
        load cached data and summary from a previous successful run.
        
        Args:
            company_id: The company ID to process
            save_token_map: Whether to save token mapping file (default: True)
            force_offline: If True, skip live database/API calls and use cache only
            
        Returns:
            LLM-generated summary string
            
        Raises:
            Various exceptions from underlying components if cache unavailable
        """
        # Validate company_id input
        if not isinstance(company_id, int):
            raise TypeError(f"company_id must be an integer, got {type(company_id).__name__}")
        if company_id <= 0:
            raise ValueError(f"company_id must be a positive integer, got {company_id}")
        
        logger.info(f"Starting middleware processing for company_id: {company_id}")
        
        # Check if we should use offline mode
        if force_offline and self.cache_manager:
            logger.info("Force offline mode enabled - using cached data only")
            cached_data = self.cache_manager.load_from_cache(company_id)
            if cached_data:
                self.offline_mode_used = True
                logger.info("Successfully loaded data from cache (offline mode)")
                return cached_data['summary']
            else:
                raise ValueError(f"No cached data available for company {company_id}. Cannot run in offline mode.")
        
        # Check cache first as fallback (only if cache exists)
        if self.cache_manager:
            cached_data = self.cache_manager.load_from_cache(company_id)
            if cached_data:
                logger.info(f"Found cached data for company {company_id} - will use if live processing fails")
        
        try:
            # STEP 1: Extract data from database (separate queries)
            logger.info("=== STEP 1: Database Extraction ===")
            profile = self.extractor.extract_company_profile(company_id)
            logger.info(f"Extracted profile: {profile.company_name}")
            
            # STEP 2: Tokenize PII
            logger.info("\n=== STEP 2: Tokenization ===")
            sanitized_data = self.tokenizer.tokenize_profile(profile)
            
            if save_token_map:
                self.tokenizer.save_token_map()
            
            # STEP 3: Prepare API payload
            logger.info("\n=== STEP 3: Payload Preparation ===")
            payload = self.payload_preparer.prepare_payload(sanitized_data)
            
            # Optional: Log payload to file for debugging (in secure location)
            # with open(f'payload_company_{company_id}.json', 'w') as f:
            #     json.dump(payload, f, indent=2)
            
            # STEP 4: Send to OpenRouter LLM
            logger.info("\n=== STEP 4: OpenRouter Integration ===")
            summary = self.api_client.generate_summary(payload)
            
            # Save successful result to cache for future offline use
            if self.cache_manager:
                try:
                    self.cache_manager.save_to_cache(company_id, sanitized_data, summary)
                    logger.info("Saved processing result to cache for future offline use")
                except Exception as e:
                    logger.warning(f"Failed to save to cache: {e}")
            
            logger.info(f"\n=== PROCESSING COMPLETE ===\nGenerated Summary:\n{summary}")
            
            return summary
            
        except Exception as e:
            logger.error(f"Middleware processing failed: {e}")
            
            # If cache is available, fall back to offline mode
            if self.cache_manager and cached_data:
                logger.warning("Live processing failed, falling back to cached data (offline mode)")
                self.offline_mode_used = True
                return cached_data['summary']
            
            # No cache available, re-raise exception
            raise
    
    def cleanup(self):
        """Cleanup resources, close database connections"""
        self.extractor.disconnect()


# ============================================================================
# SCRIPT ENTRY POINT (for testing without execution)
# ============================================================================

if __name__ == "__main__":
    """
    This block is for local testing only and should be commented out or
    removed in production. The middleware is designed to be imported and
    used by other scripts or called from the command line with arguments.
    
    To test locally:
    1. Create a .env file with:
       - DB_SERVER=your_server
       - DB_DATABASE=pineapplebytes-db
       - DB_USERNAME=your_user (or use Windows Auth)
       - DB_PASSWORD=your_pass (if using SQL auth)
       - OPENROUTER_API_KEY=your_key
       
   2. Run: python middleware_engine.py --company-id 26
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Process company data through middleware pipeline')
    parser.add_argument('--company-id', type=int, default=26, help='Company ID to process')
    parser.add_argument('--no-save-tokens', action='store_true', help='Do not save token mapping file')
    
    args = parser.parse_args()
    
    # Validate company_id (additional validation beyond type checking)
    if args.company_id <= 0:
        print(f"Error: company_id must be a positive integer, got {args.company_id}")
        sys.exit(1)
    
    # Create engine and process
    engine = MiddlewareEngine()
    try:
        summary = engine.process_company(
            company_id=args.company_id,
            save_token_map=not args.no_save_tokens
        )
        print("\n" + "="*60)
        print("FINAL SUMMARY:")
        print("="*60)
        print(summary)
        print("="*60)
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
    finally:
        engine.cleanup()