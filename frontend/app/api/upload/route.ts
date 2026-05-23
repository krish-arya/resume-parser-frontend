import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    if (file.type !== "application/pdf") {
      return NextResponse.json({ error: "Only PDF files are allowed" }, { status: 400 })
    }

    // Forward to Flask backend
    const flaskFormData = new FormData()
    flaskFormData.append("file", file)

    const flaskResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/`, {
      method: "POST",
      body: flaskFormData,
    })

    if (!flaskResponse.ok) {
      const errorData = await flaskResponse.json()
      throw new Error(errorData.error || `Flask backend error: ${flaskResponse.status}`)
    }

    const data = await flaskResponse.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("API Error:", error)
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : "Failed to process resume",
      },
      { status: 500 },
    )
  }
}
