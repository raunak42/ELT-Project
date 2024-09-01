#!/bin/bash
set -e  

export PATH=$PATH:/home/ubuntu/.nvm/versions/node/v20.5.1/bin

echo "Deploying backend..."
cd backend
source .venv/bin/activate
cd fastapi
pip install -r requirements.txt
pip cache purge
pm2 delete fastapi-server || true
pm2 start main.py --name fastapi-server --interpreter python3

echo "Deploying frontend..."
cd ../../nextjs-frontend
npm install
npm run build
pm2 delete nextjs-frontend || true
pm2 start npm --name nextjs-frontend -- start

echo "Deployment completed."
