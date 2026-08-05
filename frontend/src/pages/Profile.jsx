import { useAuth } from "../hooks/useAuth.jsx";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="page profile-page">
      <section className="page-header">
        <h1>Profile</h1>
        <p>Review your account details and role permissions.</p>
      </section>
      <div className="profile-card">
        <div>
          <strong>Username</strong>
          <p>{user?.username}</p>
        </div>
        <div>
          <strong>Email</strong>
          <p>{user?.email}</p>
        </div>
        <div>
          <strong>Role</strong>
          <p>{user?.role}</p>
        </div>
      </div>
      <div className="status-message">
        Profile editing is available through the club admin interface when
        connected to the backend.
      </div>
    </div>
  );
}
