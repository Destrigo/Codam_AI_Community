def route(q):
    return "rag" if q.startswith("what") else "chat"
def main():
    print(f"ROUTE:{route('what is RAG')}")
if __name__=="__main__": main()
