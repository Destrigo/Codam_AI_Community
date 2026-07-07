import json, os, time, urllib.error, urllib.request
def main():
    base=os.environ.get("MISTRAL_API_BASE","https://api.mistral.ai/v1").rstrip("/")
    url=f"{base}/fail_twice"
    for a in range(3):
        try:
            with urllib.request.urlopen(url,timeout=10) as r: r.read()
            print("TODO"); return
        except urllib.error.HTTPError as e:
            if e.code==503 and a<2: time.sleep(1); continue
            raise
if __name__=="__main__": main()
