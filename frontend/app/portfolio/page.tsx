"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import PortfolioDisplay from "@/components/portfolio-display"

interface ResumeData {
  name: string
  skills: string[]
  education: Array<{
    Institute_name: string
    Degree_name: string
    Marks: string
  }>
  projects: Array<{
    title: string
    desc: string
    tech: string[]
  }>
  Experience: Array<{
    Company: string
    Position: string
    Skills: string[]
  }>
  Achievements: Array<{
    achievement_name: string
    institute_name: string
    description: string
  }>
  Position_of_responsibility: Array<{
    position_name: string
    soc_name: string
    description: string
  }>
  Contact_Info: Record<string, string>
}

export default function PortfolioPage() {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const data = localStorage.getItem("resumeData")
    if (data) {
      setResumeData(JSON.parse(data))
    } else {
      router.push("/")
    }
    setIsLoading(false)
  }, [router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading portfolio...</p>
        </div>
      </div>
    )
  }

  if (!resumeData) {
    return null
  }

  return <PortfolioDisplay data={resumeData} />
}
