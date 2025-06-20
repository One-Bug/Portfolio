def main():
    while True:
        try:
            fraction = input("Fraction: ")
            temp = fraction.split('/')
            x = int(temp[0])
            y = int(temp[1])
            result = round((x/y), 2)
            if result > 1:
                continue
            elif result >= 0.9:
                print("F")
            elif result <= 0.01:
                print("E")
            else:
                print(f"{int(result*100)}%")
            break

        except (ValueError, ZeroDivisionError):
            pass


main()
