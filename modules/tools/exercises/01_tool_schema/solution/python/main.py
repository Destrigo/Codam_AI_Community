def main():
    tool={"name":"calculator","parameters":{"expression":"string"}}
    assert tool["name"]=="calculator"
    print("SCHEMA_OK")
if __name__=="__main__": main()
