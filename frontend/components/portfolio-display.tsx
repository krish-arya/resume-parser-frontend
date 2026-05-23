"use client"

import { useRouter } from "next/navigation"
import {
  ArrowLeft,
  Download,
  Share2,
  Mail,
  Phone,
  MapPin,
  Linkedin,
  Github,
  GraduationCap,
  Award,
  Users,
  Code,
  Briefcase,
} from "lucide-react"

interface PortfolioData {
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

interface PortfolioDisplayProps {
  data: PortfolioData
}

export default function PortfolioDisplay({ data }: PortfolioDisplayProps) {
  const router = useRouter()

  const getContactIcon = (key: string) => {
    const lowerKey = key.toLowerCase()
    if (lowerKey.includes("email")) return <Mail className="w-4 h-4" />
    if (lowerKey.includes("phone")) return <Phone className="w-4 h-4" />
    if (lowerKey.includes("location")) return <MapPin className="w-4 h-4" />
    if (lowerKey.includes("linkedin")) return <Linkedin className="w-4 h-4" />
    if (lowerKey.includes("github")) return <Github className="w-4 h-4" />
    return <Mail className="w-4 h-4" />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button
              onClick={() => router.push("/")}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              Back to Upload
            </button>

            <div className="flex items-center gap-3">
              <button className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <Share2 className="w-4 h-4" />
                Share
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Download className="w-4 h-4" />
                Download PDF
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Profile Card */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-center mb-6">
                <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-white">
                    {data.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </span>
                </div>
                <h1 className="text-2xl font-bold text-gray-900 mb-1">{data.name}</h1>
              </div>

              {/* Contact Info */}
              <div className="space-y-3">
                <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  Contact Information
                </h3>
                {Object.entries(data.Contact_Info).map(([key, value]) => (
                  <div key={key} className="flex items-center gap-3 text-sm">
                    {getContactIcon(key)}
                    <div>
                      <p className="font-medium text-gray-700">{key}</p>
                      <p className="text-gray-500">{value}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Skills */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Code className="w-4 h-4" />
                Skills & Technologies
              </h3>
              <div className="flex flex-wrap gap-2">
                {data.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-200"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Educational Qualifications */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <GraduationCap className="w-5 h-5" />
                Educational Qualifications
              </h2>
              <div className="space-y-4">
                {data.education.map((edu, index) => (
                  <div key={index} className="border-l-4 border-green-500 pl-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">Institute: {edu.Institute_name}</h3>
                    <p className="text-gray-600 mb-1">Degree: {edu.Degree_name}</p>
                    <small className="text-gray-500">Marks: {edu.Marks}</small>
                  </div>
                ))}
              </div>
            </div>

            {/* Work Experience */}
            {data.Experience.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Briefcase className="w-5 h-5" />
                  Work Experience
                </h2>
                <div className="space-y-6">
                  {data.Experience.map((exp, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-6 pb-6 last:pb-0">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{exp.Company}</h3>
                      <p className="text-blue-600 font-medium mb-3">{exp.Position}</p>
                      <small className="text-gray-500">Skills: {exp.Skills.join(", ")}</small>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Projects */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Code className="w-5 h-5" />
                Projects
              </h2>
              <div className="space-y-6">
                {data.projects.map((project, index) => (
                  <div key={index} className="border-l-4 border-purple-500 pl-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{project.title}</h3>
                    <p className="text-gray-600 mb-3">{project.desc}</p>
                    <small className="text-gray-500">Tech: {project.tech.join(", ")}</small>
                  </div>
                ))}
              </div>
            </div>

            {/* Achievements */}
            {data.Achievements.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Award className="w-5 h-5" />
                  Achievements
                </h2>
                <div className="space-y-4">
                  {data.Achievements.map((achievement, index) => (
                    <div key={index} className="border-l-4 border-yellow-500 pl-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{achievement.achievement_name}</h3>
                      <p className="text-yellow-600 font-medium mb-1">Offered By: {achievement.institute_name}</p>
                      <small className="text-gray-500">Description: {achievement.description}</small>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Position of Responsibility */}
            {data.Position_of_responsibility.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  Position of Responsibility
                </h2>
                <div className="space-y-4">
                  {data.Position_of_responsibility.map((responsibility, index) => (
                    <div key={index} className="border-l-4 border-orange-500 pl-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{responsibility.position_name}</h3>
                      <p className="text-orange-600 font-medium mb-1">Society: {responsibility.soc_name}</p>
                      <small className="text-gray-500">Description: {responsibility.description}</small>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
