# [Interface](https://interface.raunak42.in)

## Run Locally:

1. cd backend/fastapi
2. cp .env.example .env
3. populate the .env file with your postgres database url
4. run `bash run_api_dev.sh`
5. on a separate terminal, run `bash run_frontend_dev.sh`

Now fastapi server is running on port 8000 and nextjs server on port 3000.
Look into the above mentioned files for more detials.

## Potential Improvements:

1. Handling error messages on the frontend can be impoved.
2. Docker image has not been created yet.
3. Logs are stored in plain text in `backend/fastapi/app.log`, they can be stored in json.
4. Frontend can be made prettier.
5. Page for displaying rows of individual order-details for categories has not been created yet. The api and data fetching logic is ready to handle this frontend requirement.
6. Responsiveness not suitable enough for handheld devices yet.

## Database Schema

The schema has 6 models - 

### For creating a session.
1. UploadSession - This is to create a new session every time files are uploaded. This is done to create a unique identity for data each time someone uploads files.
   
### For processed data
Here, our output dataframes have been converted into python dictionaries to prepare them to be uploaded in the postgres database. The schema is made keeping this in mind.

1. BlankOrderIdTransaction - This is to model all the orders with blank order ids.
   
2. BlankTransactionSummary - This is to model the data of a Blank Transaction Summary.
   
3. CategorizedTransaction - This is important, it has been modeled according to the data of categorized order transactions, the categories being - 
  a. Cost of Advertising
  b. FBA Inbound Pickup Service
  c. FBA Inventory Reimbursement - Customer Return
  d. FBA Inventory Reimbursement - Customer Service Issue
  e. FBA Inventory Reimbursement - Damaged:Warehouse
  f. FBA Inventory Reimbursement - Fee Correction
  g. FBA Inventory Reimbursement - Lost:Inbound
  h. FBA Inventory Storage Fee

4. TransactionSummary - This is to model the summary created from the categorized transactions.
5. GroupedTransaction - When the merged dataset is grouped by order ids and further categorized, we get the dataframe resembling this model. The categories being - 
  a. Removal Order IDs
  b. Return
  c. Negative Payout
  d. Order & Payment Received
  e. Order Not Applicable but Payment Received
  f. Payment Pending


## ELT Pipeline

1. We first start with mtr and prs files. Both of them can be either of the two types - .xlsx or .csv.
   
2. The function `process_and_merge_datasets()` reads the files and invokes the functions `process_prs()` and `process_mtr()` respectively to retur processed and cleaned files.
   
   `process_prs()`: 
   1. Renames columns to prepare the df for merging with mtr.
   2. Replaces some values in 'Payment Type' column.
   3. Converts the values in 'Net Amount' to float, because many of them are strings.
   
   `process_mtr()`:
   4. Removes unnecessary values and renames some values in 'Transaction Type' row.
   5. Specifies which columns to return.
   
3. These clean files are then merged (concatenated) to prepare a merged dataset using `merge_datasets()`. 
4. The merged dataset is then filtered, a new dataset is created that has 'Order Id' rows blank. The function `filter_and_summarize()` is used for this. Thereafter it also created a summary of these orders with blank Order Ids. The summary adheres to the databse model `BlankTransactionSummary`.
5. Other datasets is created from the merged dataset. These are the 'grouped' and 'pivoted' datasets. The former adheres to out db model `GroupedTransaction` and the latter is moved into further processing which will be needed to create 'CategorizedTransactions'.
6. The 'pivoted' dataframe is then processed by the `create_markings()` function which adds a new column called 'Category' and assigns one of the following values based on the certain conditions - 
  a. Removal Order IDs
  b. Return
  c. Negative Payout
  d. Order & Payment Received
  e. Order Not Applicable but Payment Received
  f. Payment Pending
This reuturns the categorized transactions and the summary created with these transactions. These adhere to the models `CategorizedTransaction` and `TransactionSummary`, respectively.

7. In the file `main.py`, the above functions are called to return the necessary dataframes. The dataframes that have schema models related to them are then converted to python dictionaries and sent into the postgres database by making prisma calls.

