import { Routes, Route, NavLink } from "react-router-dom";
import JobsPage from "./pages/JobsPage";
import ApplicationsPage from "./pages/ApplicationsPage";
import ResumesPage from "./pages/ResumesPage";
import MatchPage from "./pages/MatchPage";

export default function App() {
  return (
    <div className="app">
      <nav className="nav">
        <div className="nav-brand">🤖 AI Job Hunter</div>
        <div className="nav-links">
          <NavLink to="/" end>Jobs</NavLink>
          <NavLink to="/applications">Applications</NavLink>
          <NavLink to="/resumes">Resumes</NavLink>
          <NavLink to="/match">Match & Cover Letter</NavLink>
        </div>
      </nav>
      <main className="main">
        <Routes>
          <Route path="/" element={<JobsPage />} />
          <Route path="/applications" element={<ApplicationsPage />} />
          <Route path="/resumes" element={<ResumesPage />} />
          <Route path="/match" element={<MatchPage />} />
        </Routes>
      </main>
    </div>
  );
}