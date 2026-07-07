import json, urllib.request
def main():
    with urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos/1",timeout=15) as r:
        title=json.loads(r.read())["title"]
    print(f"FETCH_OK:{title}")
if __name__=="__main__": main()
