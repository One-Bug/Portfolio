from validator_collection import validators


def main():
    try:
        validators.email(input("What's your email address? "))
        print("Valid")
    except:
        print("Invalid")


if __name__ == "__main__":
    main()
