import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function Members() {
  const { token, user } = useAuth();
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user?.role !== "admin" && user?.role !== "coach") {
      return;
    }

    const fetchMembers = async () => {
      setLoading(true);
      setError(null);
      try {
        const endpoint =
          user.role === "coach"
            ? "/api/coach/members"
            : "/api/members?page=1&per_page=20";
        const response = await fetch(`${API_BASE}${endpoint}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.message || "Failed to load members");
        }
        setMembers(
          user.role === "coach" ? payload.members || [] : payload.members || [],
        );
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMembers();
  }, [user, token]);

  if (user?.role !== "admin" && user?.role !== "coach") {
    return (
      <div className="page">
        <p>Members list is available only for admin and coach users.</p>
      </div>
    );
  }

  return (
    <div className="page listings-page">
      <section className="page-header">
        <h1>Members</h1>
        <p>Monitor member enrollment and manage member profiles.</p>
      </section>
      {loading && <div className="status-message">Loading members...</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="card-grid">
        {members.map((member) => (
          <article key={member.id} className="card">
            <h2>{member.username}</h2>
            <p>{member.email}</p>
            <p>Role: {member.role}</p>
          </article>
        ))}
        {!loading && members.length === 0 && <p>No members found.</p>}
      </div>
    </div>
  );
}
