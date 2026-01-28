import os,time
from ENGINE import search as Search, filters as Filter
from ENGINE.groq_sum import summarize_abstracts

def clear_screen():
    # Clear terminal screen based on OS
    os.system('cls' if os.name == 'nt' else 'clear')

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
    query = input("Enter your search query: ").strip()

    print("\n🔎 Searching for papers...\n")
    results = Search.search(query)

    if not results:
        print("❌ No results found.")
        input("\nPress Enter to return...")
        return

    print("🧠 Summarizing abstracts...\n")
    summary = summarize_abstracts(results)

    print("=" * 80)
    print("📌 AI Summary")
    print("=" * 80)
    print(summary)
    print("=" * 80 + "\n")

    for idx, work in enumerate(results, start=1):
        print(f"📄 Result {idx}")
        print(f"Title: {work.get('title', 'N/A')}")
        print(f"Year : {work.get('year', 'N/A')}")
        print("-" * 40)

    input("\nPress Enter to return to the menu...")


def filters():
    clear_screen()
    print("Current Active Filters: "+ str(Filter.get_active_filters()))
    print("\nFilter Options:")
    print("1: Has Abstracts")
    print("2: Published After Year")
    print("4: Has DOI")
    print("5: Cited By Count Greater Than")
    print("6: Reset Filters")
    print("7: Return to Main Menu")

    choice = input("Select a filter option (1-7): ").strip()
    if choice == '1':
        print("What Value would you like to set for 'Has Abstracts'? (true/false)")
        value = input(":").strip().lower()
        if value in ['true', 'false']:
            Filter.add_filter(f"has_abstract:{value}")
            print(f"Filter 'Has Abstracts: {value}' added.")
        else:
            print("Invalid value. Please enter 'true' or 'false'.")
    elif choice == '2':
        print("Enter the year (e.g., 2015):")
        year = input(":").strip()
        if year.isdigit():
            Filter.add_filter(f"publication_year:>{year}")
            print(f"Filter 'Published After Year: {year}' added.")
        else:
            print("Invalid year. Please enter a valid number.")
    elif choice == '4':
        print("What Value would you like to set for 'Has DOI'? (true/false)")
        value = input(":").strip().lower()
        if value in ['true', 'false']:
            Filter.add_filter(f"has_doi:{value}")
            print(f"Filter 'Has DOI: {value}' added.")
        else:
            print("Invalid value. Please enter 'true' or 'false'.")
    elif choice == '5':
        print("Enter the minimum cited by count (e.g., 50):")
        count = input(":").strip()
        if count.isdigit():
            Filter.add_filter(f"cited_by_count:>{count}")
            print(f"Filter 'Cited By Count Greater Than: {count}' added.")
        else:
            print("Invalid count. Please enter a valid number.")
    elif choice == '6':
        Filter.reset_filters()
        print("All filters have been reset.")
    elif choice == '7':
        return
    

if __name__ == "__main__":
    Filter.reset_filters()
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