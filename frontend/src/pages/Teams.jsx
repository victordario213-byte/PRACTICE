import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function Teams() {
  const { token, user } = useAuth();
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `${API_BASE}/api/teams?page=1&per_page=20`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.message || "Failed to load teams");
        }
        setTeams(payload.teams || []);
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchTeams();
    }
  }, [token]);

  return (
    <div className="page listings-page">
      <section className="page-header">
        <h1>Teams</h1>
        <p>Browse teams that are actively managed by coaches.</p>
      </section>
      {loading && <div className="status-message">Loading teams...</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="card-grid">
        {teams.map((team) => (
          <article key={team.id} className="card">
            <h2>{team.name}</h2>
            <p>{team.sport}</p>
            <p>{team.description}</p>
          </article>
        ))}
        {!loading && teams.length === 0 && <p>No teams are available yet.</p>}
      </div>
      <div className="page-footer">
        {user?.role === "coach" || user?.role === "admin" ? (
          <small>Coaches and admins can manage teams from the dashboard.</small>
        ) : null}
      </div>
    </div>
  );
}
