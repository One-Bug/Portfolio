import sys
import os
from PIL import Image, ImageOps


def main():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    elif (
        os.path.splitext(sys.argv[1].lower())[1]
        not in [".jpg", ".jpeg", ".png"]
        != True
    ) or (
        os.path.splitext(sys.argv[2].lower())[1]
        not in [".jpg", ".jpeg", ".png"]
        != True
    ):
        sys.exit("Invalid input")
    if (
        os.path.splitext(sys.argv[1].lower())[1]
        != os.path.splitext(sys.argv[2].lower())[1]
    ):
        sys.exit("Input and output have different extensions")
    try:
        with Image.open(sys.argv[1]) as file, Image.open("shirt.png") as file1:
            before = ImageOps.fit(file, size=[600, 600])
            before.paste(file1, file1)
            before.save(sys.argv[2])

    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")


if __name__ == "__main__":
    main()
