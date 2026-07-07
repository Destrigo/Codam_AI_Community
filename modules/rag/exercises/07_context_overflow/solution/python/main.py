def main():
    chunks=list(range(5))
    selected=chunks[:2]
    print("TRUNCATED_OK" if len(selected)==2 else "FAIL")
if __name__=="__main__": main()
