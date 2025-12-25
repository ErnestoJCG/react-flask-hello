import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  // Use environment variable for backend URL
  const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:3001";

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      // Normalize email (lowercase and trim)
      const normalizedEmail = email.trim().toLowerCase();
      const trimmedPassword = password.trim();

      // Basic validation
      if (!normalizedEmail || !trimmedPassword) {
        throw new Error("Email and password are required");
      }

      const response = await fetch(`${backendUrl}/api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          email: normalizedEmail, 
          password: trimmedPassword 
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || "Invalid credentials");
      }

      if (!data.token) {
        throw new Error("Authentication token missing");
      }

      // Store token and user data
      sessionStorage.setItem("token", data.token);
      if (data.user) {
        sessionStorage.setItem("user", JSON.stringify(data.user));
      }

      // Redirect to protected page
      navigate("/private");
      
    } catch (err) {
      setError(err.message);
      console.error("Login error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "500px" }}>
      <h2 className="mb-4">Login</h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="username"
            placeholder="Enter your email"
          />
        </div>

        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            placeholder="Your password"
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary w-100" 
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Logging in...
            </>
          ) : (
            "Login"
          )}
        </button>
      </form>

      <p className="mt-3 text-center">
        Don't have an account? <a href="/signup">Sign Up</a>
      </p>
    </div>
  );
};