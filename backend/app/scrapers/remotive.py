import html
import re
from datetime import datetime
import requests

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs?category=software-dev&limit=100"


def fetch_remotive():
    headers = {
        "User-Agent": "AI-Job-Hunter/1.0"
    }

    try:
        response = requests.get(
            REMOTIVE_API_URL,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        jobs = data.get("jobs", [])
        extracted_jobs = []

        for job in jobs:
            # Extract and format the date safely
            raw_date = job.get("publication_date", "")
            posted_date = ""
            if raw_date:
                try:
                    posted_date = str(raw_date).split("T")[0]
                    datetime.strptime(posted_date, "%Y-%m-%d")
                except (ValueError, IndexError):
                    posted_date = str(raw_date)

            # Strip HTML tag clutter out of descriptions
            raw_desc = job.get("description", "")
            description = ""
            if raw_desc:
                no_tags = re.sub(r"<[^>]*>", "", raw_desc)
                description = html.unescape(no_tags).strip()

            extracted_jobs.append(
                {
                    "company": str(job.get("company_name", "")).strip(),
                    "position": str(job.get("title", "")).strip(),
                    "location": str(job.get("candidate_required_location", "Worldwide")).strip(),
                    "remote": True,
                    "salary_min": str(job.get("salary", "")).strip(),
                    "description": description,
                    "url": str(job.get("url", "")).strip(),
                    "source": "Remotive",
                    "date": posted_date,
                }
            )

        return extracted_jobs

    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return []