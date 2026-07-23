import { useState, useEffect } from "react";
import { getApplications, createApplication, updateApplicationStatus, getJobs } from "../api";

const STATUSES = ["applied", "interviewing", "offer", "rejected", "withdrawn"];

export default function ApplicationsPage() {
  const [apps, setApps] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ job_id: "", status: "applied", notes: "" });
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    Promise.all([loadApps(), loadJobs()]);
  }, []);

  async function loadApps() {
    try {
      setLoading(true);
      setApps(await getApplications());
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  }

  async function loadJobs() {
    try {
      setJobs(await getJobs());
    } catch (_) {}
  }

  async function handleCreate(e) {
    e.preventDefault();
    try {
      await createApplication({ ...form, job_id: Number(form.job_id) });
      setMsg({ type: "success", text: "Application created!" });
      setShowForm(false);
      setForm({ job_id: "", status: "applied", notes: "" });
      await loadApps();
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    }
  }

  async function handleStatus(id, status) {
    try {
      await updateApplicationStatus(id, status);
      setMsg({ type: "success", text: "Status updated!" });
      await loadApps();
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    }
  }

  function jobTitle(id) {
    const job = jobs.find((j) => j.id === id);
    return job ? `${job.company} — ${job.title}` : `Job #${id}`;
  }

  return (
    <div>
      <div className="flex-between mb-1">
        <h1>Applications</h1>
        <button className="btn btn-success" onClick={() => setShowForm(!showForm)}>
          {showForm ? "✕ Cancel" : "+ New Application"}
        </button>
      </div>

      {msg && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      {showForm && (
        <div className="card">
          <h2>New Application</h2>
          <form onSubmit={handleCreate}>
            <div className="form-row">
              <div className="form-group">
                <label>Job</label>
                <select value={form.job_id} onChange={(e) => setForm({ ...form, job_id: e.target.value })} required>
                  <option value="">— Select a job —</option>
                  {jobs.map((j) => (
                    <option key={j.id} value={j.id}>{j.company} — {j.title}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Status</label>
                <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
            </div>
            <button className="btn btn-primary" type="submit">Create</button>
          </form>
        </div>
      )}

      <div className="card">
        {loading ? (
          <div className="loading">Loading applications…</div>
        ) : apps.length === 0 ? (
          <p className="text-muted">No applications yet. Create one above!</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Job</th>
                  <th>Status</th>
                  <th>Notes</th>
                  <th>Applied On</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {apps.map((a) => (
                  <tr key={a.id}>
                    <td>{jobTitle(a.job_id)}</td>
                    <td>
                      <span className={`badge badge-${a.status === "rejected" ? "red" : a.status === "offer" ? "green" : "blue"}`}>
                        {a.status}
                      </span>
                    </td>
                    <td className="text-muted">{a.notes || "—"}</td>
                    <td className="text-muted">{a.applied_on ? new Date(a.applied_on).toLocaleDateString() : "—"}</td>
                    <td>
                      <select
                        value={a.status}
                        onChange={(e) => handleStatus(a.id, e.target.value)}
                        className="btn-sm"
                        style={{ border: "1px solid #ced4da", borderRadius: 4, padding: "0.2rem 0.4rem" }}
                      >
                        {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}