import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function Sessions() {
  const { token } = useAuth();
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSessions = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `${API_BASE}/api/sessions?page=1&per_page=20`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.message || "Failed to load sessions");
        }
        setSessions(payload.sessions || []);
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchSessions();
    }
  }, [token]);

  return (
    <div className="page listings-page">
      <section className="page-header">
        <h1>Training Sessions</h1>
        <p>View available sessions and plan your training schedule.</p>
      </section>
      {loading && <div className="status-message">Loading sessions...</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="card-grid">
        {sessions.map((session) => (
          <article key={session.id} className="card">
            <h2>{session.title}</h2>
            <p>{session.location}</p>
            <p>
              {session.date} • {session.start_time} - {session.end_time}
            </p>
            <p>Capacity: {session.capacity}</p>
          </article>
        ))}
        {!loading && sessions.length === 0 && (
          <p>No sessions are available yet.</p>
        )}
      </div>
    </div>
  );
}
