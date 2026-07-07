def main():
    chunks=["aa","bb"]
    parts=[len(c) for c in chunks]
    print("MAP_REDUCE_OK" if sum(parts)==4 else "FAIL")
if __name__=="__main__": main()
