import { useAuth } from "../hooks/useAuth.jsx";
import { Link } from "react-router-dom";
import { Users, Calendar, Bell, User } from "lucide-react";

const cards = [
  { to: "/teams", title: "Teams", description: "Browse and manage sports teams.", icon: Users },
  { to: "/sessions", title: "Sessions", description: "View upcoming training sessions.", icon: Calendar },
  { to: "/notifications", title: "Notifications", description: "See announcements and schedule updates.", icon: Bell },
  { to: "/profile", title: "Profile", description: "Update your profile and account settings.", icon: User },
];

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10 md:px-12">
      <section className="mx-auto mb-10 max-w-5xl rounded-2xl bg-brand-black p-8 text-white shadow-sm">
        <h1 className="text-2xl font-bold md:text-3xl">
          Welcome back, <span className="text-brand-green">{user?.username || "ClubSync user"}</span>
        </h1>
        <p className="mt-2 inline-block rounded-full bg-white/10 px-3 py-1 text-sm font-medium capitalize text-brand-green">
          Role: {user?.role}
        </p>
      </section>

      <section className="mx-auto grid max-w-5xl grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map(({ to, title, description, icon: Icon }) => (
          <Link
            key={to}
            to={to}
            className="group rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-100 transition hover:-translate-y-1 hover:shadow-md hover:ring-brand-green"
          >
            <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-brand-black text-brand-green transition group-hover:bg-brand-green group-hover:text-brand-black">
              <Icon size={22} />
            </div>
            <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
            <p className="mt-1 text-sm text-slate-500">{description}</p>
          </Link>
        ))}
      </section>
    </div>
  );
}