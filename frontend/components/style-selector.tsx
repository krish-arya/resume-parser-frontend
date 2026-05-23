"use client"

import { Monitor, Zap, Heart } from "lucide-react"

interface StyleSelectorProps {
  selectedStyle: "professional" | "futuristic" | "playful"
  onStyleSelect: (style: "professional" | "futuristic" | "playful") => void
  resumeData: any
}

export default function StyleSelector({ selectedStyle, onStyleSelect, resumeData }: StyleSelectorProps) {
  const styles = [
    {
      id: "professional" as const,
      name: "Professional",
      description: "Clean, minimal design perfect for corporate environments",
      icon: Monitor,
      colors: ["#2563eb", "#64748b", "#0f172a"],
      preview: "bg-gradient-to-br from-blue-50 to-slate-50",
    },
    {
      id: "futuristic" as const,
      name: "Futuristic",
      description: "Modern, tech-inspired design with glowing effects",
      icon: Zap,
      colors: ["#00d4ff", "#7c3aed", "#ec4899"],
      preview: "bg-gradient-to-br from-cyan-900 to-purple-900",
    },
    {
      id: "playful" as const,
      name: "Playful",
      description: "Vibrant, creative design with fun animations",
      icon: Heart,
      colors: ["#f59e0b", "#ec4899", "#10b981"],
      preview: "bg-gradient-to-br from-amber-100 to-pink-100",
    },
  ]

  return (
    <div className="grid md:grid-cols-3 gap-6">
      {styles.map((style) => {
        const Icon = style.icon
        return (
          <div
            key={style.id}
            className={`relative cursor-pointer rounded-xl border-2 transition-all duration-200 ${
              selectedStyle === style.id
                ? "border-blue-500 shadow-lg scale-105"
                : "border-gray-200 hover:border-gray-300 hover:shadow-md"
            }`}
            onClick={() => onStyleSelect(style.id)}
          >
            {/* Preview Area */}
            <div className={`h-48 rounded-t-xl ${style.preview} p-4 flex items-center justify-center`}>
              <div className="bg-white/90 backdrop-blur-sm rounded-lg p-4 w-full max-w-xs">
                <div className="flex items-center gap-3 mb-3">
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold"
                    style={{ backgroundColor: style.colors[0] }}
                  >
                    {resumeData.name.slice(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div className="font-semibold text-sm">{resumeData.name}</div>
                    <div className="text-xs text-gray-600">Developer</div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="h-2 bg-gray-200 rounded" style={{ backgroundColor: style.colors[1] + "40" }}></div>
                  <div
                    className="h-2 bg-gray-200 rounded w-3/4"
                    style={{ backgroundColor: style.colors[2] + "40" }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Style Info */}
            <div className="p-6">
              <div className="flex items-center gap-3 mb-3">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center text-white"
                  style={{ backgroundColor: style.colors[0] }}
                >
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">{style.name}</h3>
              </div>

              <p className="text-gray-600 mb-4">{style.description}</p>

              {/* Color Palette */}
              <div className="flex gap-2">
                {style.colors.map((color, index) => (
                  <div
                    key={index}
                    className="w-6 h-6 rounded-full border-2 border-white shadow-sm"
                    style={{ backgroundColor: color }}
                  />
                ))}
              </div>
            </div>

            {/* Selection Indicator */}
            {selectedStyle === style.id && (
              <div className="absolute top-4 right-4 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
