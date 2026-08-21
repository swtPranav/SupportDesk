import { createContext, useContext, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("supportdesk_user");
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [token, setToken] = useState(
    localStorage.getItem("access_token")
  );

  const login = async (email, password) => {
    const response = await api.post("/api/auth/login", {
      email,
      password,
    });

    const data = response.data;

    localStorage.setItem("access_token", data.access_token);

    setToken(data.access_token);

    const loggedInUser = {
      id: data.user_id,
      name: data.name,
      email: data.email,
      role: data.role,
    };
    localStorage.setItem("supportdesk_user", JSON.stringify(loggedInUser));
    setUser(loggedInUser);

    return data;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("supportdesk_user");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated: Boolean(token),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
