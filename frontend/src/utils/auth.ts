import { jwtVerify, SignJWT } from "jose";

if (!process.env.JWT_SECRET_KEY) {
  throw new Error("JWT_SECRET_KEY is not defined in environment variables");
}

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET_KEY);

export interface JwtPayload {
  userId: string;
  loginMethod: string;
  exp?: number;
}

export class AuthError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AuthError";
  }
}

export async function verifyJwt(token: string): Promise<JwtPayload> {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET);
    return payload as JwtPayload;
  } catch (error) {
    if (error instanceof Error) {
      throw new AuthError(`Failed to verify token: ${error.message}`);
    }
    throw new AuthError("Failed to verify token");
  }
}

export async function createJwt(
  payload: Omit<JwtPayload, "exp">
): Promise<string> {
  try {
    return await new SignJWT(payload)
      .setProtectedHeader({ alg: "HS256" })
      .setExpirationTime("24h")
      .setIssuedAt()
      .sign(JWT_SECRET);
  } catch (error) {
    if (error instanceof Error) {
      throw new AuthError(`Failed to create token: ${error.message}`);
    }
    throw new AuthError("Failed to create token");
  }
}

// Token management functions
export const setToken = (token: string): void => {
  localStorage.setItem("auth_token", token);
};

export const getToken = (): string | null => {
  return localStorage.getItem("auth_token");
};

export const removeToken = (): void => {
  localStorage.removeItem("auth_token");
};
