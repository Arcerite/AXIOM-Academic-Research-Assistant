from ENGINE.openalex import query_openalex
from ENGINE.rewrite import rewrite_query

MAX_ATTEMPTS = 5
# Function to search for papers with rephrasing attempts
def search(query: str)-> tuple[list[dict], str | None]:
    current_query = query

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n[SEARCH] Attempt {attempt}: '{current_query}'")

        results = query_openalex(current_query)

        if results:
            print(f"[SUCCESS] Found {len(results)} papers.")
            return results, current_query

        print("[INFO] No results found.")

        if attempt < MAX_ATTEMPTS:
            current_query = rewrite_query(query)
            print(f"[REPHRASE] New query → '{current_query}'")

    print("[FAIL] No results after multiple rephrases.")
    return [], None
