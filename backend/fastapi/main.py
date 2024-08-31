from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from helpers import greet, process_and_merge_datasets, filter_and_summarize, group_and_categorize_by_order_id,create_markings
import logging

logger = logging.getLogger(__name__) 

logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO or DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log")  # Log to file 'app.log'
    ]
)
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
    return 'Health check complete'

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
    merged_df = await process_and_merge_datasets(mtrFile, prsFile)
    summary = filter_and_summarize(merged_df)
    grouped = group_and_categorize_by_order_id(merged_df)
    categorized = create_markings(grouped)
    
    
    return {"message": "Files processed and saved successfully."}   