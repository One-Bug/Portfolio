import inflect

p = inflect.engine()
names = []


def main():
    while True:
        try:
            names.append(input("Name: "))
        except EOFError:
            print("")
            break
    print(f"Adieu, adieu, to {p.join(names)}")


main()
