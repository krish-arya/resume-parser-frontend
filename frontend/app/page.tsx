"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { FileText, Zap, Shield, Users, Palette, Download, Eye } from "lucide-react"
import UploadSection from "@/components/upload-section"
import StyleSelector from "@/components/style-selector"
import WebsitePreview from "@/components/website-preview"
import Header from "@/components/header"
import Footer from "@/components/footer"

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

export default function HomePage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState<"upload" | "style" | "preview">("upload")
  const [isUploading, setIsUploading] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [resumeData, setResumeData] = useState<ResumeData | null>(null)
  const [selectedStyle, setSelectedStyle] = useState<"professional" | "futuristic" | "playful">("professional")
  const [websiteId, setWebsiteId] = useState<string | null>(null)

  const handleFileUpload = async (file: File) => {
    setIsUploading(true)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Upload failed")
      }

      const result = await response.json()
      setResumeData(result.data)
      setCurrentStep("style")
    } catch (error) {
      console.error("Upload failed:", error)
      alert("Upload failed: " + (error instanceof Error ? error.message : "Unknown error"))
    } finally {
      setIsUploading(false)
    }
  }

  const handleStyleSelect = (style: "professional" | "futuristic" | "playful") => {
    setSelectedStyle(style)
  }

  const handleGenerateWebsite = async () => {
    if (!resumeData) return

    setIsGenerating(true)

    try {
      const response = await fetch("/api/generate-website", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: resumeData,
          style: selectedStyle,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Generation failed")
      }

      const result = await response.json()
      setWebsiteId(result.website_id)
      setCurrentStep("preview")
    } catch (error) {
      console.error("Generation failed:", error)
      alert("Generation failed: " + (error instanceof Error ? error.message : "Unknown error"))
    } finally {
      setIsGenerating(false)
    }
  }

  const handleDownload = async () => {
    if (!websiteId) return

    try {
      const response = await fetch(`/api/download/${websiteId}`)
      if (!response.ok) throw new Error("Download failed")

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "portfolio_website.zip"
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error("Download failed:", error)
      alert("Download failed: " + (error instanceof Error ? error.message : "Unknown error"))
    }
  }

  const handleStartOver = () => {
    setCurrentStep("upload")
    setResumeData(null)
    setWebsiteId(null)
    setSelectedStyle("professional")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      {/* Progress Indicator */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-full ${
                currentStep === "upload"
                  ? "bg-blue-600 text-white"
                  : currentStep === "style" || currentStep === "preview"
                    ? "bg-green-600 text-white"
                    : "bg-gray-300"
              }`}
            >
              <FileText className="w-5 h-5" />
            </div>
            <div
              className={`h-1 w-16 ${currentStep === "style" || currentStep === "preview" ? "bg-green-600" : "bg-gray-300"}`}
            />
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-full ${
                currentStep === "style"
                  ? "bg-blue-600 text-white"
                  : currentStep === "preview"
                    ? "bg-green-600 text-white"
                    : "bg-gray-300"
              }`}
            >
              <Palette className="w-5 h-5" />
            </div>
            <div className={`h-1 w-16 ${currentStep === "preview" ? "bg-green-600" : "bg-gray-300"}`} />
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-full ${
                currentStep === "preview" ? "bg-blue-600 text-white" : "bg-gray-300"
              }`}
            >
              <Eye className="w-5 h-5" />
            </div>
          </div>
        </div>

        {/* Step Content */}
        {currentStep === "upload" && (
          <div>
            {/* Hero Section */}
            <section className="text-center mb-12">
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                AI-Powered Portfolio
                <span className="text-blue-600 block">Website Generator</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Upload your resume and get a complete, customizable portfolio website with AI-powered editing
                capabilities.
              </p>
              <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-500">
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4" />
                  Secure & Private
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4" />
                  AI-Powered
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  Multiple Styles
                </div>
              </div>
            </section>

            <UploadSection onFileUpload={handleFileUpload} isUploading={isUploading} />
          </div>
        )}

        {currentStep === "style" && resumeData && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Choose Your Style</h2>
              <p className="text-lg text-gray-600">Select a design theme for your portfolio website</p>
            </div>

            <StyleSelector selectedStyle={selectedStyle} onStyleSelect={handleStyleSelect} resumeData={resumeData} />

            <div className="text-center mt-8">
              <button
                onClick={handleGenerateWebsite}
                disabled={isGenerating}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating Website...
                  </div>
                ) : (
                  "Generate Website"
                )}
              </button>
            </div>
          </div>
        )}

        {currentStep === "preview" && websiteId && (
          <div>
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Your Portfolio Website</h2>
              <p className="text-lg text-gray-600">Click on any component to edit it with AI assistance</p>
            </div>

            <WebsitePreview websiteId={websiteId} />

            <div className="flex justify-center gap-4 mt-8">
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700"
              >
                <Download className="w-5 h-5" />
                Download Website
              </button>
              <button
                onClick={handleStartOver}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700"
              >
                Create Another
              </button>
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  )
}
