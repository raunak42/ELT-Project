-- DropForeignKey
ALTER TABLE "BlankOrderIdTransaction" DROP CONSTRAINT "BlankOrderIdTransaction_uploadSessionId_fkey";

-- DropForeignKey
ALTER TABLE "BlankTransactionSummary" DROP CONSTRAINT "BlankTransactionSummary_uploadSessionId_fkey";

-- DropForeignKey
ALTER TABLE "CategorizedTransaction" DROP CONSTRAINT "CategorizedTransaction_uploadSessionId_fkey";

-- DropForeignKey
ALTER TABLE "TransactionSummary" DROP CONSTRAINT "TransactionSummary_uploadSessionId_fkey";

-- AddForeignKey
ALTER TABLE "BlankOrderIdTransaction" ADD CONSTRAINT "BlankOrderIdTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "BlankTransactionSummary" ADD CONSTRAINT "BlankTransactionSummary_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CategorizedTransaction" ADD CONSTRAINT "CategorizedTransaction_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TransactionSummary" ADD CONSTRAINT "TransactionSummary_uploadSessionId_fkey" FOREIGN KEY ("uploadSessionId") REFERENCES "UploadSession"("id") ON DELETE CASCADE ON UPDATE CASCADE;
