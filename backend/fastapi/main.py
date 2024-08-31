from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from helpers import greet, process_and_merge_datasets, filter_and_summarize, group_and_categorize_by_order_id, create_markings
import logging
import os
from prisma import Prisma
from typing import Any
import pandas as pd

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
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

def safe_str(value: Any) -> str:
    """Convert value to string, or return None if value is NaN or None."""
    if pd.isna(value) or value is None:
        return None
    return str(value)

@app.post("/upload")
async def upload_files(
    mtrFile: UploadFile = File(...),
    prsFile: UploadFile = File(...)
):
    prisma = Prisma()
    await prisma.connect()

    try:
        os.makedirs('processed_data', exist_ok=True)
        merged_df = await process_and_merge_datasets(mtrFile, prsFile)
        
        blank_transaction_df, blank_transaction_summary_df = filter_and_summarize(merged_df)
        grouped_df = group_and_categorize_by_order_id(merged_df)
        categorized_df, categorized_value_counts_df = create_markings(grouped_df)
        
        # To view these dataframes in excel format.
        # merged_df.to_excel(os.path.join('.','processed_data','Merged_Dataset.xlsx'),index=False)
        # blank_transaction_df.to_excel(os.path.join('.','processed_data','Blank_Order_Id_Transactions.xlsx'), index=False)
        # blank_transaction_summary_df.to_excel(os.path.join('.','processed_data','Blank_Transaction_Summary.xlsx'), index=False)
        # categorized_df.to_excel(os.path.join('.','processed_data','Categorized_Transaction_Record.xlsx'), index=False)
        # categorized_value_counts_df.to_excel(os.path.join('.','processed_data','Transaction_Summary.xlsx'), index=False)
        
        upload_session = await prisma.uploadsession.create({})
        
        # Prepare data for bulk insert
        blank_transaction_data = [
            {
                "Order_Id": safe_str(record.get("Order Id")),
                "Transaction_Type": safe_str(record.get("Transaction Type")),
                "Payment_Type": safe_str(record.get("Payment Type")),
                "Invoice_Amt": safe_str(record.get("Invoice Amount")),
                "Net_Amt": safe_str(record.get("Net Amount")),
                "P_Description": safe_str(record.get("P_Description")),
                "Order_Date": safe_str(record.get("Order Date")),
                "Payment_Date": safe_str(record.get("Payment Date")),
                "Source": safe_str(record.get("Source")),
                "uploadSessionId": upload_session.id
            }
            for record in blank_transaction_df.to_dict(orient='records')
        ]

        blank_summary_data = [
            {
                "P_Description": safe_str(record.get("P_Description")),
                "SumNetAmt": safe_str(record.get("SUM of Net Amount")),
                "uploadSessionId": upload_session.id
            }
            for record in blank_transaction_summary_df.to_dict(orient='records')
        ]

        categorized_data = [
            {
                "Order_Id": safe_str(record.get("Order Id")),
                "Payment_Invoice_Amt": safe_str(record.get("Payment_Invoice Amount")),
                "Return_Invoice_Amt": safe_str(record.get("Return_Invoice Amount")),
                "Shipment_Invoice_Amt": safe_str(record.get("Shipment_Invoice Amount")),
                "Payment_Net_Amt": safe_str(record.get("Payment_Net Amount")),
                "Return_Net_Amt": safe_str(record.get("Return_Net Amount")),
                "Shipment_Net_Amt": safe_str(record.get("Shipment_Net Amount")),
                "Category": safe_str(record.get("Category")),
                "uploadSessionId": upload_session.id
            }
            for record in categorized_df.to_dict(orient='records')
        ]

        summary_data = [
            {
                "Category": safe_str(record.get("Category")),
                "Count": int(record.get("Count", 0)),
                "uploadSessionId": upload_session.id
            }
            for record in categorized_value_counts_df.to_dict(orient='records')
        ]

        # Perform bulk inserts
        await prisma.blankorderidtransaction.create_many(data=blank_transaction_data)
        await prisma.blanktransactionsummary.create_many(data=blank_summary_data)
        await prisma.categorizedtransaction.create_many(data=categorized_data)
        await prisma.transactionsummary.create_many(data=summary_data)
        
        return {"message": "Files processed and saved successfully.", "uploadSessionId": upload_session.id}
    
    except Exception as e:
        logger.error(f"Error occurred while saving data: {str(e)}")
        return {"error": "An error occurred while processing and saving the data."}
    
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)