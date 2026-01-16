from ENGINE.llm import run_llm

# Max number of abstracts per chunk to avoid context overflow
CHUNK_SIZE = 5  

def summarize_abstracts(papers: list[dict]) -> str:
    """
    Summarize multiple paper abstracts using an LLM, adding numbered citations.

    Args:
        papers: List of paper dicts from search_openalex().

    Returns:
        A single summary string.
    """
    # Filter abstracts
    abstracts = [p["abstract"] for p in papers if p.get("abstract")]
    if not abstracts:
        return "No abstracts found to summarize."

    # Number the abstracts for citation
    numbered_abstracts = [
        f"[{i+1}] {abstract}" for i, abstract in enumerate(abstracts)
    ]

    # Chunking abstracts to avoid token overflow
    chunks = [
        numbered_abstracts[i:i + CHUNK_SIZE]
        for i in range(0, len(numbered_abstracts), CHUNK_SIZE)
    ]

    chunk_summaries = []

    # Summarize each chunk
    for idx, chunk in enumerate(chunks):
        chunk_text = "\n\n".join(chunk)
        prompt = f"""
You are a scientific summarization assistant.

Using ONLY the following abstracts, summarize the main findings, insights, or consensus in a clear and concise way.

Rules:
- Do not speculate beyond the abstracts
- Keep numbered citations ([1], [2], etc.)
- If abstracts disagree, note the disagreement
- Provide a confidence estimate (0-100%) based on the number and clarity of abstracts
- Output in plain English

Abstracts:
{chunk_text}

Summary:
"""
        summary = run_llm(prompt)
        chunk_summaries.append(summary.strip())

    # Combine summaries of all chunks into one final summary
    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    # Otherwise, summarize the chunk summaries
    combined_prompt = f"""
You are a scientific summarization assistant.

The following are intermediate summaries of multiple abstracts. 
Combine them into a single concise summary, keeping numbered citations and confidence estimates.

Intermediate Summaries:
{"\n\n".join(chunk_summaries)}

Final Summary:
"""
    final_summary = run_llm(combined_prompt)
    return final_summary.strip()
