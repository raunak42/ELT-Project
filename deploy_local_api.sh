#!/bin/bash
set -e  

export PATH=$PATH:/home/ubuntu/.nvm/versions/node/v20.5.1/bin

echo "Deploying backend..."
cd backend
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing python dependencies..."
cd fastapi
pip install -r requirements.txt
pip cache purge
cd db
python3 -m prisma generate
cd ..
fastapi run main.py

