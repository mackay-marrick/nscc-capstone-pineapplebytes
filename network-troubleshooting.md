# School Network Troubleshooting Guide

## Problem
You're seeing `HTTP error! status: 500` when using the application on your school network.

## Root Cause
The error occurs because school networks often block external connections to cloud services. This application requires access to:
1. **AWS RDS Database** (pineapplebytes-db.cyfqs2yieuln.us-east-1.rds.amazonaws.com:14333)
2. **OpenRouter API** (openrouter.ai)

If either of these is blocked, the backend returns a 500 error.

## Recent Improvements
I've enhanced the error handling to provide more specific messages:

### Database Connection Errors
- **404**: Company ID doesn't exist (e.g., using ID 1 when data starts at 26)
- **Connection/Network errors**: Clear message about network restrictions with suggestion to use a different network

### OpenRouter API Errors
- **429**: Rate limit exceeded (free tier) - suggests using your own API key
- **Network errors**: Clear message about blocked external APIs

## Solutions

### Option 1: Use a Different Network (Recommended)
Try connecting from:
- Your home network
- A mobile hotspot (from your phone)
- A coffee shop/library with open internet

### Option 2: Use a VPN
If your school allows VPNs, you can use one to bypass network restrictions.

### Option 3: Run Locally with Local Database (Advanced)
If you have a local SQL Server instance, you could:
1. Restore the database locally
2. Update `.env` file to point to localhost
3. This would only require OpenRouter API access (still needs to be unrestricted)

### Option 4: Add Your Own OpenRouter API Key
The free tier has rate limits. You can add your own key to `.env`:
```
OPENROUTER_API_KEY=your_key_here
```

Get a key from: https://openrouter.ai/settings/integrations

## Testing Connectivity

To diagnose which service is blocked, run these tests from your school network:

### Test 1: Check Database Connectivity
```powershell
python check_data.py
```
If this hangs or fails, the school network is blocking AWS RDS.

### Test 2: Check OpenRouter API
```powershell
python test_connection.py
```
If this fails, OpenRouter is blocked.

### Test 3: Check Flask API
```powershell
powershell -Command "Invoke-WebRequest -Uri http://127.0.0.1:5000/health"
```
This should always work (localhost).

## What the Error Messages Look Like

### Database Blocked
```
Error: Database connection failed
Cannot connect to the database. This may be due to network restrictions (e.g., school/work network blocking AWS RDS).
Suggestion: Try connecting from a different network (home network, mobile hotspot) or check with your network administrator.
```

### OpenRouter Blocked
```
Error: Network or connection error
Failed to connect to external service (database or AI API). This may be due to network restrictions.
Suggestion: Check your internet connection. If you are on a school/work network, it may block external APIs. Try a different network.
```

### Rate Limited
```
Error: Rate limit exceeded
OpenRouter API is currently rate-limited. Please try again in a few moments or use your own API key for higher limits.
Suggestion: This is a known issue with the free tier. Consider adding your own OpenRouter API key in the .env file.
```

## Next Steps
1. Try accessing the application from a non-school network
2. If it works from home but not at school, confirm the school network is the issue
3. Consider using a VPN or requesting network admin to whitelist the required services
4. Add your own OpenRouter API key to avoid rate limiting

## Files Modified for Better Error Handling
- `app.py` - Enhanced exception handling with specific error messages
- `middleware_engine.py` - Added 30-second timeout to database connection, 60-second timeout to OpenRouter API
- `pineapplebytes_nscc_capstone/src/app/page.tsx` - Frontend displays detailed error messages with suggestions