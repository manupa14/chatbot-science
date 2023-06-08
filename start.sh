#!/bin/bash

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python and try again."
    exit 1
fi

# Run the chatbot script
python main.py