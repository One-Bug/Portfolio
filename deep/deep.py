def main():
    answer(input("What is the Answer to the Great Question of Life, the Universe, and Everything?").lower().lstrip().rstrip())


def answer(a):
    match a:
        case "42" | "forty-two" | "forty two":
            print("Yes")
        case _:
            print("No")


main()
