import { useState, useEffect } from "react";
import { getResumes, createResume, updateResume, deleteResume } from "../api";

const emptyForm = { name: "", skills: "", experience: "", education: "" };

export default function ResumesPage() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null); // null | 'new' | id
  const [form, setForm] = useState(emptyForm);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    loadResumes();
  }, []);

  async function loadResumes() {
    try {
      setLoading(true);
      setResumes(await getResumes());
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  }

  function startNew() {
    setEditing("new");
    setForm(emptyForm);
  }

  function startEdit(r) {
    setEditing(r.id);
    setForm({ name: r.name, skills: r.skills, experience: r.experience || "", education: r.education || "" });
  }

  function cancelEdit() {
    setEditing(null);
    setForm(emptyForm);
  }

  async function handleSave(e) {
    e.preventDefault();
    try {
      if (editing === "new") {
        await createResume(form);
        setMsg({ type: "success", text: "Resume created!" });
      } else {
        await updateResume(editing, form);
        setMsg({ type: "success", text: "Resume updated!" });
      }
      cancelEdit();
      await loadResumes();
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this resume?")) return;
    try {
      await deleteResume(id);
      setMsg({ type: "success", text: "Resume deleted." });
      await loadResumes();
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    }
  }

  return (
    <div>
      <div className="flex-between mb-1">
        <h1>Resumes</h1>
        {editing === null && (
          <button className="btn btn-success" onClick={startNew}>+ New Resume</button>
        )}
      </div>

      {msg && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      {/* Form */}
      {editing !== null && (
        <div className="card">
          <h2>{editing === "new" ? "New Resume" : "Edit Resume"}</h2>
          <form onSubmit={handleSave}>
            <div className="form-row">
              <div className="form-group">
                <label>Name</label>
                <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Skills (comma-separated)</label>
                <input value={form.skills} onChange={(e) => setForm({ ...form, skills: e.target.value })} required placeholder="Python, FastAPI, PostgreSQL" />
              </div>
            </div>
            <div className="form-group">
              <label>Experience</label>
              <textarea value={form.experience} onChange={(e) => setForm({ ...form, experience: e.target.value })} rows={3} />
            </div>
            <div className="form-group">
              <label>Education</label>
              <textarea value={form.education} onChange={(e) => setForm({ ...form, education: e.target.value })} rows={2} />
            </div>
            <div className="flex gap-1">
              <button className="btn btn-primary" type="submit">Save</button>
              <button className="btn" type="button" onClick={cancelEdit} style={{ background: "#e5e7eb" }}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* List */}
      <div className="card">
        {loading ? (
          <div className="loading">Loading resumes…</div>
        ) : resumes.length === 0 ? (
          <p className="text-muted">No resumes yet. Create one to start matching!</p>
        ) : (
          <div>
            {resumes.map((r) => (
              <div key={r.id} className="card" style={{ marginBottom: "0.75rem" }}>
                <div className="flex-between">
                  <div>
                    <strong>{r.name}</strong>
                    <div className="text-muted mt-1">
                      <span className="badge badge-blue">{r.skills.split(",").length} skills</span>
                      {r.experience && <span className="badge badge-gray" style={{ marginLeft: "0.4rem" }}>Has experience</span>}
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <button className="btn btn-primary btn-sm" onClick={() => startEdit(r)}>Edit</button>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(r.id)}>Delete</button>
                  </div>
                </div>
                {editing !== r.id && (
                  <div className="text-muted mt-1" style={{ fontSize: "0.85rem" }}>
                    <div><strong>Skills:</strong> {r.skills}</div>
                    {r.experience && <div><strong>Experience:</strong> {r.experience.slice(0, 200)}…</div>}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}