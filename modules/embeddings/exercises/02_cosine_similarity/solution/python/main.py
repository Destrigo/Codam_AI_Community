import math
def cosine(a,b):
    dot=sum(x*y for x,y in zip(a,b))
    na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
    return dot/(na*nb)
def main():
    print(f"SIMILARITY:{cosine([1,0,0],[1,0,0]):.1f}")
if __name__=="__main__": main()
