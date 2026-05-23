import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest, { params }: { params: { websiteId: string } }) {
  try {
    const { websiteId } = params

    const flaskResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/download/${websiteId}`)

    if (!flaskResponse.ok) {
      throw new Error("Download not available")
    }

    const blob = await flaskResponse.blob()

    return new NextResponse(blob, {
      headers: {
        "Content-Type": "application/zip",
        "Content-Disposition": "attachment; filename=portfolio_website.zip",
      },
    })
  } catch (error) {
    console.error("Download Error:", error)
    return NextResponse.json({ error: "Download failed" }, { status: 500 })
  }
}