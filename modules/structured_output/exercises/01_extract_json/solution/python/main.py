def main():
    raw = 'Result: {"label":"positive"}'
    start, end = raw.find("{"), raw.rfind("}")+1
    import json
    data = json.loads(raw[start:end])
    print(f"EXTRACT_OK:{data['label']}")

if __name__ == "__main__": main()
