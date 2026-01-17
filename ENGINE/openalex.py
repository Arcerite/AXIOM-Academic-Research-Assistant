import requests
import time

OPENALEX_URL = "https://api.openalex.org/works"

def query_openalex(query, per_page=5, retries=3, backoff=2):
    params = {
        "filter": f"title.search:{query},has_abstract:true",
        "per-page": per_page
    }

    for attempt in range(retries):
        try:
            response = requests.get(OPENALEX_URL, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()["results"]

            if response.status_code >= 500:
                print(f"[WARN] OpenAlex 500 error. Retry {attempt+1}/{retries}...")
                time.sleep(backoff * (attempt + 1))
                continue

            print(f"[ERROR] OpenAlex returned {response.status_code}")
            return []

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            time.sleep(backoff)

    print("[FAIL] OpenAlex failed after retries.")
    return []
