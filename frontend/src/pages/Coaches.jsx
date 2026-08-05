import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function Coaches() {
  const { token, user } = useAuth();
  const [coaches, setCoaches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user?.role !== "admin") {
      return;
    }

    const fetchCoaches = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `${API_BASE}/api/coaches?page=1&per_page=20`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.message || "Failed to load coaches");
        }
        setCoaches(payload.coaches || []);
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCoaches();
  }, [user, token]);

  if (user?.role !== "admin") {
    return (
      <div className="page">
        <p>Coaches list is available only for admins.</p>
      </div>
    );
  }

  return (
    <div className="page listings-page">
      <section className="page-header">
        <h1>Coaches</h1>
        <p>Manage coach accounts and teams from the admin dashboard.</p>
      </section>
      {loading && <div className="status-message">Loading coaches...</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="card-grid">
        {coaches.map((coach) => (
          <article key={coach.id} className="card">
            <h2>{coach.username}</h2>
            <p>{coach.email}</p>
            <p>Role: {coach.role}</p>
          </article>
        ))}
        {!loading && coaches.length === 0 && <p>No coaches found.</p>}
      </div>
    </div>
  );
}
