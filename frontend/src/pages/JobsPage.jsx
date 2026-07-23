import { useState, useEffect } from "react";
import { getJobs, syncJobs } from "../api";

export default function JobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    loadJobs();
  }, []);

  async function loadJobs() {
    try {
      setLoading(true);
      const data = await getJobs();
      setJobs(data);
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  }

  async function handleSync() {
    try {
      setSyncing(true);
      const result = await syncJobs();
      setMsg({ type: "success", text: `Synced! ${result.saved} new jobs saved.` });
      await loadJobs();
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setSyncing(false);
    }
  }

  return (
    <div>
      <div className="flex-between mb-1">
        <h1>Jobs</h1>
        <button className="btn btn-primary" onClick={handleSync} disabled={syncing}>
          {syncing ? "Syncing…" : "🔄 Sync Jobs"}
        </button>
      </div>

      {msg && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      <div className="card">
        {loading ? (
          <div className="loading">Loading jobs…</div>
        ) : jobs.length === 0 ? (
          <p className="text-muted">No jobs found. Click "Sync Jobs" to fetch the latest listings.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Company</th>
                  <th>Title</th>
                  <th>Location</th>
                  <th>Salary</th>
                  <th>Source</th>
                  <th>Posted</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id}>
                    <td><strong>{job.company}</strong></td>
                    <td>{job.title}</td>
                    <td>{job.location}</td>
                    <td>{job.salary || "—"}</td>
                    <td><span className="badge badge-blue">{job.source}</span></td>
                    <td className="text-muted">{job.posted_date}</td>
                    <td>
                      <a href={job.apply_url} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm">
                        Apply ↗
                      </a>
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