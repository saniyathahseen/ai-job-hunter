from app.scrapers.remote_ok import fetch_remote_ok,filter_python_jobs

jobs = fetch_remote_ok()

python_jobs = filter_python_jobs(jobs)

print(len(python_jobs))

print(f"Found {len(python_jobs)} jobs")

print(python_jobs[0])