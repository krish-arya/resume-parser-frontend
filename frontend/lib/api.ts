// API utility functions for Flask backend integration

export interface FlaskResumeData {
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

export async function uploadResumeToFlask(file: File): Promise<FlaskResumeData> {
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

  return response.json()
}

export function validateResumeData(data: any): data is FlaskResumeData {
  return (
    typeof data === "object" &&
    typeof data.name === "string" &&
    Array.isArray(data.skills) &&
    Array.isArray(data.education) &&
    Array.isArray(data.projects) &&
    Array.isArray(data.Experience) &&
    Array.isArray(data.Achievements) &&
    Array.isArray(data.Position_of_responsibility) &&
    typeof data.Contact_Info === "object"
  )
}
