def main():
    plate = input("Plate: ").rstrip().lstrip()
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")
    print()


def is_valid(s):
    if len(s) > 6 or len(s) < 2:
        return False
    else:
        if s[0:2].isalpha() != True:
            return False
        else:
            for i in range(len(s) - 1):
                if s[i].isdigit() and s[i + 1].isalpha():
                    return False
                else:
                    if s[i + 1] == "0":
                        return False
                    else:
                        if s[i].isalnum() != True:
                            return False
        return True


if __name__ == "__main__":
    main()
