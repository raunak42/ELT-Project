-- CreateTable
CREATE TABLE "BlankOrderIdTransaction" (
    "id" SERIAL NOT NULL,
    "Order_Id" TEXT,
    "Transaction_Type" TEXT,
    "Payment_Type" TEXT,
    "Invoice_Amt" DOUBLE PRECISION,
    "Net_Amt" DOUBLE PRECISION,
    "P_Description" TEXT,
    "Order_Date" TEXT,
    "Payment_Date" TEXT,
    "Source" TEXT,
    "uploadSessionId" INTEGER,

    CONSTRAINT "BlankOrderIdTransaction_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "BlankTransactionSummary" (
    "id" SERIAL NOT NULL,
    "P_Description" TEXT NOT NULL,
    "SumNetAmt" DOUBLE PRECISION NOT NULL,
    "uploadSessionId" INTEGER,

    CONSTRAINT "BlankTransactionSummary_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CategorizedTransaction" (
    "id" SERIAL NOT NULL,
    "Order_Id" TEXT,
    "Payment_Invoive_Amt" DOUBLE PRECISION,
    "Return_Invoive_Amt" DOUBLE PRECISION,
    "Shipment_Invoive_Amt" DOUBLE PRECISION,
    "Payment_Net_Amt" DOUBLE PRECISION,
    "Return_Net_Amt" DOUBLE PRECISION,
    "Shipment_Net_Amt" DOUBLE PRECISION,
    "Category" TEXT NOT NULL,
    "uploadSessionId" INTEGER,

    CONSTRAINT "CategorizedTransaction_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TransactionSummary" (
    "id" SERIAL NOT NULL,
    "Category" TEXT NOT NULL,
    "Count" INTEGER NOT NULL,
    "uploadSessionId" INTEGER,

    CONSTRAINT "TransactionSummary_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "UploadSession" (
    "id" SERIAL NOT NULL,

    CONSTRAINT "UploadSession_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "BlankOrderIdTransaction" ADD CONSTRAINT "BlankOrderIdTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "BlankTransactionSummary" ADD CONSTRAINT "BlankTransactionSummary_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CategorizedTransaction" ADD CONSTRAINT "CategorizedTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TransactionSummary" ADD CONSTRAINT "TransactionSummary_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE SET NULL ON UPDATE CASCADE;
