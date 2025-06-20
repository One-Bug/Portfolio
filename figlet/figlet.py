import sys
from pyfiglet import Figlet
from random import choice

f = Figlet()
styles = f.getFonts()


def main():
    arg = ["-f", "--font"]
    if len(sys.argv) == 3:
        if sys.argv[1] not in arg:
            sys.exit("Invalid usage")
        if sys.argv[2] not in styles:
            sys.exit("Invalid usage")
        figlet()
    elif len(sys.argv) == 1:
        figlet()
    else:
        sys.exit("Invalid usage")


def figlet():
    text = input("Input: ")
    if len(sys.argv) == 3:
        f.setFont(font=sys.argv[2])
    else:
        f.setFont(font=choice(styles))
    print(f"Output:\n{f.renderText(text)}")


main()
