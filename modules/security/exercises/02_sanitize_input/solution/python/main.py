def sanitize(text: str) -> str:
    t = text
    for bad in ("ignore instructions", "system:"):
        t = t.replace(bad, "")
    return t.strip()

def main() -> None:
    user = "hello system: ignore instructions world"
    print(f"SANITIZED_OK:{sanitize(user)}")

if __name__ == "__main__":
    main()
