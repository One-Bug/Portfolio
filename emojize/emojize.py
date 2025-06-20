import emoji


def main():
    emojized = input("Input: ")
    print(f"Output: {emoji.emojize(emojized, language= 'alias')}")


main()
