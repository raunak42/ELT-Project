-- CreateTable
CREATE TABLE "MergedTransaction" (
    "id" SERIAL NOT NULL,
    "Order_Id" TEXT,
    "Transaction_Type" TEXT,
    "Payment_Type" TEXT,
    "Invoice_Amt" TEXT,
    "Net_Amt" TEXT,
    "P_Description" TEXT,
    "Order_Date" TEXT,
    "Payment_Date" TEXT,
    "Source" TEXT,
    "uploadSessionId" INTEGER,

    CONSTRAINT "MergedTransaction_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "MergedTransaction" ADD CONSTRAINT "MergedTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;
