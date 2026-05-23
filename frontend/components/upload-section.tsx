"use client"

import type React from "react"
import { useRef, useState } from "react"
import { Upload, FileText, CheckCircle, Loader2, AlertCircle } from "lucide-react"

interface UploadSectionProps {
  onFileUpload: (file: File) => void
  isUploading: boolean
}

export default function UploadSection({ onFileUpload, isUploading }: UploadSectionProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

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
      setSelectedFile(file)
      setError(null)
      if (fileInputRef.current) {
        const dt = new DataTransfer()
        dt.items.add(file)
        fileInputRef.current.files = dt.files
      }
    } else {
      setError("Please drop a PDF file")
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setError(null)
      if (file.type !== "application/pdf") {
        setError("Please select a PDF file")
        return
      }
      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB")
        return
      }
      setSelectedFile(file)
    }
  }

  const handleUpload = async () => {
    if (selectedFile) {
      setError(null)
      try {
        await onFileUpload(selectedFile)
      } catch (err) {
        console.error("Upload error:", err)
        setError("Failed to process resume. Please check your connection and try again.")
      }
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Your Resume</h2>
        <p className="text-gray-600">Upload a PDF file to get started with AI-powered resume parsing</p>
      </div>

      {/* Upload Area */}
      <div
        className={`
          relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200
          ${
            dragActive
              ? "border-blue-400 bg-blue-50"
              : selectedFile
                ? "border-green-400 bg-green-50"
                : "border-gray-300 hover:border-gray-400"
          }
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={isUploading}
        />

        <div className="space-y-4">
          {selectedFile ? (
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
          ) : (
            <Upload className="w-16 h-16 text-gray-400 mx-auto" />
          )}

          {selectedFile ? (
            <div>
              <h3 className="text-lg font-semibold text-green-700">File Selected</h3>
              <div className="mt-2 p-4 bg-white rounded-lg border border-green-200">
                <div className="flex items-center justify-center gap-3">
                  <FileText className="w-5 h-5 text-green-600" />
                  <div className="text-left">
                    <p className="font-medium text-gray-900">{selectedFile.name}</p>
                    <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div>
              <h3 className="text-lg font-semibold text-gray-700">
                {dragActive ? "Drop your file here" : "Choose a file or drag it here"}
              </h3>
              <p className="text-gray-500">PDF files only, up to 10MB</p>
            </div>
          )}
        </div>
      </div>

      {/* File Requirements */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">File Requirements:</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            PDF format only
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            Maximum file size: 10MB
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            Text-based PDFs (not scanned images)
          </li>
          <li className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            Files are automatically deleted after processing
          </li>
        </ul>
      </div>

      {/* Upload Button */}
      <div className="mt-8 flex justify-center">
        <button
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          className={`
            px-8 py-3 rounded-lg font-semibold text-white transition-all duration-200
            ${
              !selectedFile || isUploading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 hover:shadow-lg"
            }
          `}
        >
          {isUploading ? (
            <div className="flex items-center gap-2">
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing with AI...
            </div>
          ) : (
            "Parse Resume"
          )}
        </button>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 rounded-lg border border-red-200">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-600" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
      )}

      {/* Processing Status */}
      {isUploading && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center gap-3">
            <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
            <div>
              <p className="font-medium text-blue-900">Processing your resume...</p>
              <p className="text-sm text-blue-700">AI is extracting and structuring your information</p>
            </div>
          </div>
        </div>
      )}

      {/* Privacy Notice */}
      <div className="mt-4 p-3 bg-green-50 rounded-lg border border-green-200">
        <div className="flex items-center gap-2">
          <CheckCircle className="w-4 h-4 text-green-600" />
          <p className="text-green-700 text-xs">
            <strong>Privacy Protected:</strong> Your resume is processed temporarily and automatically deleted. No data
            is stored permanently.
          </p>
        </div>
      </div>
    </div>
  )
}
