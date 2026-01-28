import os,time
from ENGINE import search_controller,ai_sum

def clear_screen():
    # Clear terminal screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')


def view_info(papers):
    # Display paper information, abstracts truncated to 500 chars
    for paper in papers:  # no [0] here
        if paper.get("title"):
            print(f"\nTitle: {paper['title']}")
        if paper.get("authors"):
            print(f"Authors: {', '.join(paper['authors'])}")
        if paper.get("year"):
            print(f"Year: {paper['year']}")
        if paper.get("doi"):
            print(f"DOI: {paper['doi']}")
        if paper.get("abstract"):
            print(f"Abstract: {paper['abstract'][:500]}...")
        print("-" * 40)


def menu():
    print("-----------------------------------------")
    print("Axiom, your research assistant")
    print("-----------------------------------------")
    print("1. Search for research papers")
    print("2: Change Filters")  
    print("3. Exit")
    print("-----------------------------------------")

    print("\nSelect an option (1-3): \n")
    input_choice = input(":").strip()
    if input_choice not in ['1', '2', '3']:
        clear_screen()
        print("Invalid choice. Please select 1, 2, or 3.")
        return menu()
    return input_choice


def search():
    clear_screen()
    query = input("Enter your research query: ").strip()
    print("Refined Query:\n", query)
    
    # Get papers
    papers = search_controller.search(query)
    
    # If it's a tuple, unwrap it
    if isinstance(papers, tuple):
        papers = papers[0]
    
    # Only keep dicts
    papers = [p for p in papers if isinstance(p, dict)]
    
    if not papers:
        print("No papers found.")
        input("\nPress Enter to return to main menu...")
        return

    # Summarize papers
    start_time = time.time()
    summary, confidence = ai_sum.summarize_papers_in_chunks(papers)
    end_time = time.time()
    print("\nFinal Summary:\n", summary)
    print("\nConfidence Level:", confidence)
    print(f"\nProcessing Time: {end_time - start_time:.2f} seconds")

    # Show paper info
    print("Would you like to see the papers? (yes/no)")
    if input().strip().lower() in ["yes", "y"]:
        view_info(papers)

    input("\nPress Enter to return to main menu...")

def filters():
    clear_screen()
    print("Filter settings are not implemented yet.")

if __name__ == "__main__":
    while True:
        clear_screen()
        choice = menu()
        if choice == '1':
            search()
        elif choice == '2':
            filters()
        elif choice == '3':
            print("Exiting Axiom. Goodbye!")
            break