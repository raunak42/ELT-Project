"use client";

import { BASE_URL } from "@/lib/constants";
import Image from "next/image";
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
  grouped_transactions: any[];
}

export const Insights: React.FC<InsightsProps> = ({ uploadSessionId }) => {
  const [data, setData] = useState<InsightsResType>();
  const [showSpinner, setShowSpinner] = useState<boolean>(false);

  const handleClick = async () => {
    setShowSpinner(true)
    try {
      const res = await fetch(`${BASE_URL}/get_processed_data`, {
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
      setShowSpinner(false)
      setData(data);
      console.log(data);
    } catch (error) {
      console.error("An error occurred while fetching data:", error);
    }
  };

  const labels = [
    { label: "Order & Payment Received", value: data?.opr_transactions.length },
    { label: "Payment Pending", value: data?.pending_transactions.length },
    { label: "Return", value: data?.return_transactions.length },
    { label: "Negative Payout", value: data?.negative_transactions.length },
    {
      label: "Order Not Applicable but Payment Received",
      value: data?.ona_transactions.length,
    },
  ];

  return (
    <div className="w-full  flex flex-col items-center  justify-center ">
      <button
        disabled={!uploadSessionId}
        onClick={handleClick}
        className={`bg-black text-white font-semibold rounded-lg w-[200px] h-[40px] disabled:cursor-not-allowed disabled:bg-zinc-400 flex items-center justify-center`}
      >
        {!showSpinner ? (
            <h1>Get insights</h1>
          ) : (
            <Image
              alt=""
              width={24}
              height={24}
              src={"/spinner.svg"}
              className="animate-spin"
            />
          )}
      </button>
      {data && (
        <div className="w-full flex items-center justify-center ">
          <div className=" flex flex-col items-start justify-center  w-[90%]">
            <div className="flex flex-row items-center justify-start p-[24px] flex-wrap ">
              {labels.map((item, index) => {
                return <Card item={item} key={index} />;
              })}
            </div>

            <div className="w-[680px] h-fit border ml-[48px] rounded-lg p-[32px] flex flex-col gap-[24px]">
              <h1 className="font-semibold text-xl">
                Reimbursements by Dispute Type - Alltime
              </h1>
              <div className="flex flex-col gap-[4px]" >
                {data.blank_summaries.map((item, index) => {
                  return (
                    <div
                      key={index}
                      className="flex flex-row items-center justify-between"
                    >
                      <h1 className="">{item.P_Description}</h1>
                      <h1 className="font-light" >{item.SumNetAmt}</h1>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
      {
        !data&&<h1 className="mt-[48px] text-3xl" >Your insights will appear here.</h1>
      }
    </div>
  );
};

interface CardProps {
  item: {
    label: string;
    value: number | undefined | null;
  };
}

const Card: React.FC<CardProps> = ({ item }) => {
  return (
    <div className="flex items-center justify-between px-[12px] py-[18px] w-[360px] h-[100px] border rounded-lg m-[24px]">
      <div className="flex flex-col h-full justify-between ">
        <h1 className="text-sm font-semibold">{item.label}</h1>
        <h1 className="text-2xl font-semibold">{item.value}</h1>
      </div>
      <Image alt="" width={24} height={24} src={"/arrow.svg"} />
    </div>
  );
};
