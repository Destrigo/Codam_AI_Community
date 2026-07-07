import os

def main() -> None:
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    print(f"MODEL_OK:{model}")

if __name__ == "__main__":
    main()
