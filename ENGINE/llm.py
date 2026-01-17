import subprocess

MODEL = "llama3.2:3b"

def run_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()
