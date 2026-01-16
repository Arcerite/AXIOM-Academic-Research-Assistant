#This file will handle everything from user input, it will parse the input, classify it, and fix prompt to be better for querying the model
from ENGINE import llm

MODEL = "llama3.2:3b"


def get_user_prompt() -> str:
    with open(f"RESOURCES/query_rewrite.txt") as f:
        template = f.read()

    user_input = input("Please enter your research question or topic: ")
    prompt = template.format(question=user_input)
    return refine_query(prompt)

def refine_query(user_question: str) -> str:
    with open(f"RESOURCES/query_rewrite.txt") as f:
        template = f.read()

    prompt = template.format(question=user_question)
    return llm.run_llm(prompt)


if __name__ == "__main__":
    print(get_user_prompt())


