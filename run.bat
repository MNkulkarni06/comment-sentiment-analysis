@echo off
REM Comment Sentiment Analysis - Run Script for Windows
REM This script sets up and runs the Flask application

echo ================================================
echo Comment Sentiment Analysis System
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if all required files exist
echo Checking project files...
set "all_files_exist=true"

if not exist "app.py" (
    echo Error: Required file missing - app.py
    set "all_files_exist=false"
)

if not exist "modules\text_preprocessor.py" (
    echo Error: Required file missing - modules\text_preprocessor.py
    set "all_files_exist=false"
)

if not exist "modules\sentiment_analyzer.py" (
    echo Error: Required file missing - modules\sentiment_analyzer.py
    set "all_files_exist=false"
)

if not exist "modules\wordcloud_generator.py" (
    echo Error: Required file missing - modules\wordcloud_generator.py
    set "all_files_exist=false"
)

if not exist "modules\data_loader.py" (
    echo Error: Required file missing - modules\data_loader.py
    set "all_files_exist=false"
)

if not exist "static\datasets\comments.csv" (
    echo Error: Required file missing - static\datasets\comments.csv
    set "all_files_exist=false"
)

if not exist "static\datasets\positive_words.txt" (
    echo Error: Required file missing - static\datasets\positive_words.txt
    set "all_files_exist=false"
)

if not exist "static\datasets\negative_words.txt" (
    echo Error: Required file missing - static\datasets\negative_words.txt
    set "all_files_exist=false"
)

if "%all_files_exist%"=="false" (
    echo.
    echo Error: Some required files are missing
    pause
    exit /b 1
)

echo All required files present
echo.

REM Run the Flask application
echo ================================================
echo Starting Flask application...
echo ================================================
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
