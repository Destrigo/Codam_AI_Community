def redact(s):
    return s.replace("sk-secret","[REDACTED]")
def main():
    log=redact("key=sk-secret")
    print("TODO" if "[REDACTED]" in log else "LEAK")
if __name__=="__main__": main()
