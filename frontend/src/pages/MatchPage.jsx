import { useState, useEffect } from "react";
import { getJobs, getResumes, getMatch, generateCoverLetter } from "../api";

export default function MatchPage() {
  const [jobs, setJobs] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [jobId, setJobId] = useState("");
  const [resumeId, setResumeId] = useState("");
  const [match, setMatch] = useState(null);
  const [coverLetter, setCoverLetter] = useState("");
  const [loading, setLoading] = useState(false);
  const [genLetter, setGenLetter] = useState(false);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    Promise.all([loadJobs(), loadResumes()]);
  }, []);

  async function loadJobs() {
    try {
      setJobs(await getJobs());
    } catch (_) {}
  }

  async function loadResumes() {
    try {
      setResumes(await getResumes());
    } catch (_) {}
  }

  async function handleMatch() {
    if (!jobId || !resumeId) return;
    try {
      setLoading(true);
      setMatch(null);
      setCoverLetter("");
      const result = await getMatch(Number(jobId), Number(resumeId));
      setMatch(result);
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  }

  async function handleCoverLetter() {
    if (!jobId || !resumeId) return;
    try {
      setGenLetter(true);
      const result = await generateCoverLetter({ job_id: Number(jobId), resume_id: Number(resumeId), tone: "professional" });
      setCoverLetter(result.cover_letter);
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setGenLetter(false);
    }
  }

  const scoreClass = match
    ? match.match_score >= 0.5 ? "high" : match.match_score >= 0.25 ? "medium" : "low"
    : "";

  return (
    <div>
      <h1>Match & Cover Letter</h1>

      {msg && <div className={`alert alert-${msg.type}`}>{msg.text}</div>}

      {/* Selection */}
      <div className="card">
        <div className="form-row">
          <div className="form-group">
            <label>Job</label>
            <select value={jobId} onChange={(e) => setJobId(e.target.value)}>
              <option value="">— Select a job —</option>
              {jobs.map((j) => (
                <option key={j.id} value={j.id}>{j.company} — {j.title}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Resume</label>
            <select value={resumeId} onChange={(e) => setResumeId(e.target.value)}>
              <option value="">— Select a resume —</option>
              {resumes.map((r) => (
                <option key={r.id} value={r.id}>{r.name} ({r.skills.split(",").length} skills)</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex gap-1">
          <button className="btn btn-primary" onClick={handleMatch} disabled={loading || !jobId || !resumeId}>
            {loading ? "Matching…" : "📊 Compute Match"}
          </button>
          <button className="btn btn-success" onClick={handleCoverLetter} disabled={genLetter || !jobId || !resumeId}>
            {genLetter ? "Generating…" : "✍️ Generate Cover Letter"}
          </button>
        </div>
      </div>

      {/* Match Result */}
      {match && (
        <div className="card">
          <h2>Match Result</h2>
          <div className="flex-between">
            <div>
              <strong>{match.job_title}</strong> @ {match.company}
            </div>
            <div>
              <span className="badge" style={{
                background: match.match_score >= 0.5 ? "#d1fae5" : match.match_score >= 0.25 ? "#fef3c7" : "#fee2e2",
                color: match.match_score >= 0.5 ? "#065f46" : match.match_score >= 0.25 ? "#92400e" : "#991b1b",
                fontSize: "1rem",
                padding: "0.3rem 0.8rem",
              }}>
                {Math.round(match.match_score * 100)}% Match
              </span>
            </div>
          </div>
          <div className="score-bar">
            <div className={`score-fill ${scoreClass}`} style={{ width: `${Math.round(match.match_score * 100)}%` }} />
          </div>
          <div className="form-row mt-1">
            <div>
              <h3>✅ Matched Skills ({match.matched_skills.length})</h3>
              <div className="flex gap-1" style={{ flexWrap: "wrap", marginTop: "0.4rem" }}>
                {match.matched_skills.map((s) => (
                  <span key={s} className="badge badge-green">{s}</span>
                ))}
                {match.matched_skills.length === 0 && <span className="text-muted">None</span>}
              </div>
            </div>
            <div>
              <h3>❌ Missing Skills ({match.missing_skills.length})</h3>
              <div className="flex gap-1" style={{ flexWrap: "wrap", marginTop: "0.4rem" }}>
                {match.missing_skills.map((s) => (
                  <span key={s} className="badge badge-red">{s}</span>
                ))}
                {match.missing_skills.length === 0 && <span className="text-muted">None</span>}
              </div>
            </div>
          </div>
          <p className="text-muted mt-1">Total skills detected in job: {match.total_required_skills}</p>
        </div>
      )}

      {/* Cover Letter */}
      {coverLetter && (
        <div className="card">
          <h2>Cover Letter</h2>
          <div className="cover-letter">{coverLetter}</div>
        </div>
      )}
    </div>
  );
}