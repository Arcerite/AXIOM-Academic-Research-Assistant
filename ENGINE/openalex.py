# ENGINE/openalex.py

import requests
import time

BASE_URL = "https://api.openalex.org/works"

def search_openalex(query, filters="", per_page=10, retries=3):
    params = {
        "filter": ",".join(
            f for f in [
                f"title.search:{query}",
                f"abstract.search:{query}",
                filters
            ] if f
        ),
        "per-page": per_page
    }

    for attempt in range(retries):
        try:
            r = requests.get(BASE_URL, params=params, timeout=15)
            if r.status_code == 200:
                return r.json().get("results", [])
            if r.status_code >= 500:
                time.sleep(2 ** attempt)
        except requests.RequestException:
            time.sleep(2 ** attempt)

    return []
