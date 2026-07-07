import json, os, urllib.request
def main():
    base=os.environ.get("MISTRAL_API_BASE","https://api.mistral.ai/v1").rstrip("/")
    key=os.environ.get("MISTRAL_API_KEY","")
    payload={"model":"mistral-embed","input":"hello"}
    req=urllib.request.Request(f"{base}/embeddings",data=json.dumps(payload).encode(),method="POST")
    req.add_header("Content-Type","application/json")
    if key: req.add_header("Authorization",f"Bearer {key}")
    with urllib.request.urlopen(req,timeout=30) as r:
        vec=json.loads(r.read())["data"][0]["embedding"]
    print(f"EMBED_DIM:{len(vec)}")
if __name__=="__main__": main()
