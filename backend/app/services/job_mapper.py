def map_remote_ok(job):

    return {
        "company": job.get("company", ""),

        "title": job.get("position", ""),

        "location": job.get("location", "Worldwide"),

        "remote": True,

        "salary": str(job.get("salary_min", "")),

        "description": job.get("description", ""),

        "apply_url": job.get("url", ""),

        "source": job.get("source", "Remote OK"),

        "posted_date": str(job.get("date", "")),
    }