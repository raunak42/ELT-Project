from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from helpers import greet, process_and_merge_datasets, filter_and_summarize, group_and_categorize_by_order_id,create_markings
import logging
import os

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
    os.makedirs('processed_data', exist_ok=True)
    merged_df = await process_and_merge_datasets(mtrFile, prsFile)
    
    blank_transaction_df, blank_transaction_summary_df = filter_and_summarize(merged_df)
    grouped_df = group_and_categorize_by_order_id(merged_df)
    categorized_df,categorized_value_counts_df = create_markings(grouped_df)
    
    merged_df.to_excel(os.path.join('.','processed_data','Merged_Dataset.xlsx'),index=False)
    blank_transaction_df.to_excel(os.path.join('.','processed_data','Blank_Order_Id_Transactions.xlsx'), index=False)
    blank_transaction_summary_df.to_excel(os.path.join('.','processed_data','Blank_Transaction_Summary.xlsx'), index=False)
    categorized_df.to_excel(os.path.join('.','processed_data','Categorized_Transaction_Record.xlsx'), index=False)
    categorized_value_counts_df.to_excel(os.path.join('.','processed_data','Transaction_Summary.xlsx'), index=False)

    
    blank_transaction_records = blank_transaction_df.to_dict(orient='records')
    blank_transaction_summary_records = blank_transaction_summary_df.to_dict(orient='records')
    categorized_df_records = categorized_df.to_dict(orient='records')
    categorized_value_counts_df_records = categorized_value_counts_df.to_dict(orient='records')
    
    
    return {"message": "Files processed and saved successfully."}   