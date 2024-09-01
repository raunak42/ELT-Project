/*
  Warnings:

  - You are about to drop the `MergedTransaction` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "MergedTransaction" DROP CONSTRAINT "MergedTransaction_uploadSessionId_fkey";

-- DropTable
DROP TABLE "MergedTransaction";

-- CreateTable
CREATE TABLE "GroupedTransaction" (
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

    CONSTRAINT "GroupedTransaction_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "GroupedTransaction" ADD CONSTRAINT "GroupedTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;
