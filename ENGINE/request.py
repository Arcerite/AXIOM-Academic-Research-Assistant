#Using OpenAlex to get information about academic papers, authors, and institutions, as well as the fixed prompt, we search and collect data

import requests


ABSTRACT_ONLY =True #Set to false to get papers without abstracts too

def search_openalex(query, per_page=5):
    """Search OpenAlex for academic papers matching the query."""

    """OpenAlex API endpoint for works"""
    url = "https://api.openalex.org/works"
    
    # OpenAlex uses a simple GET request with filters
    if ABSTRACT_ONLY:
        params = {
        "filter": f"has_abstract:true,title.search:{query},abstract.search:{query}",
        "per-page": per_page
        }
    else:

        params = {
            "filter": f"title.search:{query},abstract.search:{query}",  # search title and abstract
            "per-page": per_page
        }
    
    # Make the request to OpenAlex
    response = requests.get(url, params=params)
    
    # Check for successful response
    if response.status_code != 200:
        print("Error querying OpenAlex:", response.status_code)
        return []
    
    # Parse the JSON response
    results = response.json()["results"]
    
    # Extract relevant information from results
    papers = []
    # Iterate through results and collect data
    for r in results:
        paper = {
            "title": r.get("title"),
            "abstract": r.get("abstract_inverted_index"),
            "doi": r.get("doi"),
            "url": r.get("id"),
            "authors": [a["author"]["display_name"] for a in r.get("authorships", [])],
            "year": r.get("publication_year")
        }
        # Convert abstract from inverted index to string
        if paper["abstract"]:
            # OpenAlex abstracts are stored as inverted index, convert to words
            # Abstract example: {'word1': [0,2], 'word2':[1], ...}
            abstract_words = [""] * sum(len(v) for v in paper["abstract"].values())
            for word, positions in paper["abstract"].items():
                for pos in positions:
                    abstract_words[pos] = word
            paper["abstract"] = " ".join(abstract_words)
        papers.append(paper)
    
    return papers

def display_papers(papers):
    # Display the collected paper information
    for paper in papers:
        print("Title:", paper["title"])
        print("Year:", paper.get("year"))
        print("DOI:", paper.get("doi"))
        print("Authors:", ", ".join(paper.get("authors", [])))
        
        if paper.get("abstract"):  # check if abstract exists
            print(f"Abstract: {paper['abstract'][:500]}...")
        else:
            print("Abstract: [No abstract available]")
        
        print("-" * 50)


