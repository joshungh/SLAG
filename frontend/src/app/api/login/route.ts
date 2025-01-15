import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const BACKEND_URL = process.env.BACKEND_URL;
    if (!BACKEND_URL) {
      throw new Error("BACKEND_URL environment variable is not set");
    }

    const data = await request.json();
    console.log("Login request data:", data);

    // Forward request to FastAPI backend
    const response = await fetch(`${BACKEND_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    console.log("Backend response status:", response.status);
    const responseText = await response.text();
    console.log("Backend response text:", responseText);

    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (e) {
      console.error("Failed to parse response as JSON:", e);
      return NextResponse.json(
        { error: "Invalid response from server" },
        { status: 500 }
      );
    }

    if (!response.ok) {
      console.error("Login failed:", responseData);
      return NextResponse.json(
        {
          error: responseData.detail || responseData.message || "Login failed",
        },
        { status: response.status }
      );
    }

    return NextResponse.json(responseData);
  } catch (error) {
    console.error("Error during login:", error);
    return NextResponse.json(
      { error: "Failed to process login" },
      { status: 500 }
    );
  }
}
