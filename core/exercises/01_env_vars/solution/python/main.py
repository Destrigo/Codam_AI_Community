"""Exercise 01 — Environment variables."""

import os


def main() -> None:
    value = os.environ.get("APP_NAME")
    if value is None:
        print("APP_NAME=MISSING")
    else:
        print(f"APP_NAME={value}")


if __name__ == "__main__":
    main()
