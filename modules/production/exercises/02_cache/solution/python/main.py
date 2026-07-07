cache={}
def get(p):
    if p in cache: return cache[p]
    cache[p]="x"; return "miss"
def main():
    get("p"); r=get("p")
    print("CACHE_HIT" if "p" in cache and len(cache)==1 else "MISS")
if __name__=="__main__": main()
