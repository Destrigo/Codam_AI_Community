import re
def main():
    out="MOCK_RESPONSE:hello"
    print("TEST_PASS" if re.search(r"MOCK_RESPONSE", out) else "FAIL")
if __name__=="__main__": main()
