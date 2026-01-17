import os
from ENGINE import search_controller,response

def clear_screen():
    # Clear terminal screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')


def view_info(papers):
    # Display paper information, abstracts truncated to 500 chars
    for paper in papers[0]:
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
    papers = search_controller.search(query)
    summary = response.summarize_abstracts(papers[0])
    print("\nFinal Summary:\n", summary)
    if papers[0] not in [None, []]:
        print("Would you like to see the papers? (yes/no)")
        if input().strip().lower() == "yes" or input().strip().lower() == "y":
            view_info(papers)

    else: 
        print("No papers found.")

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