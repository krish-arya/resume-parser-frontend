import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { Analytics } from "@vercel/analytics/react" // ✅ Add this line
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "ResumeParser - Professional Resume Analysis",
  description:
    "Enterprise-grade AI-powered resume parsing and portfolio generation. Transform PDF resumes into structured, professional portfolios.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <Analytics /> 
      </body>
    </html>
  )
}

//