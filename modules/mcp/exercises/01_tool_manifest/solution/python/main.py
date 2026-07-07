import json

MANIFEST = {"tools": [{"name": "search"}, {"name": "calculator"}]}

def main() -> None:
    tools = MANIFEST["tools"]
    names = [t["name"] for t in tools]
    if "search" in names:
        print(f"MANIFEST_OK:{len(tools)}")

if __name__ == "__main__":
    main()
