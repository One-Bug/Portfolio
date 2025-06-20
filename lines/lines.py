import sys


def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    elif sys.argv[1].endswith(".py") != True:
        sys.exit("Not a Python file")
    try:
        with open(sys.argv[1]) as file:
            lines = file.readlines()
            counter = 0
            for line in lines:
                line = line.lstrip().rstrip()
                if line.startswith("#") or (line == ""):
                    continue
                else:
                    counter += 1
            print(counter)
    except FileNotFoundError:
        sys.exit("File does not exist")


if __name__ == "__main__":
    main()
