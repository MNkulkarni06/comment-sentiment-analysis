#!/bin/bash

# Comment Sentiment Analysis - Run Script
# This script sets up and runs the Flask application

echo "================================================"
echo "Comment Sentiment Analysis System"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if all required files exist
echo "Checking project files..."
required_files=(
    "app.py"
    "modules/text_preprocessor.py"
    "modules/sentiment_analyzer.py"
    "modules/wordcloud_generator.py"
    "modules/data_loader.py"
    "static/datasets/comments.csv"
    "static/datasets/positive_words.txt"
    "static/datasets/negative_words.txt"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file missing - $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "Error: Some required files are missing"
    exit 1
fi

echo "All required files present"
echo ""

# Run the Flask application
echo "================================================"
echo "Starting Flask application..."
echo "================================================"
echo ""
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
