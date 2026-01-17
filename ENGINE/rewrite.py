import ENGINE.llm as llm
def rewrite_query(original_query: str) -> str:
    template="""Rewrite the following question into a short academic search query.
    Do NOT answer the question.
    Remove opinions, fluff, and phrasing.
    Limit to 6–10 words.

    Question:
    {original_query}
    """
    prompt = template.format(original_query=original_query)
    return llm.run_llm(prompt)