import { NavLink } from "react-router-dom";

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/teams", label: "Teams" },
  { to: "/sessions", label: "Sessions" },
  { to: "/notifications", label: "Notifications" },
  { to: "/profile", label: "Profile" },
];

export function NavBar({ user, onLogout }) {
  return (
    <nav className="flex items-center justify-between bg-brand-black px-6 py-4 md:px-12">
      <div className="text-xl font-bold text-white">
        Club<span className="text-brand-green">Sync</span>
      </div>

      <div className="hidden gap-6 md:flex">
        {links.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `text-sm font-medium transition ${
                isActive
                  ? "text-brand-green"
                  : "text-slate-300 hover:text-white"
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </div>

      <div className="flex items-center gap-3">
        {user ? (
          <span className="rounded-full bg-brand-green/10 px-3 py-1 text-xs font-semibold capitalize text-brand-green">
            {user.role}
          </span>
        ) : null}
        <button
          type="button"
          onClick={onLogout}
          className="rounded-lg border border-slate-600 px-4 py-1.5 text-sm font-medium text-white transition hover:border-brand-green hover:text-brand-green"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}