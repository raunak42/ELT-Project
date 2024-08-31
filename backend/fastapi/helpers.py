from fastapi import FastAPI, File, UploadFile
from typing import Optional
import pandas as pd
import tempfile
import os


def greet():
    return "HELLO SUCKER"

async def process_and_merge_datasets(
    mtrFile: UploadFile = File(...),
    prsFile: UploadFile = File(...)
):
     # Initialize dataframes
    df_mtr: Optional[pd.DataFrame] = None
    df_prs: Optional[pd.DataFrame] = None

    mtr_file_type = mtrFile.filename.split('.')[-1].lower()
    prs_file_type = prsFile.filename.split('.')[-1].lower()

    if mtr_file_type not in ['xlsx', 'csv'] or prs_file_type not in ['xlsx', 'csv']:
        return {"error": "Invalid file type. Only .xlsx and .csv files are allowed."}

    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False) as temp_mtr_file:
        temp_mtr_file.write(await mtrFile.read())
        temp_mtr_file_path = temp_mtr_file.name

    with tempfile.NamedTemporaryFile(delete=False) as temp_prs_file:
        temp_prs_file.write(await prsFile.read())
        temp_prs_file_path = temp_prs_file.name

    if mtr_file_type == 'xlsx':
        df_mtr = pd.read_excel(temp_mtr_file_path)
    elif mtr_file_type == 'csv':
        df_mtr = pd.read_csv(temp_mtr_file_path)

    if prs_file_type == 'xlsx':
        df_prs = pd.read_excel(temp_prs_file_path)
    elif prs_file_type == 'csv':
        df_prs = pd.read_csv(temp_prs_file_path)

    # Check if dataframes are created
    if df_mtr is None:
        return {"error": "Failed to process mtrFile."}
    if df_prs is None:
        return {"error": "Failed to process prsFile."}

    # # Create directory if it doesn't exist
    # os.makedirs(os.path.join('.', 'sex'), exist_ok=True)

    # # Save the processed DataFrames as Excel files
    # output_mtr_path = os.path.join('.', 'sex', 'mtr1.xlsx')
    # df_mtr.to_excel(output_mtr_path, index=False)
    
    # output_prs_path = os.path.join('.', 'sex', 'prs1.xlsx')
    # df_prs.to_excel(output_prs_path, index=False)
    
    
    

    # Remove temporary files
    os.remove(temp_mtr_file_path)
    os.remove(temp_prs_file_path)
    
    return True
    