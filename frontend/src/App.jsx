import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./hooks/useAuth.jsx";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { NavBar } from "./components/NavBar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Teams from "./pages/Teams";
import Sessions from "./pages/Sessions";
import Members from "./pages/Members";
import Coaches from "./pages/Coaches";
import Notifications from "./pages/Notifications";
import Profile from "./pages/Profile";
import "./App.css";

function AppRoutes() {
  const { isAuthenticated, user, clearAuth } = useAuth();

  return (
    <BrowserRouter>
      {isAuthenticated && <NavBar user={user} onLogout={clearAuth} />}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teams"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Teams />
            </ProtectedRoute>
          }
        />
        <Route
          path="/sessions"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Sessions />
            </ProtectedRoute>
          }
        />
        <Route
          path="/members"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Members />
            </ProtectedRoute>
          }
        />
        <Route
          path="/coaches"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Coaches />
            </ProtectedRoute>
          }
        />
        <Route
          path="/notifications"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Notifications />
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
