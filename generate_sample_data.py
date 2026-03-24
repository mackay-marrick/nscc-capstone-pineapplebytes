#!/usr/bin/env python3
"""
Generates 50 rows of realistic sample data for the PineappleBites database schema.
Uses Faker library to create fabricated data respecting foreign key relationships.
Outputs SQL INSERT statements to 'sample_data.sql' with SQL Server syntax.
"""

import random
from datetime import datetime, timedelta
from faker import Faker
from collections import defaultdict

fake = Faker()

# Configuration: Current max IDs from existing data
ID_START = {
    'company': 26,          # existing 1-25
    'team': 81,             # existing max 80 (10,20,30,40,50,60,70,80)
    'resource': 713,        # existing 703-712
    'contact': 126,         # existing 101-125
    'configuration': 825,  # existing 801-824
    'agreement': 525,       # existing 501-524
    'ticket': 9026,         # existing 9001-9025
    'ticket_note': 1        # new table
}

# Existing reference data (sample to maintain consistency)
EXISTING_TEAMS = [
    'On-Site Technicians', 'Remote Software Support', 'POS Hardware Repair',
    'Network Infrastructure', 'Cloud Systems Admin', 'Customer Success',
    'Menu & Pricing Ops', 'Emergency Response'
]

EXISTING_CONFIGURATIONS = list(range(801, 825))  # IDs 801-824

# Departments from company table
DEPARTMENTS = ['Operations', 'IT Support', 'Management', 'Technical Services', 'Procurement', 'Kitchen', 'Admin', 'Support', 'IT', 'Technical']

# Ticket statuses, priorities, types (from existing data)
TICKET_STATUSES = ['Open', 'In Progress', 'Closed', 'Pending']
TICKET_PRIORITIES = ['High', 'Medium', 'Low', 'Emergency']
TICKET_TYPES = ['Hardware', 'Software', 'Maintenance', 'Network', 'Service', 'Project']
TICKET_SUBTYPES = ['Repair', 'Update', 'Audit', 'Replacement', 'Training', 'Config', 'Clean', 'Admin', 'Critical', 'Sync', 'Reboot', 'New', 'Install', 'Reader', 'Supply', 'Cable', 'Wifi', 'Power', 'Mobile', 'Server', 'Install', 'Train', 'Scanner']
TICKET_ITEMS = ['401', '205', '110', '302', '550', '806', '807', '810', '805', '823', '806', '824', '816', '817', '809', '807', '821', '820', '818', '819', '814', '815', '814', '811', '821']  # from existing
SCHEDULE_FLAGS = ['Scheduled', 'Unscheduled', 'S', 'U']

# Agreement types and statuses
AGREEMENT_TYPES = ['SLA', 'Maintenance', 'Subscription', 'Software', 'Service', 'Hardware', 'Project']
AGREEMENT_STATUSES = ['Active', 'Expiring', 'Pending', 'Closed']
BILLING_CYCLES = ['30', '90', '365', '0']

# Configuration types and statuses
CONFIG_TYPES = ['Terminal', 'Monitor', 'Server', 'Handheld', 'Hardware', 'Network', 'Mobile', 'Stand', 'Battery']
CONFIG_STATUSES = ['Online', 'Damaged', 'In Repair', 'Offline', 'Broken', 'Repair']

# Contact types and relationships
CONTACT_TYPES = ['Client', 'Vendor', 'Partner', 'Internal']
CONTACT_RELATIONSHIPS = ['Primary', 'Secondary', 'Technical', 'Billing']
CONTACT_TITLES = ['CEO', 'Owner', 'Manager', 'Director', 'Chef', 'IT Lead', 'IT Tech', 'Admin', 'Supervisor', 'Clerk', 'Intern', 'Reporter', 'Partner', 'Cashier', 'Purchasing', 'Head Chef', 'Computer', 'Partner', 'Technician']

def generate_companies(num_rows):
    """Generate company data"""
    companies = []
    for i in range(num_rows):
        company_id = ID_START['company'] + i
        company_name = fake.company()
        location = f"{fake.city()}, {fake.state_abbr()}"
        department = random.choice(DEPARTMENTS)
        companies.append((company_id, company_name, location, department))
    return companies

def generate_teams(num_rows):
    """Generate team data - using realistic team names"""
    teams = []
    for i in range(num_rows):
        team_id = ID_START['team'] + (i * 10)  # increment by 10 to match existing pattern
        team_name = f"{fake.catch_phrase().title()} Team"
        teams.append((team_id, team_name))
    return teams

def generate_resources(num_rows):
    """Generate resource (person) data"""
    resources = []
    for i in range(num_rows):
        resource_id = ID_START['resource'] + i
        resource_name = fake.name()
        resources.append((resource_id, resource_name))
    return resources

def generate_contacts(num_rows, company_ids):
    """Generate contact data with company_id foreign key"""
    contacts = []
    for i in range(num_rows):
        contact_id = ID_START['contact'] + i
        company_id = random.choice(company_ids)  # Assign to random company
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = fake.phone_number()
        extension = str(random.randint(0, 999))
        title = random.choice(CONTACT_TITLES)
        relationship = random.choice(CONTACT_RELATIONSHIPS)
        contact_type = random.choice(CONTACT_TYPES)
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
        contacts.append((contact_id, company_id, first_name, last_name, phone_number, extension, title, relationship, contact_type, email))
    return contacts

def generate_configurations(num_rows):
    """Generate configuration/hardware data"""
    configs = []
    for i in range(num_rows):
        config_id = ID_START['configuration'] + i
        config_name = f"{fake.catch_phrase().title()} {random.choice(['Unit', 'Device', 'System', 'Terminal', 'Display'])}"
        config_type = random.choice(CONFIG_TYPES)
        status = random.choice(CONFIG_STATUSES)
        serial_number = fake.ean13() if random.choice([True, False]) else fake.ean8()
        tag_number = f"TAG-{random.randint(1000, 9999)}"
        model_number = f"MOD-{random.randint(100, 999)}"
        purchased_date = fake.date_between(start_date='-3y', end_date='today')
        configs.append((config_id, config_name, config_type, status, serial_number, tag_number, model_number, purchased_date))
    return configs

def generate_agreements(num_rows, company_ids):
    """Generate agreement data with company_id foreign key"""
    agreements = []
    for i in range(num_rows):
        agreement_id = ID_START['agreement'] + i
        company_id = random.choice(company_ids)  # Assign to random company
        agreement_type = random.choice(AGREEMENT_TYPES)
        agreement_name = f"{fake.catch_phrase().title()} Agreement"
        amount = f"{round(random.uniform(50, 10000), 2):.2f}"
        billing_cycle = random.choice(BILLING_CYCLES)
        date_start = fake.date_between(start_date='-2y', end_date='today')
        # date_end is typically start + cycle days (or longer for annual)
        if billing_cycle == '0':
            date_end = date_start + timedelta(days=random.randint(30, 180))
        else:
            date_end = date_start + timedelta(days=int(billing_cycle) * random.randint(1, 3))
        status = random.choice(AGREEMENT_STATUSES)
        agreements.append((agreement_id, company_id, agreement_type, agreement_name, amount, billing_cycle, date_start, date_end, status))
    return agreements

def generate_tickets(num_rows, company_ids):
    """Generate ticket data with company_id foreign key"""
    tickets = []
    # We'll generate both new teams and use some existing ones
    all_teams = EXISTING_TEAMS + [f"Team {i}" for i in range(100, 100+num_rows)]
    for i in range(num_rows):
        ticket_id = ID_START['ticket'] + i
        company_id = random.choice(company_ids)  # Assign to random company
        total_hours = round(random.uniform(0, 20), 2)
        age = round(random.uniform(0, 100), 1)
        status = random.choice(TICKET_STATUSES)
        schedule_flag = random.choice(SCHEDULE_FLAGS)
        summary_description = fake.sentence(nb_words=random.randint(5, 12))
        priority = random.choice(TICKET_PRIORITIES)
        budget = round(random.uniform(0, 5000), 2)
        ticket_type = random.choice(TICKET_TYPES)
        subtype = random.choice(TICKET_SUBTYPES)
        item = str(random.choice(EXISTING_CONFIGURATIONS))  # reference configuration_id as string
        date_entered = fake.date_between(start_date='-6m', end_date='today')
        team_name = random.choice(all_teams)
        tickets.append((ticket_id, company_id, total_hours, age, status, schedule_flag, summary_description, priority, budget, ticket_type, subtype, item, date_entered, team_name))
    return tickets

def generate_ticket_notes(num_rows, ticket_start_id):
    """Generate ticket_note data - multiple notes per ticket"""
    notes = []
    note_id_counter = ID_START['ticket_note']
    # Each ticket gets 1-5 notes on average
    notes_per_ticket = [random.randint(1, 5) for _ in range(num_rows)]
    total_notes = sum(notes_per_ticket)
    
    note_idx = 0
    for i, count in enumerate(notes_per_ticket):
        ticket_id = ticket_start_id + i
        for j in range(count):
            note_id = note_id_counter + note_idx
            note_text = fake.paragraph(nb_sentences=random.randint(2, 5))
            created_date = fake.date_time_between(start_date='-6m', end_date='now')
            author = fake.name()
            notes.append((note_id, ticket_id, note_text, created_date, author))
            note_idx += 1
    return notes

def write_sql_file(all_data):
    """Write all data to sample_data.sql with SQL Server syntax"""
    with open('sample_data.sql', 'w', encoding='utf-8') as f:
        f.write("-- PineappleBites Sample Data\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- Total rows: 8 tables x 50 each = 400\n\n")
        
        # Write INSERT statements for each table
        for table_name, rows in all_data.items():
            f.write(f"--\n-- Table `{table_name}`\n--\n")
            for row in rows:
                # Escape single quotes in strings
                escaped_row = []
                for val in row:
                    if isinstance(val, str):
                        val = val.replace("'", "''")
                        escaped_row.append(f"'{val}'")
                    elif isinstance(val, datetime):
                        escaped_row.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                    else:
                        escaped_row.append(str(val))
                # Use SQL Server syntax: INSERT INTO [table] VALUES (...)
                insert_sql = f"INSERT INTO [{table_name}] VALUES ({', '.join(escaped_row)});\n"
                f.write(insert_sql)
            f.write("\n")
    
    print(f"Successfully wrote sample_data.sql with {sum(len(v) for v in all_data.values())} rows")

def generate_ticket_note_table_ddl():
    """Output the CREATE TABLE statement for ticket_note with SQL Server syntax"""
    ddl = """--
-- Table structure for table ticket_note
--
IF OBJECT_ID('ticket_note', 'U') IS NOT NULL DROP TABLE ticket_note;
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
    return ddl

def main():
    """Main generation function"""
    print("Generating sample data for PineappleBites database...")
    
    # Generate companies first to get valid company IDs
    companies = generate_companies(50)
    company_ids = [c[0] for c in companies]
    
    # Generate data for each table (50 rows each)
    data = {
        'company': companies,
        'team': generate_teams(50),
        'resource': generate_resources(50),
        'contact': generate_contacts(50, company_ids),
        'configuration': generate_configurations(50),
        'agreement': generate_agreements(50, company_ids),
        'ticket': generate_tickets(50, company_ids),
    }
    
    # Generate ticket notes using the new ticket IDs
    notes = generate_ticket_notes(50, ID_START['ticket'])
    data['ticket_note'] = notes
    
    # Create SQL file
    write_sql_file(data)
    
    # Also print the ticket_note DDL separately
    print("\n" + generate_ticket_note_table_ddl())
    print("The DDL for ticket_note is shown above. It's already included in the schema.")

if __name__ == "__main__":
    main()