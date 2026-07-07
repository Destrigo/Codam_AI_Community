import math
def sim(a,b):
    return sum(x*y for x,y in zip(a,b))
def main():
    q=[1.0,0.0]; docs={"doc_a":[1.0,0.0],"doc_b":[0.0,1.0]}
    best=max(docs,key=lambda k: sim(q,docs[k]))
    print(f"TOP1:{best}")
if __name__=="__main__": main()
