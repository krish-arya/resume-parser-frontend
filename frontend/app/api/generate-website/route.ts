import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const flaskResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate-website`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    if (!flaskResponse.ok) {
      const errorData = await flaskResponse.json()
      throw new Error(errorData.error || "Website generation failed")
    }

    const data = await flaskResponse.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Generation Error:", error)
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : "Failed to generate website",
      },
      { status: 500 },
    )
  }
}
