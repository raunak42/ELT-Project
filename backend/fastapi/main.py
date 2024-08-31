from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional
from helpers import greet, process_and_merge_datasets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return 'Health check complete for'

class User(BaseModel):
    user_name: str

@app.post('/hello')
def hello(user: User):
    greeting = greet()
    return {"message": f"Request received from user {user.user_name} {greeting}"}

@app.post("/upload")
async def upload_files(
    mtrFile: UploadFile = File(...),
    prsFile: UploadFile = File(...)
):
   await process_and_merge_datasets(mtrFile, prsFile)

   return {"message": "Files processed and saved successfully."}
