def main():
    while True:
        fraction = input("Fraction: ")
        percentage = convert(fraction)
        print(gauge(percentage))
        break


def convert(fraction):
    temp = fraction.split("/")
    x = int(temp[0])
    y = int(temp[1])
    if y == 0:
        raise ZeroDivisionError
    if x > y:
        raise ValueError
    return round((x / y), 2) * 100


def gauge(percentage):
    if percentage > 100:
        pass
    elif percentage >= 99:
        return "F"
    elif percentage <= 1:
        return "E"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()
