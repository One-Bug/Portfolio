def main():
    camel = input("camelCase: ").rstrip().lstrip()
    print("snake_case: ", end="")
    for c in camel:
        if c.isupper() == True:
            print("_" + c.lower(), end="")
        else:
            print(c, end="")
    print()


main()
