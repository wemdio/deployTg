#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Starting application..."
uvicorn api:app --host 0.0.0.0 --port 8000

