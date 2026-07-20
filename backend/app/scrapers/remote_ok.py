import requests

REMOTE_OK_API = "https://remoteok.com/api"

# "https://remoteok.com/remote-python-jobs.rss"
def fetch_remote_ok():
    headers = {
        "User-Agent": "AI-Job-Hunter/1.0"
    }

    response = requests.get(
        REMOTE_OK_API,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    jobs = response.json()

    # First item contains metadata
    return jobs[1:]

SKILLS = [
    "python",

    "fastapi",

    "flask",

    "postgresql",

    "mongodb",

    "rest",

    "api",
]


def filter_python_jobs(jobs):

    filtered = []

    for job in jobs:

        text = (
            f"{job.get('position','')} "
            f"{job.get('description','')}"
        ).lower()

        if any(keyword in text for keyword in SKILLS):
            filtered.append(job)

    return filtered