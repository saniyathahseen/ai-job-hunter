from app.scrapers.remote_ok import fetch_jobs,filter_python_jobs

jobs = fetch_jobs()

python_jobs = filter_python_jobs(jobs)

print(len(python_jobs))

print(f"Found {len(python_jobs)} jobs")

print(python_jobs[0])