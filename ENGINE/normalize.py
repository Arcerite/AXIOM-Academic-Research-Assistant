def inverted_index_to_text(inv_index: dict | None) -> str | None:
    if not inv_index:
        return None

    length = max(
        pos
        for positions in inv_index.values()
        for pos in positions
    ) + 1

    words = [""] * length
    for word, positions in inv_index.items():
        for pos in positions:
            words[pos] = word

    return " ".join(words)


def extract_links(work: dict) -> dict:
    links = {}

    # OpenAlex page
    if work.get("id"):
        links["openalex"] = work["id"]

    # Publisher landing page
    primary = work.get("primary_location") or {}
    if primary.get("landing_page_url"):
        links["publisher"] = primary["landing_page_url"]

    # Open access PDF or page
    oa = work.get("open_access") or {}
    if oa.get("oa_url"):
        links["open_access"] = oa["oa_url"]

    # DOI link
    doi = work.get("doi")
    if doi:
        links["doi"] = f"https://doi.org/{doi.replace('https://doi.org/', '')}"

    return links

def normalize_work(work: dict) -> dict:
    abstract_text = inverted_index_to_text(
        work.get("abstract_inverted_index")
    )

    return {
        "title": work.get("title"),
        "authors": [
            a["author"]["display_name"]
            for a in work.get("authorships", [])
            if a.get("author")
        ],
        "year": work.get("publication_year"),
        "abstract": abstract_text,
        "links": extract_links(work)
    }