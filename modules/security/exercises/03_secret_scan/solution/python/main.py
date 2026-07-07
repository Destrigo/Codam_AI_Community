import re

def main() -> None:
    code = 'api_key = "sk-test123456789"'
    if re.search(r"sk-[A-Za-z0-9_-]+", code):
        print("SECRET_SCAN_OK")

if __name__ == "__main__":
    main()
