from datetime import date
import sys
import inflect


inf = inflect.engine()


def main():
    print(minutes(input("Date of Birth: ")))


def minutes(birth):
    try:
        if birth := date.fromisoformat(birth):
            time = date.today() - birth
            return f"{(inf.number_to_words(time.days * 60 * 24, andword = "")).capitalize()} minutes"
    except:
        sys.exit("Inavlid date")


if __name__ == "__main__":
    main()
