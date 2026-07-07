def main() -> None:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize this policy."},
    ]
    print(f"BOUNDARY_OK:{len(messages)}")

if __name__ == "__main__":
    main()
