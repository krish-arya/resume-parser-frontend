"use client"

import type React from "react"

import { useRef, useState } from "react"

interface UploadFormProps {
  onFileUpload: (file: File) => void
  isUploading: boolean
}

export default function UploadForm({ onFileUpload, isUploading }: UploadFormProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const file = fileInputRef.current?.files?.[0]
    if (file && file.type === "application/pdf") {
      onFileUpload(file)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const file = e.dataTransfer.files?.[0]
    if (file && file.type === "application/pdf") {
      if (fileInputRef.current) {
        const dt = new DataTransfer()
        dt.items.add(file)
        fileInputRef.current.files = dt.files
      }
      onFileUpload(file)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-5 relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 bg-gradient-to-br from-[#aabdff] to-[#c9b6ff]" />

      {/* Floating Background Elements */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute w-[350px] h-[350px] bg-[#ffa3ac] rounded-full opacity-12 blur-[70px] top-[15%] left-[10%] animate-float-1" />
        <div className="absolute w-[500px] h-[500px] bg-[#9a6fff] rounded-full opacity-12 blur-[70px] top-[75%] right-[8%] animate-float-2" />
      </div>

      {/* Bouncing Balls */}
      <div className="fixed inset-0 pointer-events-none overflow-visible">
        <div className="absolute w-[110px] h-[110px] bg-[#FF4E50] rounded-full opacity-40 shadow-lg top-[8%] left-[12%] animate-bounce-1" />
        <div className="absolute w-[80px] h-[80px] bg-[#FC913A] rounded-full opacity-40 shadow-lg top-[72%] left-[28%] animate-bounce-2" />
        <div className="absolute w-[130px] h-[130px] bg-[#FFFA65] rounded-full opacity-40 shadow-lg top-[38%] left-[78%] animate-bounce-3" />
        <div className="absolute w-[90px] h-[90px] bg-[#24FFBD] rounded-full opacity-40 shadow-lg top-[82%] left-[62%] animate-bounce-4" />
        <div className="absolute w-[100px] h-[100px] bg-[#4A90E2] rounded-full opacity-40 shadow-lg top-[55%] left-[15%] animate-bounce-5" />
        <div className="absolute w-[120px] h-[120px] bg-[#9B59B6] rounded-full opacity-40 shadow-lg top-[20%] left-[55%] animate-bounce-6" />
        <div className="absolute w-[85px] h-[85px] bg-[#F39C12] rounded-full opacity-40 shadow-lg top-[68%] left-[85%] animate-bounce-7" />
        <div className="absolute w-[95px] h-[95px] bg-[#2ECC71] rounded-full opacity-40 shadow-lg top-[12%] left-[80%] animate-bounce-8" />
      </div>

      {/* Upload Form */}
      <div className="relative z-10">
        <h1 className="text-4xl font-bold text-gray-700 text-center mb-8 tracking-wide">Upload a PDF</h1>

        <form
          onSubmit={handleSubmit}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`
            bg-white p-12 rounded-3xl w-full max-w-md mx-auto
            shadow-[0_4px_8px_rgba(0,0,0,0.1),0_12px_24px_rgba(0,0,0,0.1)]
            transition-all duration-300 ease-out
            hover:shadow-[0_12px_20px_rgba(0,0,0,0.15),0_40px_60px_rgba(0,0,0,0.15)]
            hover:transform hover:translateZ-10 hover:-translate-y-2
            ${dragActive ? "scale-105 shadow-2xl" : ""}
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf"
            className={`
              w-full p-4 border-2 rounded-xl text-lg cursor-pointer
              transition-all duration-300 bg-gray-50
              shadow-inner
              focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500
              hover:border-purple-500 hover:bg-white hover:shadow-lg
              ${dragActive ? "border-purple-500 bg-purple-50" : "border-gray-300"}
            `}
            disabled={isUploading}
          />

          <button
            type="submit"
            disabled={isUploading}
            className={`
              w-full mt-5 py-4 px-8 text-white font-bold text-lg rounded-2xl
              bg-gradient-to-r from-pink-400 to-pink-300
              shadow-[0_6px_15px_rgba(255,106,136,0.5)]
              transition-all duration-300
              hover:from-pink-300 hover:to-pink-400
              hover:shadow-[0_8px_20px_rgba(255,153,172,0.7)]
              hover:-translate-y-1
              focus:outline-none focus:ring-2 focus:ring-pink-500
              disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
              ${isUploading ? "animate-pulse" : ""}
            `}
          >
            {isUploading ? "Processing..." : "Upload"}
          </button>
        </form>
      </div>
    </div>
  )
}
