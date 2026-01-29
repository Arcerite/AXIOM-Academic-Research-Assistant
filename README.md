BIG DISCLAIMERS:
1 - THIS IS STILL A WIP PROJECT, IT MAY BE BUGGY AND UGLY
2 - THIS WAS MADE WITH AI ASSISTANCE
3 - THIS IS JUST A FUN SIDE PROJECT OF MINE


AXIOM – Academic Research Assistant

AXIOM is a lightweight academic research assistant designed to make discovering and understanding scholarly papers faster and more accessible. It combines semantic academic search with AI-powered summarization to help users explore research topics without manually reading dozens of dense papers.

AXIOM is built as a modular Python application and currently runs as a terminal-based tool, with plans for a graphical interface in future versions.

Features

Semantic Academic Search: Uses OpenAlex’s semantic search to find conceptually related papers, supporting natural-language queries beyond simple keyword matching.

AI-Powered Summarization: Aggregates abstracts from multiple papers to produce concise summaries of the overall research landscape.

Rich Paper Metadata: Extracts title, authors, publication year, and abstracts, with direct links to OpenAlex pages, publisher sites, open-access PDFs, and DOIs.

Robust Error Handling: Gracefully handles API failures and automatically retries temporary server errors.

Project Structure

AXIOM/
├── APP/
│ └── main.py
├── ENGINE/
│ ├── openalex.py
│ ├── search.py
│ ├── normalize.py
│ ├── filters.py
│ └── ai_summary.py
├── README.md
└── requirements.txt

Requirements

Python 3.10+

Internet connection

API keys for OpenAlex (semantic search) and Groq (AI summarization). Keys are not included; users must supply their own.

Setup

Clone the repository:
git clone https://github.com/Arcerite/AXIOM-Academic-Research-Assistant.git

cd AXIOM-Academic-Research-Assistant

Install dependencies:
pip install -r requirements.txt

Add your API keys according to the template provided.

Run the application:
python3 -m APP.main

Roadmap

Graphical user interface (GUI)

Faster and optional background summarization

Advanced filtering controls

Citation export and summary saving

Additional academic data sources

License

MIT License

Disclaimer

AXIOM is intended as a research aid. AI-generated summaries may contain inaccuracies and should not replace reading original academic sources or applying scholarly judgment.

Author

Created by Arcerite – Computer Science & Cybersecurity
