#!/bin/bash

echo "🔧 Setting up Python virtual environment..."

if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myenv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source ./myenv/bin/activate

echo "Installing required packages..."
pip install --upgrade pip
pip install pandas matplotlib seaborn

echo "Setup complete."
