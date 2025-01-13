import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { verifyJwt, AuthError } from "@/utils/auth";
import { getToken } from "@/utils/token";

// GET /api/users/profile
export async function GET(req: NextRequest) {
  try {
    // Get the token from the Authorization header
    const authHeader = req.headers.get("authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json(
        { error: "Missing or invalid authorization header" },
        { status: 401 }
      );
    }

    const token = authHeader.split(" ")[1];
    const payload = await verifyJwt(token);

    if (!payload || !payload.userId) {
      return NextResponse.json(
        { error: "Invalid or expired token" },
        { status: 401 }
      );
    }

    const BACKEND_URL = process.env.BACKEND_URL;
    if (!BACKEND_URL) {
      throw new Error("BACKEND_URL environment variable is not set");
    }

    // Get user profile from Python backend
    const response = await fetch(`${BACKEND_URL}/api/users/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.detail || "Failed to fetch profile" },
        { status: response.status }
      );
    }

    const user = await response.json();
    return NextResponse.json(user);
  } catch (error) {
    console.error("Profile fetch error:", error);
    return NextResponse.json(
      { error: "Failed to fetch profile" },
      { status: 500 }
    );
  }
}

// PUT /api/users/profile
export async function PUT(req: NextRequest) {
  try {
    const authHeader = req.headers.get("authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json(
        { error: "Missing or invalid authorization header" },
        { status: 401 }
      );
    }

    const token = authHeader.split(" ")[1];
    const payload = await verifyJwt(token);

    if (!payload || !payload.userId) {
      return NextResponse.json(
        { error: "Invalid or expired token" },
        { status: 401 }
      );
    }

    const BACKEND_URL = process.env.BACKEND_URL;
    if (!BACKEND_URL) {
      throw new Error("BACKEND_URL environment variable is not set");
    }

    const formData = await req.formData();

    // Forward the request to Python backend
    const response = await fetch(`${BACKEND_URL}/api/users/profile`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      return NextResponse.json(
        { error: errorData.detail || "Failed to update profile" },
        { status: response.status }
      );
    }

    const updatedUser = await response.json();
    return NextResponse.json(updatedUser);
  } catch (error) {
    console.error("Profile update error:", error);
    return NextResponse.json(
      { error: "Failed to update profile" },
      { status: 500 }
    );
  }
}
