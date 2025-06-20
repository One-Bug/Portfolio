def main():
    word = input("Input: ").rstrip().lstrip()
    print("Output: ", end="")
    print(shorten(word))


def shorten(word):
    new = []
    for c in word:
        if c.lower() not in {"a", "e", "i", "o", "u"}:
            new.append(c)
    return "".join(new)


if __name__ == "__main__":
    main()
