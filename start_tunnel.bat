@echo off
REM SSH Tunnel Startup Script for Windows
REM
REM This script establishes an SSH tunnel from localhost:1433 to the RDS instance
REM via the bastion host. This allows database connections to use localhost:1433
REM while the tunnel forwards traffic to the actual RDS endpoint.
REM
REM Prerequisites:
REM - OpenSSH Client must be installed on Windows
REM   (Windows 10/11 has it built-in, can be enabled in Settings > Apps > Optional Features)
REM - Private key file must exist at the path specified in .env
REM
REM Usage:
REM   1. Open a command prompt or PowerShell
REM   2. Run this script
REM   3. Keep the terminal open while you need the tunnel
REM   4. Press Ctrl+C to close the tunnel

echo ============================================================================
echo PineappleBytes SSH Tunnel
echo ============================================================================
echo.
echo This script will create an SSH tunnel from localhost:1433 to the RDS database.
echo The tunnel will forward traffic through the bastion host.
echo.
echo Press Ctrl+C to stop the tunnel.
echo ============================================================================
echo.

REM Get the current directory (where this script is located)
set CURRENT_DIR=%~dp0

REM Load environment variables from .env file in current directory
if exist "%CURRENT_DIR%.env" (
    echo Loading environment from .env...
    for /f "tokens=*" %%a in ('type "%CURRENT_DIR%.env" ^| findstr "^[^#]"') do (
        set "%%a"
    )
) else (
    echo WARNING: .env file not found in current directory.
    echo Please ensure .env exists with the required variables.
    echo.
)

REM Check if required variables are set
if "%BASTION_IP%"=="" (
    echo ERROR: BASTION_IP not set in .env file
    pause
    exit /b 1
)

if "%RDS_ENDPOINT%"=="" (
    echo ERROR: RDS_ENDPOINT not set in .env file
    pause
    exit /b 1
)

if "%KEY_PATH%"=="" (
    echo ERROR: KEY_PATH not set in .env file
    echo Please set KEY_PATH to the path of your SSH private key file
    pause
    exit /b 1
)

REM Check if key file exists
if not exist "%KEY_PATH%" (
    echo ERROR: SSH key file not found at: %KEY_PATH%
    echo Please verify the key path in your .env file
    pause
    exit /b 1
)

REM Default values if not set in .env
set SSH_USER=ec2-user
if not "%DB_PORT%"=="" (
    set LOCAL_PORT=%DB_PORT%
) else (
    set LOCAL_PORT=1433
)

echo Configuration:
echo   Bastion Host: %BASTION_IP%
echo   RDS Endpoint: %RDS_ENDPOINT%
echo   Local Port:   %LOCAL_PORT%
echo   SSH User:     %SSH_USER%
echo   Key File:     %KEY_PATH%
echo.

echo Establishing SSH tunnel...
echo Command: ssh -i "%KEY_PATH%" -L %LOCAL_PORT%:%RDS_ENDPOINT%:1433 %SSH_USER%@%BASTION_IP%
echo.

REM Start the SSH tunnel
ssh -i "%KEY_PATH%" -L %LOCAL_PORT%:%RDS_ENDPOINT%:1433 %SSH_USER%@%BASTION_IP%

if errorlevel 1 (
    echo.
    echo SSH tunnel failed to start or disconnected.
    echo Check the error message above for details.
    pause
    exit /b 1
)