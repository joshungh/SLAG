import { jwtVerify, SignJWT } from "jose";

const JWT_SECRET = process.env.JWT_SECRET_KEY || "your-secret-key";

export interface JwtPayload {
  userId: string;
  loginMethod: string;
  exp?: number;
}

export async function verifyJwt(token: string): Promise<JwtPayload | null> {
  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(JWT_SECRET)
    );
    return payload as JwtPayload;
  } catch (error) {
    console.error("JWT verification error:", error);
    return null;
  }
}

export async function createJwt(payload: JwtPayload): Promise<string> {
  try {
    const jwt = await new SignJWT(payload)
      .setProtectedHeader({ alg: "HS256" })
      .setExpirationTime("24h")
      .sign(new TextEncoder().encode(JWT_SECRET));
    return jwt;
  } catch (error) {
    console.error("JWT creation error:", error);
    throw error;
  }
}
