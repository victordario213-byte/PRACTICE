import { createContext, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "clubsync_auth";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (stored?.token && stored?.user) {
      setToken(stored.token);
      setUser(stored.user);
    }
  }, []);

  const saveAuth = (authData) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(authData));
    setToken(authData.token);
    setUser(authData.user);
  };

  const clearAuth = () => {
    localStorage.removeItem(STORAGE_KEY);
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = Boolean(token && user);

  return (
    <AuthContext.Provider
      value={{ user, token, isAuthenticated, saveAuth, clearAuth }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
