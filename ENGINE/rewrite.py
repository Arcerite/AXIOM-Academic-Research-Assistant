import ENGINE.llm as llm
def rewrite_query(original_query: str) -> str:
    with open(f"RESOURCES/query_rewrite.txt") as f:
        template = f.read()
        prompt = template.format(original_query=original_query)
        return llm.run_llm(prompt)