#!/bin/bash
set -e  

export PATH=$PATH:/home/ubuntu/.nvm/versions/node/v20.5.1/bin

echo "Deploying frontend..."
cd  nextjs-frontend
npm install
npm run dev

