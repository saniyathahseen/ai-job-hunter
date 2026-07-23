const API_BASE = "/api/v1";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ── Jobs ──────────────────────────────────────────────────────
export const getJobs = (skip = 0, limit = 20) =>
  request(`/jobs/?skip=${skip}&limit=${limit}`);

export const syncJobs = () =>
  request("/jobs/sync", { method: "POST" });

// ── Applications ──────────────────────────────────────────────
export const getApplications = (skip = 0, limit = 20) =>
  request(`/applications/?skip=${skip}&limit=${limit}`);

export const createApplication = (data) =>
  request("/applications/", { method: "POST", body: JSON.stringify(data) });

export const updateApplicationStatus = (id, status) =>
  request(`/applications/${id}/status?status=${encodeURIComponent(status)}`, {
    method: "PATCH",
  });

// ── Resumes ───────────────────────────────────────────────────
export const getResumes = (skip = 0, limit = 20) =>
  request(`/resumes/?skip=${skip}&limit=${limit}`);

export const getResume = (id) => request(`/resumes/${id}`);

export const createResume = (data) =>
  request("/resumes/", { method: "POST", body: JSON.stringify(data) });

export const updateResume = (id, data) =>
  request(`/resumes/${id}`, { method: "PUT", body: JSON.stringify(data) });

export const deleteResume = (id) =>
  request(`/resumes/${id}`, { method: "DELETE" });

// ── Matching & Cover Letter ───────────────────────────────────
export const getMatch = (jobId, resumeId) =>
  request(`/matching/match/${jobId}/${resumeId}`);

export const generateCoverLetter = (data) =>
  request("/matching/cover-letter", {
    method: "POST",
    body: JSON.stringify(data),
  });