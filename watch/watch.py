import re
import sys


def main():
    try:
        print(parse(input("HTML: ")))
    except:
        pass


def parse(s):
    if match := re.search(
        r'src="((https?)://((?:www\.)?youtube\.com/embed)/(.+))"', s, re.IGNORECASE
    ):
        return f"{match.group(1).replace(match.group(2), "https").replace(match.group(3), "youtu.be")}"


if __name__ == "__main__":
    main()
