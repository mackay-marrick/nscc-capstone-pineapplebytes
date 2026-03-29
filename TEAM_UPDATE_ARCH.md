# PineappleBytes Capstone V2 - System Architecture & Onboarding Guide

*Technical Lead Documentation | Version 1.0 | March 2026*

---

## 1. System Architecture Overview

### 1.1 Monorepo Structure

The PineappleBytes Capstone V2 project is organized as a **monorepo** with a clear separation between backend and frontend services:

```
pineapplebytes_nscc_capstone_v2/
├── app.py                  ← Python/Flask backend (root)
├── middleware_engine.py
├── start_tunnel.bat        ← SSH tunnel script
├── cache_manager.py
├── .env                    ← Environment configuration
├── public/                 ← Static assets for backend
├── sql_files/              ← Database schemas
└── pineapplebytes_nscc_capstone/  ← Next.js frontend (ISOLATED)
    ├── app/
    ├── components/
    ├── lib/
    ├── package.json
    ├── next.config.ts
    └── ...
```

**Key Principle**: The frontend is **strictly isolated** inside the `pineapplebytes_nscc_capstone` subdirectory. All backend services operate from the root directory. This separation prevents dependency conflicts and maintains clear service boundaries.

### 1.2 Backend Architecture (Python/Flask)

The backend runs on **Port 5000** and serves as a middleware layer with the following responsibilities:

- **API Gateway**: Receives requests from the Next.js frontend
- **AI Integration**: Forwards sanitized data to OpenRouter API for processing
- **Database Proxy**: Manages connections to AWS RDS via SSH tunnel
- **PII Sanitization**: Processes sensitive data before external transmission
- **Caching Layer**: Implements Redis-based caching via `cache_manager.py`

**Core Files**:
- `app.py` - Main Flask application entry point
- `middleware_engine.py` - Business logic and request handling
- `cache_manager.py` - Redis caching utilities
- `test_connection.py` - Database connectivity verification
- `test_middleware.py` - Middleware function tests

### 1.3 Frontend Architecture (Next.js/React)

The frontend runs on **Port 3000** and is built with modern React/Next.js patterns:

- **App Router**: Next.js 14+ with `app/` directory structure
- **TypeScript**: Full type safety across components
- **Tailwind CSS**: Utility-first styling approach
- **Server Components**: Strategic use of RSC for performance

**Key Directories**:
- `app/` - Route handlers and page components (App Router)
- `components/` - Reusable UI components
- `lib/` - Utility functions and API clients
- `public/` - Static assets and images

### 1.4 Database Layer

**Database**: AWS RDS (PostgreSQL/MySQL based on schema files)

**Connection Strategy**: SSH Tunnel Bypass  
To circumvent restricted school network firewalls, the application uses an SSH tunnel established via `start_tunnel.bat`:

```batch
# start_tunnel.bat
ssh -L 3306:your-rds-endpoint.rds.amazonaws.com:3306 ec2-user@your-bastion-host
```

This creates a local port forward (`localhost:3306`) that the Flask backend connects to, while the tunnel securely routes traffic through an EC2 bastion host to the RDS instance.

**Schema Files** (`sql_files/`):
- `pineapplebites_agreement.sql`
- `pineapplebites_company.sql`
- `pineapplebites_configuration.sql`
- `pineapplebites_contact.sql`
- `pineapplebites_resource.sql`
- `pineapplebites_team.sql`
- `pineapplebites_ticket.sql`

### 1.5 AI Integration

**Provider**: OpenRouter API

**Data Flow**:
1. Frontend collects user input
2. Backend sanitizes PII (Personally Identifiable Information)
3. Sanitized data sent to OpenRouter for processing
4. Results returned to backend and forwarded to frontend

**Security Note**: All PII sanitization occurs server-side before any external API calls to ensure compliance with data privacy regulations.

---

## 2. The Startup Sequence (How to Run the App)

**Critical Requirement**: Two separate terminal sessions are required—one for the backend, one for the frontend.

### 2.1 Terminal 1: Backend Setup

```bash
# Navigate to project root (if not already there)
cd c:\Users\marym\Desktop\projects\pineapplebytes_nscc_capstone_v2

# Create and activate virtual environment (first-time setup only)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install backend dependencies
pip install -r requirements.txt  # If exists, or install manually:

# Key packages typically needed:
# flask, pandas, paramiko, redis, python-dotenv, openai, sqlalchemy

# Set up environment variables
# Create a .env file in the root directory (see section 2.3)

# Start the SSH tunnel (REQUIRED for database access)
# In a separate terminal or in background, run:
start_tunnel.bat

# Launch the Flask backend
python app.py
```

**Expected Output**:
```
[INFO] Starting Flask server...
[INFO] Database connection established
[INFO] SSH tunnel active on localhost:3306
[INFO] Server running on http://0.0.0.0:5000
```

### 2.2 Terminal 2: Frontend Setup

```bash
# Navigate to the isolated frontend directory
cd c:\Users\marym\Desktop\projects\pineapplebytes_nscc_capstone_v2\pineapplebytes_nscc_capstone

# Install frontend dependencies (first-time setup only)
npm install

# Start the Next.js development server
npm run dev
```

**Expected Output**:
```
 ✓ Starting...
 ✓ Ready in 123ms
 ┌────────────────────────────────────────────────────────────┐
 │                                                            │
 │   Server running at                                        │
 │   ➜ Local:        http://localhost:3000                   │
 │   ➜ Network:      http://192.168.x.x:3000                │
 │                                                            │
 │   Waiting for the debugger to disconnect...              │
 │                                                            │
 └────────────────────────────────────────────────────────────┘
```

### 2.3 Environment Variable Configuration (.env)

The `.env` file must reside in the **project root** (backend directory).

**Format Rules**:
- ❌ **NO spaces** around the `=` sign
- ✅ **Use quotes** for values containing special characters or spaces
- ✅ Keep the file out of version control (already in `.gitignore`)

**Template**:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pineapplebites
DB_USER=your_username
DB_PASSWORD=your_password

# AI Integration
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
OPENROUTER_MODEL=anthropic/claude-3-haiku

# Application Settings
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=1

# Cache Configuration
REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=300

# SSH Tunnel Settings
SSH_BASTION_HOST=ec2-user@your-bastion-host.amazonaws.com
SSH_RDS_ENDPOINT=your-rds-endpoint.rds.amazonaws.com
SSH_KEY_PATH=C:\path\to\your\private_key.pem
```

**Important**: After modifying `.env`, restart both backend and frontend servers to apply changes.

---

## 3. Known Traps & Resolutions (The Troubleshooting Log)

### 3.1 The Git Submodule Trap

**Symptom**: The `pineapplebytes_nscc_capstone/` directory exists but appears empty (0 bytes) or only contains a `.git` file.

**Root Cause**: The frontend directory is configured as a Git submodule. When cloning the repository without the `--recurse-submodules` flag, the submodule directory is created but its contents are not automatically fetched.

**Incorrect Fix**: ❌ Do **NOT** manually move files from `src_backup/` to the root or try to "fix" by copying files around. This breaks the submodule structure and causes commit inconsistencies.

**Correct Fix**:

```bash
# From the project root, initialize and update all submodules:
git submodule update --init --recursive

# If the frontend directory is already present but empty, first remove it:
rmdir /s pineapplebytes_nscc_capstone  # Windows
# OR
rm -rf pineapplebytes_nscc_capstone     # Mac/Linux

# Then pull the submodule contents:
git submodule update --init --recursive
```

**History Context**: The frontend was extracted from commit `a6a0013` (the source of truth). The submodule points to that specific commit, ensuring version stability across the monorepo.

### 3.2 The BOM Parsing Error

**Symptom**: Next.js fails to start with an error similar to:

```
Error: Invalid JSON: expected value at line 1 column 1 of the JSON data.
```

**Root Cause**: The `package.json` file (or any `.json` config file) has been saved with **UTF-8 with BOM (Byte Order Mark)** encoding. The invisible BOM characters (`ï»¿`) at the start of the file break JSON parsing.

**Detection**: Open `pineapplebytes_nscc_capstone/package.json` in VS Code and check the encoding indicator in the status bar (bottom right). If it says `UTF-8 with BOM` or `UTF-8 with signature`, this is the problem.

**Correct Fix**:

1. **Save the file with pure UTF-8 encoding**:
   - In VS Code: Click the encoding indicator → Select "Save with Encoding" → Choose `UTF-8`
   - Or: `File` → `Save with Encoding` → `UTF-8`

2. **Delete the Next.js cache** to prevent cached errors:
   ```bash
   cd pineapplebytes_nscc_capstone
   rmdir /s .next  # Windows
   # OR
   rm -rf .next   # Mac/Linux
   ```

3. **Restart the frontend**:
   ```bash
   npm run dev
   ```

**Prevention**: Configure your editor to default to UTF-8 (without BOM). VS Code default is already correct; issues arise when files are edited in other editors (Notepad++, some IDEs) that default to BOM.

---

## 4. Additional Technical Notes

### 4.1 Port Management

| Service   | Port | Protocol | Access URL              |
|-----------|------|----------|-------------------------|
| Backend   | 5000 | HTTP     | http://localhost:5000   |
| Frontend  | 3000 | HTTP     | http://localhost:3000   |
| Database  | 3306 | MySQL    | localhost:3306 (tunnel) |
| Redis     | 6379 | TCP      | localhost:6379 (if used) |

**Port Conflicts**: If either 3000 or 5000 is already in use, change the port in the respective config files:
- Backend: Modify `app.py` → `app.run(port=YOUR_PORT)`
- Frontend: Set `PORT=3001` in `.env.local` (Next.js) or run `PORT=3001 npm run dev`

### 4.2 CORS Configuration

The Flask backend includes CORS headers to allow requests from the Next.js frontend. If you encounter CORS errors in the browser console:

```python
# In app.py or middleware_engine.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
```

### 4.3 Database Schema Management

SQL schema files are located in:
- Root: `sql_files/`
- Frontend: `pineapplebytes_nscc_capstone/sql_files/`

**To apply schema changes**:

```bash
# Using the provided deployment script
python deploy_database.py

# OR manually via MySQL client
mysql -h localhost -P 3306 -u username -p pineapplebites < sql_files/your_schema.sql
```

### 4.4 SSH Tunnel Management

The `start_tunnel.bat` script establishes the required tunnel to AWS RDS.

**To keep the tunnel running in the background** (Windows):

```batch
# Start in a separate minimized terminal window, OR:
start /B cmd /c "start_tunnel.bat"
```

**To verify the tunnel is active**:

```bash
# Test connectivity to the forwarded port
telnet localhost 3306
# OR
python test_connection.py
```

**To terminate the tunnel**: Close the terminal window or press `Ctrl+C` in the tunnel session.

---

## 5. Final Verification Checklist

Before presenting the project or deploying to production:

- [ ] SSH tunnel is working (`test_connection.py` returns success)
- [ ] Backend starts on port 5000 without errors
- [ ] Frontend builds successfully (`npm run build` works)
- [ ] Frontend proxies API requests to backend correctly
- [ ] Database queries execute and return expected results
- [ ] OpenRouter API integration returns valid responses
- [ ] PII sanitization is verified in logs/middleware
- [ ] CORS headers are correctly configured
- [ ] All `.env` variables are set (no missing keys)
- [ ] Git submodule is properly initialized (`git submodule status` shows no changes)
- [ ] No BOM encoding issues in JSON files
- [ ] `.next` cache is clean after configuration changes

---

## 6. Common Commands Reference

```bash
# Backend operations
python app.py                          # Start server
python test_connection.py             # Test DB connection
python deploy_database.py             # Apply schema

# Frontend operations
npm run dev                           # Development server
npm run build                         # Production build
npm run lint                          # Lint codebase
npm run preview                       # Preview production build

# Git submodule management
git submodule update --init --recursive   # Pull submodules
git submodule status                       # Check status
git submodule sync                         # Sync URLs

# Cache management
# Delete .next in frontend folder
# Delete cache/ in backend folder if needed
```

---

## 7. Support & Resources

**Internal Documentation**:
- `restricted-network-deployment.md` - Detailed deployment guide for restricted networks
- `network-troubleshooting.md` - Network-specific issue resolution
- `README.md` - Project overview and quick start

**Architecture Decision Records**: See commit history for major structural changes (submodule extraction, SSH tunnel implementation, etc.).

---

*Document maintained by the Technical Lead. Last updated: March 2026.*  
*For questions or clarifications, refer to the team Slack channel or GitHub Issues.*