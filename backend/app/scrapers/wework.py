import html
from datetime import datetime
import re
import xml.etree.ElementTree as ET
import requests

WEWORK_REMOTELY_RSS = "https://weworkremotely.com/remote-jobs.rss"


def fetch_wework():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(
            WEWORK_REMOTELY_RSS,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        jobs = []

        for item in root.findall(".//item"):
            title_element = item.find("title")
            link_element = item.find("link")

            if title_element is None or link_element is None:
                continue

            raw_title = title_element.text or ""
            job_url = link_element.text or ""

            # 1. Parse Company & Title (WWR format: "Company: Position")
            company, _, title = (
                raw_title.partition(":")
                if ":" in raw_title
                else ("", "", raw_title)
            )

            # 2. Extract Location (WWR stores this in <category> tags)
            category_element = item.find("category")
            location = (
                category_element.text.strip()
                if category_element is not None and category_element.text
                else "Worldwide"
            )

            # 3. Clean Description Text (Remove HTML tags and clean up codes)
            desc_element = item.find("description")
            description = ""
            if desc_element is not None and desc_element.text:
                no_tags = re.sub(r"<[^>]*>", "", desc_element.text)
                description = html.unescape(no_tags).strip()

            # 4. Standardize Posted Date (Converts RSS format to YYYY-MM-DD)
            pub_date_element = item.find("pubDate")
            posted_date = ""
            if pub_date_element is not None and pub_date_element.text:
                try:
                    # Clean up string text padding around the date
                    date_str = pub_date_element.text.strip()
                    # Strip out trailing text timezone labels if present (e.g. GMT / +0000)
                    date_clean = re.sub(r"\s+[A-Z]{3,4}$|\s+\+\d{4}$", "", date_str)
                    parsed_date = datetime.strptime(
                        date_clean, "%a, %d %b %Y %H:%M:%S"
                    )
                    posted_date = parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    posted_date = pub_date_element.text.strip()

            # 5. Build and append the exact schema payload
            jobs.append(
                {
                    "company": company.strip() or "Unknown",
                    "position": title.strip(),
                    "location": location,
                    "remote": True,
                    "salary_min": "",  # WWR RSS feeds do not expose structured minimum salary values
                    "description": description,
                    "url": job_url.strip(),
                    "source": "WeWorkRemotely",
                    "date": posted_date,
                }
            )
        return jobs

    except requests.exceptions.RequestException as e:
        print(f"Network request failed: {e}")
        return []
    except ET.ParseError as e:
        print(f"XML Parsing failed: {e}")
        return []