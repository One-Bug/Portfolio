import random


def main():
    counter = 0
    score = 0
    level = get_level()
    for x in range(10):
        val1 = generate_integer(level)
        val2 = generate_integer(level)
        while True:
            answer = input(f"{val1} + {val2} = ")
            if answer != str(val1 + val2):
                if counter == 2:
                    counter = 0
                    print(f"{val1} + {val2} = {val1 + val2}")
                    break
                else:
                    print("EEE")
                    counter += 1
                    continue
            else:
                counter = 0
                score += 1
                break
    print(f"Score: {score}")


def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level > 3 or level <= 0:
                continue
            return level
        except ValueError:
            pass


def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(100, 999)


if __name__ == "__main__":
    main()
