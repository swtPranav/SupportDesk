import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Ticket,
  Users,
  LogOut,
  ClipboardList,
  CircleDot,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  UserCheck,
} from "lucide-react";

import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const { user, logout } = useAuth();

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get("/api/dashboard/stats");
        setDashboard(response.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="dashboard-message">
        Loading dashboard...
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-message">
        {error}
      </div>
    );
  }

  return (
    <div className="dashboard">

      {/* Sidebar */}

      <aside className="sidebar">
        <div className="sidebar-logo">
          SupportDesk
        </div>

        <nav className="sidebar-nav">

          <NavLink
            to="/dashboard"
            className="sidebar-link active"
          >
            <LayoutDashboard size={19} />
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/tickets"
            className="sidebar-link"
          >
            <Ticket size={19} />
            <span>Tickets</span>
          </NavLink>

          {user?.role === "admin" && (
            <NavLink
              to="/agents"
              className="sidebar-link"
            >
              <Users size={19} />
              <span>Agents</span>
            </NavLink>
          )}

        </nav>
      </aside>

      {/* Main */}

      <div className="dashboard-main">

        {/* Header */}

        <header className="dashboard-header">

          <div className="dashboard-title">
            Dashboard
          </div>

          <div className="user-section">

            <div className="user-info">
              <div className="user-name">
                {user?.name}
              </div>

              <div className="user-role">
                {user?.role}
              </div>
            </div>

            <button
              className="logout-button"
              onClick={logout}
            >
              <LogOut size={16} />
              Logout
            </button>

          </div>

        </header>

        {/* Content */}

        <main className="dashboard-content">

          <section className="welcome-section">
            <h1>Welcome back, {user?.name} 👋</h1>

            <p>
              Here's what's happening with your support tickets.
            </p>
          </section>

          {/* Primary statistics */}

          <section className="stats-grid">

            <div className="stat-card">
              <div className="stat-info">
                <p>Total Tickets</p>
                <h2>{dashboard?.total_tickets ?? 0}</h2>
              </div>

              <div className="stat-icon">
                <ClipboardList size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>Open Tickets</p>
                <h2>{dashboard?.open_tickets ?? 0}</h2>
              </div>

              <div className="stat-icon">
                <CircleDot size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>In Progress</p>
                <h2>
                  {dashboard?.in_progress_tickets ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <Clock size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>Resolved</p>
                <h2>
                  {dashboard?.resolved_tickets ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <CheckCircle size={21} />
              </div>
            </div>

          </section>

          {/* Secondary statistics */}

          <section className="secondary-grid">

            <div className="stat-card">
              <div className="stat-info">
                <p>Closed Tickets</p>
                <h2>
                  {dashboard?.closed_tickets ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <XCircle size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>High Priority</p>
                <h2>
                  {dashboard?.high_priority_tickets ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <AlertTriangle size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>Assigned Tickets</p>
                <h2>
                  {dashboard?.assigned_tickets ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <UserCheck size={21} />
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-info">
                <p>Active Agents</p>
                <h2>
                  {dashboard?.active_agents ?? 0}
                </h2>
              </div>

              <div className="stat-icon">
                <Users size={21} />
              </div>
            </div>

          </section>

        </main>

      </div>

    </div>
  );
}

export default Dashboard;
