import re

def redact_pii(text: str) -> str:
    return re.sub(r"[\w.-]+@[\w.-]+", "[EMAIL]", text)

def main() -> None:
    log = "contact marco@example.com please"
    out = redact_pii(log)
    print("PII_REDACTED" if "[EMAIL]" in out else "LEAK")

if __name__ == "__main__":
    main()
