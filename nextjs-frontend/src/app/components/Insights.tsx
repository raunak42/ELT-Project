"use client";

import { useState } from "react";

interface InsightsProps {
  uploadSessionId: number;
}

interface InsightsResType {
  removal_transactions: any[];
  return_transactions: any[];
  negative_transactions: any[];
  opr_transactions: any[];
  ona_transactions: any[];
  pending_transactions: any[];
  blank_summaries: any[];
  transaction_summaries: any[];
}

export const Insights: React.FC<InsightsProps> = ({ uploadSessionId }) => {
  const [data, setData] = useState<InsightsResType>();
  const handleClick = async () => {
    try {
      const res = await fetch("http://localhost:8000/get_processed_data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-store",
        body: JSON.stringify({ id: uploadSessionId }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data: InsightsResType = await res.json();
      setData(data);
      console.log(data.blank_summaries);
      console.log(data.transaction_summaries);
      // Process your data here
    } catch (error) {
      console.error("An error occurred while fetching data:", error);
      // Handle the error appropriately
    }
  };

  return (
    <div>
      <button
        disabled={!uploadSessionId}
        onClick={handleClick}
        className={`bg-black text-white font-semibold rounded-lg w-[200px] h-[40px] disabled:cursor-not-allowed disabled:bg-zinc-400`}
      >
        Get insights
      </button>
      {data && (
        <ul>
          <h1>Order & Payment Received:{data?.opr_transactions.length}</h1>
          <h1>Payment Pending:{data?.pending_transactions.length}</h1>
          <h1>Return:{data?.return_transactions.length}</h1>
          <h1>Negative Payout:{data?.negative_transactions.length}</h1>
          <h1>
            Order Not Applicable but Payment Received:
            {data?.ona_transactions.length}
          </h1>

          <h1>Blank Summaries:{data?.blank_summaries.length}</h1>
          <h1>Transaction Summaries:{data?.transaction_summaries.length}</h1>
        </ul>
      )}
    </div>
  );
};
