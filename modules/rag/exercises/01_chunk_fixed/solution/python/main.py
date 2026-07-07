def chunk(text,size=4):
    return [text[i:i+size] for i in range(0,len(text),size)]
def main():
    print(f"CHUNKS:{len(chunk('abcdefghij',4))}")
if __name__=="__main__": main()
