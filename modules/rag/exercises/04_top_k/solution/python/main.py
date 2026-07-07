def main():
    scores=[("a",0.9),("b",0.8),("c",0.1)]
    top=sorted(scores,key=lambda x:-x[1])[:2]
    print(f"TOPK:{len(top)}")
if __name__=="__main__": main()
