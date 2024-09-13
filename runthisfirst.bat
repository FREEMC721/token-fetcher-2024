@echo off
echo Running Python script to install dependencies...

:: Run the Python script
python runthisfirst.py

:: Check if the script was successful
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b %errorlevel%
)

echo Dependencies installed successfully.
pause
