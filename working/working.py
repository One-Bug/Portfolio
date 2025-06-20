import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    matches = re.search(
        "^(1?[0-9])(?::([0-5][0-9]))? (AM|PM) to (1?[0-9])(:[0-5][0-9])? (AM|PM)$", s
    )
    if matches:
        from_hour = fix(int(matches.group(1)), matches.group(2), matches.group(3))
        to_hour = fix(int(matches.group(4)), matches.group(5), matches.group(6))
        return f"{from_hour} to {to_hour}"
    else:
        raise ValueError


def fix(hh, mm, m):
    if m == "AM":
        if hh == 12:
            hour = "00"
        else:
            if hh < 10:
                hour = f"{hh:02}"
            else:
                hour = f"{hh}"
    else:
        if hh == 12:
            hour = "12"
        else:
            hour = f"{hh+12}"
    if mm == None:
        minutes = f"00"
    else:
        minutes = f"{mm.replace(":","")}"
    return f"{hour}:{minutes}"


if __name__ == "__main__":
    main()
