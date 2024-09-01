from fastapi import UploadFile
import pandas as pd
import tempfile
import os
import logging

logger = logging.getLogger(__name__) 

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

async def process_and_merge_datasets(mtrFile: UploadFile, prsFile: UploadFile):
    try:
        mtr_file_type = mtrFile.filename.split('.')[-1].lower()
        prs_file_type = prsFile.filename.split('.')[-1].lower()
    
        if mtr_file_type not in ['xlsx', 'csv'] or prs_file_type not in ['xlsx', 'csv']:
            logger.error ("Invalid file type. Only .xlsx and .csv files are allowed.")
            return
        
        df_mtr = await read_file(mtrFile)
        df_prs = await read_file(prsFile)
    
        if df_mtr is None or df_prs is None:
            logger.error ("Failed to read one or both files.")
            return
    
        df_processed_prs = process_prs(df_prs)    
        df_processed_mtr = process_mtr(df_mtr)
        
        if df_processed_prs is None:
            logger.error("Failed to process payment report.")
            return
        if df_processed_mtr is None:
            logger.error("Failed to process MTR.")
            return
        merged_df = merge_datasets(df_processed_mtr, df_processed_prs)
        return merged_df
    except Exception as e:
        logger.error(f"Error - {str(e)}")
        return

async def read_file(file: UploadFile):
    logger.info(f"Reading file: {file.filename}")
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
    try:
        logger.info("Payment Report: Processing ...")
        df = df.copy()
        
        if 'type' in df.columns:
            df['type'] = df['type'].str.replace(r'\s+', '', regex=True)
            df = df[df['type'] != 'Transfer']
        elif 'Type' in df.columns:
            df['Type'] = df['Type'].str.replace(r'\s+', '', regex=True)
            df = df[df['Type'] != 'Transfer']
        
        logger.info("Payment Report: Renaming columns ...")    
        df = df.rename(columns={'type': 'Payment Type', 'order id': 'Order Id', 'date/time': 'Payment Date', 'description': 'P_Description', 'total': 'Net Amount'})
        
        logger.info("Payment Report: Replacing values in 'Payment Type' column ... ")
        value_map = {
            'Adjustment': 'Order',
            'FBAInventoryFee': 'Order',
            'FulfilmentFeeRefund': 'Order',
            'ServiceFee': 'Order',
            'Refund': 'Return'
        }
        df['Payment Type'] = df['Payment Type'].replace(value_map)
        df['Transaction Type'] = 'Payment'
        
        logger.info("Payment Report: Converting Net Amount values to float...")
        df['Net Amount'] = df['Net Amount'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
        df['Source'] = 'Payment Sheet'
        logger.info("Payment Report: Processing completed.")
        return df    
    
    except Exception as e:
        logger.error(f"Payment Report: Error occured while processing - {str(e)}")
        return

def process_mtr(df):
    try:
        logger.info("MTR: Processing ...")
        df = df.copy()
        logger.info("MTR: Removing cancelled transactions ...")
        df = df[df['Transaction Type'] != 'Cancel']
        logger.info("MTR: Replacing values in 'Transaction Type' row ... ")
        df['Transaction Type'] = df['Transaction Type'].replace({'Refund': 'Return', 'FreeReplacement': 'Return'})
        df = df[['Order Id', 'Transaction Type', 'Invoice Amount', 'Order Date']]
        df['Source'] = 'MTR Sheet'
        logger.info("MTR: Processing completed.")
        return df
    except Exception as e:
        logger.error(f"MTR: Error occured while processing - {str(e)}")
        return

def merge_datasets(df_processed_mtr, df_processed_prs):
    try:
        logger.info("Merging Payment Report and MTR.")
        merged_df = pd.concat([df_processed_mtr, df_processed_prs], sort=False)
        column_order = ['Order Id', 'Transaction Type', 'Payment Type', 'Invoice Amount', 'Net Amount', 'P_Description', 'Order Date', 'Payment Date', 'Source']
        merged_df = merged_df.reindex(columns=column_order)
        logger.info("Payment Report and MTR merged successfully.")
        return merged_df
    except Exception as e:
        logger.error(f"MTR: Error occured while merging datasets - {str(e)}")
        return

def filter_and_summarize(merged_df):
    try:
        logger.info("Filtering out rows with blank Order Ids in Merged Dataset to create a df.")
        blank_transaction_df = merged_df[merged_df['Order Id'].isna() | (merged_df['Order Id'] == '')]
        blank_transaction_summary_df = blank_transaction_df.groupby('P_Description')['Net Amount'].sum().reset_index()
        blank_transaction_summary_df = blank_transaction_summary_df.rename(columns={'Net Amount': 'SUM of Net Amount'})
        logger.info("Created Blank Transaction Summary:\n")
        logger.info(blank_transaction_summary_df)
        return blank_transaction_df, blank_transaction_summary_df
    except Exception as e:
        logger.error(f"MTR: Error occured while filtering and summarizing the Merged Dataset - {str(e)}")
        return

def group_and_categorize_by_order_id(merged_df):
    try:
        grouped = merged_df.groupby(['Order Id', 'Transaction Type']).agg({
            'Invoice Amount': 'sum',
            'Net Amount': 'sum'
        }).reset_index()
        
        pivoted = grouped.pivot(index='Order Id', 
                                columns='Transaction Type', 
                                values=['Invoice Amount', 'Net Amount'])
        pivoted.columns = [f'{col[1]}_{col[0]}' for col in pivoted.columns]
        pivoted = pivoted.reset_index()
        logger.info("Grouped the Merged Dataset by Order Id.")
        return pivoted
    except Exception as e:
        logger.error(f"MTR: Error occured while categorizing the Merged Dataset by Order Id - {str(e)}")
        return

def create_markings(grouped):
    try:
        logger.info("Categorizing the Grouped Dataset.")
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
        
        logger.info("Grouped Dataset successfully categorized, now creating transaction summary.")    
        transaction_summary = grouped['Category'].value_counts().reset_index()
        transaction_summary.columns = ['Category','Count']
        
        total_row = pd.DataFrame({'Category': ['TOTAL'], 'Count': [transaction_summary['Count'].sum()]})
        transaction_summary = pd.concat([transaction_summary, total_row], ignore_index=True)  
        logger.info(transaction_summary)
        return grouped,transaction_summary
    except Exception as e:
        logger.error(f"An error occurred while categorizing the grouped data - {str(e)}")
        return