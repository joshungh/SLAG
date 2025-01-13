// Token management utilities
export const setToken = (token: string) => {
  localStorage.setItem("auth_token", token);
};

export const getToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("auth_token");
  }
  return null;
};

export const removeToken = () => {
  localStorage.removeItem("auth_token");
};

// Session management
export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};

// Add token to API requests
export const getAuthHeaders = () => {
  const token = getToken();
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
};
