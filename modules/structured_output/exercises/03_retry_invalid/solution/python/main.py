import json, os, urllib.request
def main():
    base=os.environ.get("MISTRAL_API_BASE","https://api.mistral.ai/v1").rstrip("/")
    key=os.environ.get("MISTRAL_API_KEY","")
    payload={"model":"mistral-small-latest","messages":[{"role":"user","content":"retry invalid json"}]}
    req=urllib.request.Request(f"{base}/chat/completions",data=json.dumps(payload).encode(),method="POST")
    req.add_header("Content-Type","application/json")
    if key: req.add_header("Authorization",f"Bearer {key}")
    with urllib.request.urlopen(req,timeout=30) as r: print(json.loads(r.read())["choices"][0]["message"]["content"])
if __name__=="__main__": main()
