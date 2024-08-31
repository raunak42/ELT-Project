-- AlterTable
ALTER TABLE "BlankOrderIdTransaction" ALTER COLUMN "Invoice_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Net_Amt" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "BlankTransactionSummary" ALTER COLUMN "SumNetAmt" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "CategorizedTransaction" ALTER COLUMN "Payment_Invoive_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Return_Invoive_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Shipment_Invoive_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Payment_Net_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Return_Net_Amt" SET DATA TYPE TEXT,
ALTER COLUMN "Shipment_Net_Amt" SET DATA TYPE TEXT;
