# PineappleBytes AI Database Middleware

**NSCC IT Database Administration — Capstone Project**  
**Lead Database Administrator:** Marrick MacKay

## System Overview

PineappleBytes is a robust, cloud-hosted data pipeline designed to integrate a relational SQL Server database with advanced AI business intelligence.

The system extracts complex client records from an AWS RDS instance, processes the relational data to prevent memory bloat, securely masks Personally Identifiable Information (PII) to maintain strict privacy/GRC compliance, and generates actionable AI summaries using the OpenRouter API.

---

## Tech Stack

- **Frontend:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS
- **Backend:** Python 3, Flask REST API
- **Database:** Microsoft SQL Server on AWS RDS
- **Cloud Infrastructure:** AWS RDS (SQL Server), AWS EC2 (Bastion Host)
- **AI Integration:** OpenRouter API (StepFun Model)
- **Data Masking:** Custom tokenization for PII compliance

---

## Prerequisites

Before installing and running this project, ensure you have the following:

1. **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
2. **Python 3.8+** - [Download](https://www.python.org/downloads/)
3. **OpenSSH Client** (for SSH tunnel) - Built-in on Linux/Mac, optional feature on Windows 10/11
4. **Microsoft ODBC Driver 17 for SQL Server** - [Download](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
5. **AWS Access**: `.pem` key file for the bastion host and RDS instance access
6. **Git** (optional) - [Download](https://git-scm.com/downloads)

---

## Project Structure

```
pineapplebytes_nscc_capstone_v2/
├── .env                    # Environment variables (create from .env.example)
├── .gitignore             # Git ignore file
├── README.md              # This file
├── start_tunnel.bat       # SSH tunnel script (Windows)
├── .env.example           # Environment template
├── app.py                 # Flask backend API
├── middleware_engine.py  # Core data processing & AI integration
├── cache_manager.py      # Cache management for offline mode
├── precache_all.py       # Pre-cache script for restricted networks
├── cache/                # Cached data (auto-generated)
├── sql_files/            # Database schema and sample data
├── pineapplebytes_nscc_capstone/  # Next.js frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── RestaurantHeader.tsx
│   │   │   ├── OverviewView.tsx
│   │   │   ├── SummaryView.tsx
│   │   │   └── RestaurantSelector.tsx
│   │   └── data/
│   │       └── restaurantData.ts
│   └── public/
└── docs/                 # Additional documentation (optional)
    ├── network-troubleshooting.md
    └── restricted-network-deployment.md
```

---

## Database Connection Guide (SSH Tunnel Method)

The production database is hosted on AWS RDS and is not directly accessible from the internet. You must connect through a bastion host (EC2 instance) using an SSH tunnel.

### Step 1: Update AWS Security Group

First, ensure your current public IP address is whitelisted in the RDS security group:

1. Go to AWS Console → RDS → Security Groups
2. Find the security group attached to the RDS instance
3. Add an inbound rule:
   - **Type:** MySQL/Aurora (or custom TCP)
   - **Port:** 1433
   - **Source:** Your current public IP (or 0.0.0.0/0 for testing only)
4. **Also add port 22** to the bastion host security group for SSH access

To find your public IP:
```bash
# Windows PowerShell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content

# Or visit: https://whatismyipaddress.com/
```

### Step 2: Start the SSH Tunnel

#### Windows (using start_tunnel.bat)

Simply double-click `start_tunnel.bat` in the project root, or run from command line:

```batch
start_tunnel.bat
```

Keep this terminal window open while using the application. The tunnel forwards:
- `localhost:1433` → `RDS_ENDPOINT:1433` via bastion host

#### Manual SSH Command (Linux/Mac/Windows WSL)

```bash
ssh -i "path/to/your-key.pem" -L 1433:RDS_ENDPOINT:1433 ec2-user@BASTION_IP
```

**Replace placeholders:**
- `path/to/your-key.pem` → Your `.pem` private key file
- `RDS_ENDPOINT` → From `.env.example` (e.g., `pineapplebytes-db.cyfqs2yieuln.us-east-1.rds.amazonaws.com`)
- `BASTION_IP` → From `.env.example` (e.g., `44.201.167.193`)

Expected output:
```
Welcome to Amazon Linux 2 ...
...
The connection is established and waiting for traffic.
```

### Step 3: Stop Local SQL Server (Windows Only)

If you have SQL Server service running locally, it will conflict with port 1433. Stop it:

```powershell
# Stop the default SQL Server instance
Stop-Service -Name "MSSQLSERVER"

# Or via Services.msc GUI
```

The SSH tunnel needs to bind to port 1433 locally.

### Step 4: Configure Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database Configuration (SSH Tunnel Mode)
DB_HOST=127.0.0.1
DB_PORT=1433
DB_USER=admin
DB_PASS=your_actual_password
DB_NAME=PineappleBytes

# OR use the direct format (as shown in .env.example):
# DB_SERVER=127.0.0.1,1433
# DB_DATABASE=PineappleBytes
# DB_USERNAME=admin
# DB_PASSWORD=your_actual_password

# OpenRouter API Key (Get from https://openrouter.ai/settings/integrations)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Set to true for restricted networks (school/work)
OFFLINE_MODE=true
CACHE_ONLY_MODE=false

# Infrastructure (for tunnel script - already in .env.example)
BASTION_IP=44.201.167.193
RDS_ENDPOINT=pb-dev-db.cyfqs2yieuln.us-east-1.rds.amazonaws.com
KEY_PATH=C:\Users\yourusername\.ssh\pb-dev-key.pem
```

---

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mackay-marrick/nscc-capstone-pineapplebytes.git
cd nscc-capstone-pineapplebytes
```

### 2. Install Backend Dependencies

```bash
pip install pyodbc python-dotenv flask flask-cors openai faker
```

**Note:** You may need to install the ODBC driver separately (see Prerequisites).

### 3. Install Frontend Dependencies

```bash
cd pineapplebytes_nscc_capstone
npm install
cd ..
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your actual database credentials and API keys
```

### 5. Start the Backend Server

```bash
python app.py
```

The Flask API will start on `http://127.0.0.1:5000`

Test health endpoint:
```bash
curl http://127.0.0.1:5000/health
# Expected: {"status":"healthy"}
```

### 6. Start the Frontend Development Server

Open a new terminal (keep the backend running):

```bash
cd pineapplebytes_nscc_capstone
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Using the Application

1. **Enter a Company ID** (default is 26) and click **Search**
2. The app fetches data from the database, processes it through the middleware, and displays:
   - **Client Overview**: Health metrics, tickets, recommendations
   - **Support Summary**: AI-generated executive summary
3. Use **Export** buttons to generate Word/PDF reports (placeholder in current version)
4. **Regenerate** to refresh AI analysis

---

## Working Offline or on Restricted Networks

School or corporate networks often block external APIs. To use PineappleBytes in these environments:

### Option A: Pre-Cache Mode (No Internet Required After Setup)

1. **On an unrestricted network** (home, mobile hotspot), run:
   ```bash
   python precache_all.py --start 26 --end 75
   ```
   This pre-generates all AI summaries and caches them locally.

2. **Transfer** the entire project (including `cache/` folder) to the restricted network.

3. **Enable cache-only mode** in `.env`:
   ```env
   OFFLINE_MODE=true
   CACHE_ONLY_MODE=true
   ```

4. **Start servers** - no database or OpenRouter API calls will be made.

### Option B: Offline Mode with Database

If you have a local SQL Server instance with a copy of the PineappleBytes database:

1. Restore the database locally
2. Update `.env` to point to localhost:
   ```env
   DB_HOST=localhost
   DB_PORT=1433
   DB_USER=sa
   DB_PASS=your_local_password
   ```
3. Set `OFFLINE_MODE=false` (OpenRouter API still required)

---

## Environment Variables Reference

See `.env.example` for all available configuration options.

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database host (localhost when using SSH tunnel) | `127.0.0.1` |
| `DB_PORT` | Database port | `1433` |
| `DB_USER` | Database username | `admin` |
| `DB_PASS` | Database password | `SecurePassword123` |
| `DB_NAME` | Database name | `PineappleBytes` |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI summaries | `sk-or-...` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OFFLINE_MODE` | `true` | Fallback to cached data when network fails |
| `CACHE_ONLY_MODE` | `false` | Skip all external API calls (use only cache) |
| `NEXT_PUBLIC_API_URL` | `http://127.0.0.1:5000` | Frontend API endpoint URL |
| `BASTION_IP` | (see .env.example) | EC2 bastion host IP (for tunnel script) |
| `RDS_ENDPOINT` | (see .env.example) | RDS instance endpoint (for tunnel script) |
| `KEY_PATH` | (see .env.example) | Path to `.pem` SSH key file |

---

## File Naming Standards

This project uses **kebab-case** for files and directories:

- ✅ `middleware-engine.py` (if it were Python module)
- ✅ `restaurant-data.ts`
- ✅ `cache-manager.js`
- ❌ `middlewareEngine.py` (camelCase - not used)
- ❌ `RestaurantData.ts` (PascalCase - not used)

**Note:** Existing Python modules may use snake_case (e.g., `cache_manager.py`) which is also acceptable for Python conventions.

---

## API Endpoints

### Frontend Facing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/company/{id}/summary` | Get AI summary and masked profile for a company |
| GET | `/api/cache/status` | List all cached companies |
| POST | `/api/cache/clear` | Clear all cached data |
| POST | `/api/cache/preload?company_ids=26,27` | Pre-cache specific companies |
| GET | `/health` | Health check |

### Response Format

```json
{
  "summary": "AI-generated executive summary text...",
  "profile": {
    "company": { "company_id": 26, "company_name": "..." },
    "contacts": [...],
    "agreements": [...],
    "tickets": [...]
  },
  "offline_mode": false  // Optional: true if served from cache
}
```

---

## Database Schema

The `sql_files/` directory contains the schema and sample data:

- `pineapplebites_company.sql` - Company table
- `pineapplebites_contact.sql` - Contact information
- `pineapplebites_agreement.sql` - Service agreements
- `pineapplebites_resource.sql` - Resource (staff) table
- `pineapplebites_team.sql` - Team structures
- `pineapplebites_ticket.sql` - Support tickets
- `pineapplebites_configuration.sql` - Hardware/software configurations

See `deploy_database.py` for automated deployment.

---

## Troubleshooting

### SSH Tunnel Issues

**Error: "Address already in use"**
```bash
# Port 1433 is already bound. Stop local SQL Server:
Stop-Service -Name "MSSQLSERVER"
# Or find and kill the process using port 1433:
netstat -ano | findstr :1433
taskkill /PID <pid> /F
```

**Error: "Permission denied (publickey)"**
- Verify the `.pem` file path in `KEY_PATH`
- Ensure the key file has correct permissions (read-only for owner)
- Check that the bastion host IP and username (`ec2-user`) are correct

**Error: "Could not resolve hostname"**
- Verify `BASTION_IP` and `RDS_ENDPOINT` in `.env`
- Test connectivity: `ping BASTION_IP`

### Database Connection Errors

- **404 Company Not Found**: Company IDs start at 26 (sample data). Try IDs 26-75.
- **Connection timeout**: Verify SSH tunnel is running and RDS security group allows your IP.
- **Login failed**: Verify `DB_USER` and `DB_PASS` in `.env`.

### API Errors

- **429 Rate Limit**: Free tier OpenRouter has limits. Add your own API key to `.env` or use cache-only mode.
- **Network errors**: On school/work networks, external APIs may be blocked. Use restricted network deployment guide.

See `network-troubleshooting.md` for more details.

---

## Deployment Notes

### Production Deployment (AWS EC2)

1. **Launch EC2 instance** (Ubuntu/Amazon Linux)
2. **Clone repository** and install dependencies
3. **Configure Nginx** as reverse proxy for Flask
4. **Use systemd** to manage Flask service
5. **Set up SSH keys** for RDS access
6. **Configure `.env`** with production values
7. **Build frontend**: `npm run build` in `pineapplebytes_nscc_capstone/`
8. **Serve frontend** via Nginx from `/var/www/pineapplebytes`

*Detailed deployment scripts are in `create_and_deploy.py` and `deploy_database.py`.*

---

## Contributing

This is a capstone project. For questions or issues, contact:

**Marrick MacKay**  
Lead Database Administrator  
NSCC IT Database Administration Capstone 2025

---

## License

[Specify license if applicable]

---

## Acknowledgments

- **NSCC Faculty**: Database Administration Program
- **OpenRouter**: AI API platform
- **AWS**: Cloud infrastructure (RDS, EC2)
- **Vercel**: Next.js hosting recommendation (not used in production)