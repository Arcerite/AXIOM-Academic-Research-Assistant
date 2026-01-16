from ENGINE import prompts,request

def main():
    query = prompts.get_user_prompt()
    papers = request.search_openalex(query)
    request.display_papers(papers)

if __name__ == "__main__":
    main()
