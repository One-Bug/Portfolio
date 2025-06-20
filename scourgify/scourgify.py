import sys
import csv


def main():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    elif (sys.argv[1].endswith(".csv") != True) or (
        sys.argv[2].endswith(".csv") != True
    ):
        print(sys.argv[1], sys.argv[2])
        sys.exit("Not a CSV file")
    try:
        with open(sys.argv[1], "r") as file, open(sys.argv[2], "w") as file2:
            rows = csv.DictReader(file)
            newrows = csv.DictWriter(file2, fieldnames=["first", "last", "house"])
            newrows.writeheader()
            for row in rows:
                last, first = row["name"].split(", ")
                newrows.writerow({"first": first, "last": last, "house": row["house"]})

    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")


if __name__ == "__main__":
    main()
