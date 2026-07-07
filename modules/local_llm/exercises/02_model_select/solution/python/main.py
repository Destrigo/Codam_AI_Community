import os
def main():
    print(f"MODEL:{os.environ.get('MISTRAL_MODEL','mistral-small-latest')}")
if __name__=="__main__": main()
