import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest, { params }: { params: { websiteId: string } }) {
  try {
    const { websiteId } = params

    console.log(`Fetching preview for website ID: ${websiteId}`)

    const flaskResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/preview/${websiteId}`, {
      method: "GET",
      headers: {
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      },
    })

    console.log(`Flask response status: ${flaskResponse.status}`)

    if (!flaskResponse.ok) {
      const errorText = await flaskResponse.text()
      console.error(`Flask error: ${errorText}`)

      // Return a basic error page instead of just throwing
      const errorHtml = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Preview Error</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
            .error { color: #dc2626; }
          </style>
        </head>
        <body>
          <h1 class="error">Preview Not Available</h1>
          <p>Website ID: ${websiteId}</p>
          <p>Error: ${errorText || "Unknown error"}</p>
          <button onclick="window.location.reload()">Retry</button>
        </body>
        </html>
      `

      return new NextResponse(errorHtml, {
        status: 200, // Return 200 so iframe loads the error page
        headers: {
          "Content-Type": "text/html; charset=utf-8",
        },
      })
    }

    const html = await flaskResponse.text()
    console.log(`HTML length: ${html.length}`)

    return new NextResponse(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        Pragma: "no-cache",
        Expires: "0",
      },
    })
  } catch (error) {
    console.error("Preview Error:", error)

    // Return a basic error page
    const errorHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Preview Error</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
          .error { color: #dc2626; }
        </style>
      </head>
      <body>
        <h1 class="error">Connection Error</h1>
        <p>Unable to connect to the preview service.</p>
        <p>Please make sure the Flask backend is running on port 5000.</p>
        <button onclick="window.location.reload()">Retry</button>
      </body>
      </html>
    `

    return new NextResponse(errorHtml, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
      },
    })
  }
}
