import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import AppShell from "../components/AppShell";
import "./Tickets.css";

const emptyTicket = { customer_name: "", customer_email: "", subject: "", description: "", priority: "Medium" };
const messageFor = (error, fallback) => error.response?.data?.detail || fallback;

export default function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [filters, setFilters] = useState({ search: "", status: "", priority: "" });
  const [page, setPage] = useState(1); const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false); const [form, setForm] = useState(emptyTicket); const [saving, setSaving] = useState(false);
  const loadTickets = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const { data } = await api.get("/api/tickets", { params: { page, page_size: 10, ...(filters.search && { search: filters.search }), ...(filters.status && { status: filters.status }), ...(filters.priority && { priority: filters.priority }) } });
      setTickets(data.tickets); setTotalPages(data.total_pages);
    } catch (err) { setError(messageFor(err, "Could not load tickets.")); } finally { setLoading(false); }
  }, [filters, page]);
  useEffect(() => { loadTickets(); }, [loadTickets]);
  const submitCreate = async (event) => {
    event.preventDefault(); setSaving(true); setError("");
    try { await api.post("/api/tickets", form); setShowCreate(false); setForm(emptyTicket); setPage(1); await loadTickets(); }
    catch (err) { setError(messageFor(err, "Could not create ticket.")); } finally { setSaving(false); }
  };
  const updateFilters = (field, value) => { setFilters({ ...filters, [field]: value }); setPage(1); };
  return <AppShell title="Tickets">
    <div className="page-intro"><div><h2>Support tickets</h2><p>Track, update, and resolve customer requests.</p></div><button className="primary" onClick={() => setShowCreate(true)}>+ Create ticket</button></div>
    <section className="filters"><input aria-label="Search tickets" value={filters.search} onChange={(e) => updateFilters("search", e.target.value)} placeholder="Search customer or subject" /><select value={filters.status} onChange={(e) => updateFilters("status", e.target.value)}><option value="">All statuses</option><option>Open</option><option>In Progress</option><option>Resolved</option><option>Closed</option></select><select value={filters.priority} onChange={(e) => updateFilters("priority", e.target.value)}><option value="">All priorities</option><option>High</option><option>Medium</option><option>Low</option></select><button className="secondary" onClick={() => { setFilters({ search: "", status: "", priority: "" }); setPage(1); }}>Clear</button></section>
    {error && <div className="alert error">{error}</div>}
    <section className="table-card">{loading ? <div className="state">Loading tickets…</div> : tickets.length === 0 ? <div className="state">No tickets match these filters.</div> : <div className="table-scroll"><table><thead><tr><th>Ticket</th><th>Customer</th><th>Subject</th><th>Created</th><th>Status</th><th>Priority</th><th>Assigned</th><th /></tr></thead><tbody>{tickets.map((ticket) => <tr key={ticket.ticket_id}><td className="ticket-id">{ticket.ticket_id}</td><td><strong>{ticket.customer_name}</strong><small>{ticket.customer_email}</small></td><td>{ticket.subject}</td><td>{new Date(ticket.created_at).toLocaleDateString()}</td><td><span className={`pill status-${ticket.status.toLowerCase().replaceAll(" ", "-")}`}>{ticket.status}</span></td><td><span className={`pill priority-${ticket.priority.toLowerCase()}`}>{ticket.priority}</span></td><td>{ticket.assigned_to ? `Agent #${ticket.assigned_to}` : "Unassigned"}</td><td><Link className="text-button" to={`/tickets/${ticket.ticket_id}`}>View</Link></td></tr>)}</tbody></table></div>}</section>
    <div className="pagination"><button className="secondary" disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button><span>Page {page} of {totalPages || 1}</span><button className="secondary" disabled={!totalPages || page >= totalPages} onClick={() => setPage(page + 1)}>Next</button></div>
    {showCreate && <div className="modal-backdrop"><form className="modal" onSubmit={submitCreate}><div className="modal-title"><h2>Create ticket</h2><button type="button" className="icon-button" onClick={() => setShowCreate(false)}>×</button></div><label>Customer name<input required minLength="2" value={form.customer_name} onChange={(e) => setForm({ ...form, customer_name: e.target.value })} /></label><label>Customer email<input required type="email" value={form.customer_email} onChange={(e) => setForm({ ...form, customer_email: e.target.value })} /></label><label>Subject<input required minLength="3" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} /></label><label>Description<textarea required value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></label><label>Priority<select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}><option>High</option><option>Medium</option><option>Low</option></select></label><div className="modal-actions"><button type="button" className="secondary" onClick={() => setShowCreate(false)}>Cancel</button><button className="primary" disabled={saving}>{saving ? "Creating…" : "Create ticket"}</button></div></form></div>}
  </AppShell>;
}
