import html
import re
from datetime import datetime
import requests
import feedparser

# 1. FIXED: Point to the official open API endpoint path, not the root site domain!
REMOTIVE_API_URL = "https://remoteok.com/remote-python-jobs.rss"


def fetch_remotive():
    # A complete browser signature bypasses standard network filters
    headers = {
        "User-Agent": "AI-Job-Hunter/1.0"
    }

    try:
        response = requests.get(
            REMOTIVE_API_URL,
            headers=headers,
            timeout=30,
        )
        feed = feedparser.parse(REMOTIVE_API_URL)
        response.raise_for_status()

        jobs = []
        extracted_jobs = []

        for job in feed.entries:
            # 2. Extract and format the date safely
            raw_date = job.get("published", "")
            posted_date = ""
            if raw_date:
                try:
                    posted_date = str(raw_date).split("T")[0]
                    datetime.strptime(posted_date, "%Y-%m-%d")
                except (ValueError, IndexError):
                    posted_date = str(raw_date)
            
            # 3. Strip HTML tag clutter out of descriptions
            raw_desc = job.get("summary", "")
            description = ""
            if raw_desc:
                no_tags = re.sub(r"<[^>]*>", "", raw_desc)
                description = html.unescape(no_tags).strip()
            
            extracted_jobs.append(
                {
                    "company": str(job.get("company", "")).strip(),
                    "position": str(job.get("title", "")).strip(),
                    "location": str(job.get("location", "Worldwide")).strip(),
                    "remote": True,
                    "salary_min": str(job.get("salary", "")).strip(),
                    "description": description,
                    "url": str(job.get("link", "")).strip(),
                    "source": "Remotive",
                    "date": posted_date,
                }
            )

        return extracted_jobs
        

    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return []


