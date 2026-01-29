from ENGINE.api_keys import GROQ
from groq import Groq

client = Groq(api_key=GROQ)
MODEL = "llama-3.1-8b-instant"
MAX_ABSTRACT_CHARS = 8000  # safety limit

def summarize_abstracts(papers):
    """
    Summarizes a list of normalized papers using Groq.
    Returns a summary string. Handles errors gracefully.
    """
    abstracts = [
        p["abstract"] for p in papers
        if p.get("abstract")
    ]

    if not abstracts:
        return "No abstracts available to summarize."

    combined = "\n\n".join(abstracts)[:MAX_ABSTRACT_CHARS]

    prompt = f"""
You are a research assistant.

Summarize the following academic abstracts into:
- A concise overview
- Key themes
- Notable findings

Avoid speculation. Be factual.

ABSTRACTS:
{combined}
"""

    # Try/except wrapper to handle errors gracefully
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You summarize academic research clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        summary = response.choices[0].message.content.strip() # type: ignore
        return summary

    except Exception as e:
        # Catch Groq errors: rate limits, quota, network issues
        error_msg = str(e)
        print("\n⚠️ Groq summarization failed:", error_msg)
        print("The summary could not be generated. Returning raw abstracts instead.\n")

        # Return a truncated version of combined abstracts as fallback
        fallback_preview = combined[:1000]
        if len(combined) > 1000:
            fallback_preview += "..."
        return f"[Fallback: Groq summary failed]\n{fallback_preview}"
