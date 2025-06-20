def main():
    print(convert(input("")))


def convert(inp):
    inp = inp.replace(":)", "🙂")
    inp = inp.replace(":(", "🙁")
    return inp


main()
