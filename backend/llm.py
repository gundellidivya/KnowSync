import subprocess

def ask_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "tinyllama"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8", errors="ignore").strip()
