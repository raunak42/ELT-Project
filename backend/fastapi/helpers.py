from fastapi import UploadFile
import pandas as pd
import tempfile
import os
import logging
import json

logger = logging.getLogger(__name__) 

logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO or DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log")  # Log to file 'app.log'
    ]
)
def greet():
    return "HELLO SUCKER"

async def process_and_merge_datasets(mtrFile: UploadFile, prsFile: UploadFile):
    mtr_file_type = mtrFile.filename.split('.')[-1].lower()
    prs_file_type = prsFile.filename.split('.')[-1].lower()

    if mtr_file_type not in ['xlsx', 'csv'] or prs_file_type not in ['xlsx', 'csv']:
        return {"error": "Invalid file type. Only .xlsx and .csv files are allowed."}

    df_mtr = await read_file(mtrFile)
    df_prs = await read_file(prsFile)

    if df_mtr is None or df_prs is None:
        return {"error": "Failed to process one or both files."}

    df_processed_prs = process_prs(df_prs)    
    df_processed_mtr = process_mtr(df_mtr)
    
    merged_df = merge_datasets(df_processed_mtr, df_processed_prs)
    

    
    return merged_df

async def read_file(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(temp_file_path)
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(temp_file_path)
        else:
            return None
    finally:
        os.remove(temp_file_path)

    return df

def process_prs(df):
    df = df.copy()
    df = df[df['type'] != 'Transfer\n']
    df = df.rename(columns={'type': 'Payment Type', 'order id': 'Order Id', 'date/time': 'Payment Date', 'description': 'P_Description', 'total': 'Net Amount'})
    
    value_map = {
        'Order\n': 'Order',
        'Adjustment\n': 'Order',
        'FBA Inventory Fee\n': 'Order',
        'Fulfilment Fee Refund': 'Order',
        'Service Fee\n': 'Order',
        'Refund\n': 'Return'
    }
    df['Payment Type'] = df['Payment Type'].replace(value_map)
    df['Transaction Type'] = 'Payment'
    df['Net Amount'] = df['Net Amount'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
    df['Source'] = 'Payment Sheet'
    return df    

def process_mtr(df):
    df = df.copy()
    df = df[df['Transaction Type'] != 'Cancel']
    df['Transaction Type'] = df['Transaction Type'].replace({'Refund': 'Return', 'FreeReplacement': 'Return'})
    df = df[['Order Id', 'Transaction Type', 'Invoice Amount', 'Order Date']]
    df['Source'] = 'MTR Sheet'
    return df

def merge_datasets(df_processed_mtr, df_processed_prs):
    merged_df = pd.concat([df_processed_mtr, df_processed_prs], sort=False)
    column_order = ['Order Id', 'Transaction Type', 'Payment Type', 'Invoice Amount', 'Net Amount', 'P_Description', 'Order Date', 'Payment Date', 'Source']
    merged_df = merged_df.reindex(columns=column_order)
    return merged_df

def filter_and_summarize(merged_df):
    blank_transaction_df = merged_df[merged_df['Order Id'].isna() | (merged_df['Order Id'] == '')]


    blank_transaction_summary_df = blank_transaction_df.groupby('P_Description')['Net Amount'].sum().reset_index()
    blank_transaction_summary_df = blank_transaction_summary_df.rename(columns={'Net Amount': 'SUM of Net Amount'})
    return blank_transaction_df, blank_transaction_summary_df

def group_and_categorize_by_order_id(merged_df):
    # Group by Order Id and Transaction Type
    grouped = merged_df.groupby(['Order Id', 'Transaction Type']).agg({
        'Invoice Amount': 'sum',
        'Net Amount': 'sum'
    }).reset_index()
    
    # Pivot the table to get Transaction Types as columns
    pivoted = grouped.pivot(index='Order Id', 
                            columns='Transaction Type', 
                            values=['Invoice Amount', 'Net Amount'])
    # Flatten column names
    pivoted.columns = [f'{col[1]}_{col[0]}' for col in pivoted.columns]
    # Reset index to make Order Id a column again
    pivoted = pivoted.reset_index()
    
    return pivoted

def create_markings(grouped):
    # Apply categorization rules
    logger.info(grouped.head())
    grouped['Category'] = ''
    
    # Removal Order IDs
    grouped.loc[grouped['Order Id'].astype(str).str.len() == 10, 'Category'] = 'Removal Order IDs'
    
    # Return
    grouped.loc[(grouped['Return_Invoice Amount'].notna()) , 'Category'] = 'Return'
    
    # Negative Payout
    grouped.loc[(grouped['Payment_Net Amount'] < 0), 'Category'] = 'Negative Payout'
    
    # Order & Payment Received
    grouped.loc[(grouped['Order Id'].notna()) & 
                (grouped['Payment_Net Amount'].notna()) & 
                (grouped['Shipment_Invoice Amount'].notna()), 'Category'] = 'Order & Payment Received'
    
    # Order Not Applicable but Payment Received
    grouped.loc[(grouped['Order Id'].notna()) & 
                (grouped['Payment_Net Amount'].notna()) & 
                (grouped['Shipment_Invoice Amount'].isna()), 'Category'] = 'Order Not Applicable but Payment Received'
    
    # Payment Pending
    grouped.loc[(grouped['Order Id'].notna()) & 
                (grouped['Shipment_Invoice Amount'].notna()) & 
                (grouped['Payment_Net Amount'].isna()), 'Category'] = 'Payment Pending'
    
    
    value_counts = grouped['Category'].value_counts()
    print(value_counts)
    
    grouped_value_counts_df = value_counts.reset_index()
    grouped_value_counts_df.columns = ['Category','Count']
    
    total_row = pd.DataFrame({'Category': ['TOTAL'], 'Count': [grouped_value_counts_df['Count'].sum()]})
    grouped_value_counts_df = pd.concat([grouped_value_counts_df, total_row], ignore_index=True)  
    

    return grouped,grouped_value_counts_df