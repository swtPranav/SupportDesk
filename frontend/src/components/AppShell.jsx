import { NavLink, useNavigate } from "react-router-dom";
import { LayoutDashboard, Ticket, Users, LogOut } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./AppShell.css";

export default function AppShell({ title, children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const signOut = () => {
    logout();
    navigate("/login");
  };

  return <div className="app-shell">
    <aside className="app-sidebar">
      <div className="app-logo">SupportDesk</div>
      <nav>
        <NavLink to="/dashboard"><LayoutDashboard size={18} /> <span>Dashboard</span></NavLink>
        <NavLink to="/tickets"><Ticket size={18} /> <span>Tickets</span></NavLink>
        {user?.role === "admin" && <NavLink to="/agents"><Users size={18} /> <span>Agents</span></NavLink>}
      </nav>
    </aside>
    <div className="app-main">
      <header className="app-header"><h1>{title}</h1><div><span className="app-user">{user?.name || "Signed in"} · {user?.role}</span><button onClick={signOut}><LogOut size={16} /> Logout</button></div></header>
      <main className="app-content">{children}</main>
    </div>
  </div>;
}
