# Restricted Network Deployment Guide

**How to run PineappleBytes on school/work networks without consuming OpenRouter tokens**

---

## Quick Start

### Step 1: Prepare on an Unrestricted Network

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 2. Pre-cache all company data (consumes tokens ONCE)
python precache_all.py --start 26 --end 75
```

### Step 2: Deploy to Restricted Network

```bash
# 1. Ensure cache directory exists with company_XX.json files

# 2. Enable cache-only mode in .env:
CACHE_ONLY_MODE=true
OFFLINE_MODE=true

# 3. Start the server
python app.py
```

---

## Key Features

- **CACHE_ONLY_MODE**: Never makes API calls (zero token usage)
- **OFFLINE_MODE**: Falls back to cache when network fails
- **precache_all.py**: Pre-generate all summaries on unrestricted network

---

## Pre-Caching

```bash
# Cache all companies (default 26-75)
python precache_all.py

# Specific companies
python precache_all.py --company_ids 26,27,28

# Force re-cache
python precache_all.py --force

# List cached companies
python precache_all.py --list-only
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OFFLINE_MODE` | `true` | Fallback to cache on network failure |
| `CACHE_ONLY_MODE` | `false` | Never use live API (set to `true` for restricted networks) |

---

## Token Conservation

1. **Always use CACHE_ONLY_MODE=true** on restricted networks
2. Pre-cache only the companies you need
3. Monitor logs for "Sending request to OpenRouter API" (should see none in cache-only mode)

---

## Cache Management API

```bash
# Check cache status
curl http://localhost:5000/api/cache/status

# Preload cache via API
curl -X POST "http://localhost:5000/api/cache/preload?company_ids=26,27,28"

# Clear cache
curl -X POST "http://localhost:5000/api/cache/clear"
```

---

## Troubleshooting

- **"No cached data available"**: Run precache_all.py first on unrestricted network
- **High token usage**: Ensure CACHE_ONLY_MODE=true in .env
- **Database connection fails**: Use cache-only mode (no DB needed)

See `network-troubleshooting.md` for more details.
</parameter>
<task_progress>
- [x] Create precache_all.py script to pre-cache all company data
- [x] Add token usage tracking to middleware_engine.py
- [x] Enhance app.py to support token conservation mode
- [x] Add cache-only mode that skips OpenRouter API entirely
- [x] Update .env.example with new configuration options
- [x] Create deployment guide for restricted networks
- [x] Test the implementation
</parameter>
</write_to_file>