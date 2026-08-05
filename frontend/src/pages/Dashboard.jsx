import { useAuth } from "../hooks/useAuth.jsx";
import { Link } from "react-router-dom";

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="page dashboard-page">
      <section className="dashboard-hero">
        <h1>Welcome back, {user?.username || "ClubSync user"}</h1>
        <p>Role: {user?.role}</p>
      </section>
      <section className="dashboard-grid">
        <Link to="/teams" className="dashboard-card">
          <h2>Teams</h2>
          <p>Browse and manage sports teams.</p>
        </Link>
        <Link to="/sessions" className="dashboard-card">
          <h2>Sessions</h2>
          <p>View upcoming training sessions.</p>
        </Link>
        <Link to="/notifications" className="dashboard-card">
          <h2>Notifications</h2>
          <p>See announcements and schedule updates.</p>
        </Link>
        <Link to="/profile" className="dashboard-card">
          <h2>Profile</h2>
          <p>Update your profile and account settings.</p>
        </Link>
      </section>
    </div>
  );
}
