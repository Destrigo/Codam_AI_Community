import json, os, urllib.request
def main():
    base=os.environ.get("MISTRAL_API_BASE","https://api.mistral.ai/v1").rstrip("/")
    payload={"model":"mistral-embed","input":"test"}
    req=urllib.request.Request(f"{base}/embeddings",data=json.dumps(payload).encode(),method="POST")
    req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req,timeout=30) as r: r.read()
    print("EMBED_SOURCE:mock" if os.environ.get("CODAM_LABS_MOCK") else "EMBED_SOURCE:api")
if __name__=="__main__": main()
