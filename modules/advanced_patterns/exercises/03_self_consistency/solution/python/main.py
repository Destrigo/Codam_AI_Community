from collections import Counter
def main():
    votes=Counter(["a","a","b"])
    print(f"VOTE:{votes.most_common(1)[0][1]}")
if __name__=="__main__": main()
