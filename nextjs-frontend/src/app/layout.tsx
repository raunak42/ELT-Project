import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Interface",
  description: "Interface data crunching",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="w-full h-[100px] border-b flex items-center justify-center fixed top-0 bg-white shadow-sm">
          <h1 className="text-base font-semibold">Dashboard</h1>
        </div>
        <div className="h-full w-[70px] border-r fixed left-0 bg-white"></div>
        <div className="mt-[100px]" > {children}</div>
      </body>
    </html>
  );
}
