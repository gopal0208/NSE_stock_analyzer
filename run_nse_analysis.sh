#!/bin/bash

echo "Activating virtual environment..."
source ./myenv/bin/activate

echo "Running processNSE.py..."
python3 processNSE.py

echo "Running plotIt.py..."
python3 plotIt.py

echo "Analysis complete."
