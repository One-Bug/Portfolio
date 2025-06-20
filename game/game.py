from random import randint
import sys


def main():
    level = 0
    guess = 0
    while level <= 0:
        try:
            level = int(input("Level: "))
        except ValueError:
            pass
    n = randint(1, level)
    while True:
        try:
            guess = int(input("Guess: "))
            if guess > 0:
                if guess > n:
                    print("Too large!")
                    continue
                elif guess < n:
                    print("Too small!")
                    continue
                else:
                    sys.exit("Just right!")
            else:
                continue
        except ValueError:
            pass


main()
