from ENGINE import prompts,request, response

def main():
    query = prompts.get_user_prompt()
    print("Refined Query:\n", query)
    papers = request.search_openalex(query)
    request.display_papers(papers)
    summary = response.summarize_abstracts(papers)
    print("\nFinal Summary:\n", summary)
if __name__ == "__main__":
    main()
