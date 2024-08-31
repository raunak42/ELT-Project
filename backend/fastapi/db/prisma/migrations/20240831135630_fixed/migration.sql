/*
  Warnings:

  - You are about to drop the column `Payment_Invoive_Amt` on the `CategorizedTransaction` table. All the data in the column will be lost.
  - You are about to drop the column `Return_Invoive_Amt` on the `CategorizedTransaction` table. All the data in the column will be lost.
  - You are about to drop the column `Shipment_Invoive_Amt` on the `CategorizedTransaction` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "CategorizedTransaction" DROP COLUMN "Payment_Invoive_Amt",
DROP COLUMN "Return_Invoive_Amt",
DROP COLUMN "Shipment_Invoive_Amt",
ADD COLUMN     "Payment_Invoice_Amt" TEXT,
ADD COLUMN     "Return_Invoice_Amt" TEXT,
ADD COLUMN     "Shipment_Invoice_Amt" TEXT;
