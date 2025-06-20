import sys
from tabulate import tabulate
import csv


def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    elif sys.argv[1].endswith(".csv") != True:
        sys.exit("Not a CSV file")
    try:
        with open(sys.argv[1]) as file:
            menu = []
            rows = csv.DictReader(file)
            for row in rows:
                menu.append(row)
            print(tabulate(menu, headers="keys", tablefmt="grid"))
    except FileNotFoundError:
        sys.exit("File does not exist")


if __name__ == "__main__":
    main()
