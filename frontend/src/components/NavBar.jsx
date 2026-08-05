import { Link } from "react-router-dom";

export function NavBar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="brand">ClubSync</div>
      <div className="links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/teams">Teams</Link>
        <Link to="/sessions">Sessions</Link>
        <Link to="/notifications">Notifications</Link>
        <Link to="/profile">Profile</Link>
      </div>
      <div className="actions">
        {user ? <span className="role-label">{user.role}</span> : null}
        <button type="button" onClick={onLogout} className="btn-logout">
          Logout
        </button>
      </div>
    </nav>
  );
}
