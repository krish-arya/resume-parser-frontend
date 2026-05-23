import { type NextRequest, NextResponse } from "next/server"

// Proxy route to handle Flask backend communication
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const flaskResponse = await fetch('${process.env.NEXT_PUBLIC_API_URL}/', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    const data = await flaskResponse.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Flask proxy error:", error)
    return NextResponse.json({ error: "Failed to connect to Flask backend" }, { status: 500 })
  }
}
