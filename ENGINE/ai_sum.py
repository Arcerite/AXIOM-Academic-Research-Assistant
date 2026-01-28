from concurrent.futures import ThreadPoolExecutor
from ENGINE.llm import run_llm

MAX_CHARS = 1500 # Safety limit for LLM input
CHUNK_SIZE = 1   # Number of papers per chunk
MAX_WORKERS = 1  # Threads for parallel summarization

# ---------------------------
# Helper: Convert paper to text
# ---------------------------
def paper_to_text(paper, idx):
    """
    Converts a paper into best-available summarizable text with inline citation number.
    """
    if paper.get("abstract"):
        return f"[{idx}] {paper['abstract']}"

    # Fallback: title + concepts
    text_parts = []
    if paper.get("title"):
        text_parts.append(f"[{idx}] TITLE: {paper['title']}")

    concepts = paper.get("concepts", [])
    if concepts:
        concept_names = [c["display_name"] for c in concepts[:5]]
        text_parts.append("CONCEPTS: " + ", ".join(concept_names))

    if text_parts:
        return "\n".join(text_parts)

    # Nothing to summarize
    return None

# ---------------------------
# Helper: Split list into chunks
# ---------------------------
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# ---------------------------
# Build input text for LLM
# ---------------------------
def build_chunk_text(chunk, start_idx=1):
    """
    Converts a list of papers into a single text block for the LLM.
    start_idx allows citations to continue numbering across chunks.
    """
    chunk_texts = []
    for i, paper in enumerate(chunk, start=start_idx):
        text = paper_to_text(paper, i)
        if text:
            chunk_texts.append(text)
    combined = "\n\n---\n\n".join(chunk_texts)
    return combined[:MAX_CHARS]

# ---------------------------
# Confidence scoring
# ---------------------------
def confidence_score(papers):
    total = len(papers)
    if total == 0:
        return "None"

    abstracts = sum(1 for p in papers if p.get("abstract"))
    if abstracts == total:
        return "High (abstract-based sources)"
    elif abstracts > 0:
        return "Medium (partial abstract coverage)"
    else:
        return "Low (metadata-only sources)"

# ---------------------------
# LLM prompt builder
# ---------------------------
def summary_prompt(text):
    return f"""
You are a factual scientific assistant.

Some sources contain full abstracts, others only titles or keywords.

Summarize the main points from these sources.

Instructions:
- Clearly state disagreements between sources
- Include numbered citations ([1], [2], etc.)
- Provide a confidence estimate
- Do not speculate beyond the given text
- Output in plain English

Source material:
{text}

Summary:
"""

# ---------------------------
# Summarize a single chunk (can be run in parallel)
# ---------------------------
def summarize_chunk(chunk, start_idx=1):
    text = build_chunk_text(chunk, start_idx)
    if not text:
        return "No usable data found.", "None"

    prompt = summary_prompt(text)
    summary = run_llm(prompt)
    confidence = confidence_score(chunk)
    return summary.strip(), confidence

# ---------------------------
# Summarize multiple papers in chunks
# ---------------------------
def summarize_papers_in_chunks(papers):
    """
    Main function: summarizing all papers in chunks in parallel.
    Returns combined summary and overall confidence.
    """
    if not papers:
        return "No papers provided.", "None"

    chunks = list(chunk_list(papers, CHUNK_SIZE))
    chunk_summaries = []
    chunk_confidences = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        start_idx = 1
        for chunk in chunks:
            futures.append(executor.submit(summarize_chunk, chunk, start_idx))
            start_idx += len(chunk)

        for f in futures:
            summary, confidence = f.result()
            chunk_summaries.append(summary)
            chunk_confidences.append(confidence)

    # Combine all chunk summaries
    final_summary = "\n\n".join(chunk_summaries)

    # Overall confidence: worst-case
    if all(c.startswith("High") for c in chunk_confidences):
        overall_conf = "High"
    elif any(c.startswith("Medium") for c in chunk_confidences):
        overall_conf = "Medium"
    else:
        overall_conf = "Low"

    return final_summary, overall_conf
