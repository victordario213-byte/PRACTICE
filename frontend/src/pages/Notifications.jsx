import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function Notifications() {
  const { token } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNotifications = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(
          `${API_BASE}/api/notifications?page=1&per_page=20`,
          {
            headers: { Authorization: `Bearer ${token}` },
          },
        );
        const payload = await response.json();
        if (!response.ok) {
          throw new Error(payload.message || "Failed to load notifications");
        }
        setNotifications(payload.notifications || []);
      } catch (fetchError) {
        setError(fetchError.message);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchNotifications();
    }
  }, [token]);

  return (
    <div className="page listings-page">
      <section className="page-header">
        <h1>Notifications</h1>
        <p>Stay updated on session changes and announcements.</p>
      </section>
      {loading && (
        <div className="status-message">Loading notifications...</div>
      )}
      {error && <div className="error-message">{error}</div>}
      <div className="card-grid">
        {notifications.map((notification) => (
          <article key={notification.id} className="card notification-card">
            <h2>{notification.title}</h2>
            <p>{notification.message}</p>
            <p className="meta">
              {new Date(notification.created_at).toLocaleString()}
            </p>
          </article>
        ))}
        {!loading && notifications.length === 0 && <p>No notifications yet.</p>}
      </div>
    </div>
  );
}
