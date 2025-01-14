import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const BACKEND_URL = process.env.BACKEND_URL;
    if (!BACKEND_URL) {
      throw new Error("BACKEND_URL environment variable is not set");
    }

    const data = await request.json();
    console.log("Registration request data:", data);

    // Determine endpoint based on login method
    const endpoint =
      data.login_method === "web3" ? "/api/users" : "/api/register";

    // Send request to FastAPI backend
    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
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
      console.error("Registration failed:", responseData);
      return NextResponse.json(
        {
          error:
            responseData.detail ||
            responseData.message ||
            "Registration failed",
        },
        { status: response.status }
      );
    }

    // For Web3 registration, check if user exists by wallet address
    if (data.login_method === "web3" && data.web3_wallet) {
      const userResponse = await fetch(
        `${BACKEND_URL}/api/users/wallet/${data.web3_wallet}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (userResponse.ok) {
        const userData = await userResponse.json();
        return NextResponse.json(userData);
      }
    }

    return NextResponse.json(responseData);
  } catch (error) {
    console.error("Error during registration:", error);
    return NextResponse.json(
      { error: "Failed to process registration" },
      { status: 500 }
    );
  }
}
