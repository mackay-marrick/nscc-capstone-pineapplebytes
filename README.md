# PineappleBytes AI Database Middleware

**NSCC IT Database Administration — Capstone Project** **Lead Database Administrator:** Marrick MacKay  

## System Overview
PineappleBytes is a robust, cloud-hosted data pipeline designed to integrate a relational SQL Server database with advanced AI business intelligence. 

The system extracts complex client records from an AWS RDS instance, processes the relational data to prevent memory bloat, securely masks Personally Identifiable Information (PII) to maintain strict privacy/GRC compliance, and generates actionable AI summaries using the OpenRouter API.

### Architecture Stack
* **Cloud Infrastructure:** AWS RDS (Microsoft SQL Server)
* **Backend Logic:** Python 3
* **Database Driver:** `pyodbc` (ODBC Driver 17 for SQL Server)
* **AI Integration:** OpenRouter API (StepFun Model)

---

## Prerequisites & Local Setup

To run this pipeline locally, ensure you have the following installed:
1. **Python 3.8+**
2. **Microsoft ODBC Driver 17 for SQL Server**
3. **Required Python Packages:** `pip install pyodbc python-dotenv requests`

### Environment Variables (`.env`)
Create a `.env` file in the root directory. This project utilizes a custom port routing strategy to bypass standard ISP firewalls for development. Ensure your configuration matches the following template exactly:

```env
# AWS RDS Connection (Note the custom 14333 port)
DB_SERVER=pineapplebytes-db.[redacted].us-east-1.rds.amazonaws.com,14333
DB_DATABASE=PineappleBytes
DB_USERNAME=admin
DB_PASSWORD=your_secure_password

# AI Integration
OPENROUTER_API_KEY=your_openrouter_api_key