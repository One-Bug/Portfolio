import re
import sys


def main():
    try:
        print(validate(input("IPv4 Address: ")))
    except:
        pass


def validate(ip):
    match = re.search(
        r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$",
        ip,
    )
    if match:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
