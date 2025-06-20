def main():
    interpreter(input("Expression: ").rstrip().lstrip())


def interpreter(e):
    x, y, z = e.split(" ")
    match y:
        case "+":
            print(float(x) + float(z))
        case "-":
            print(float(x) - float(z))
        case "/":
            print(float(x) / float(z))
        case "*":
            print(float(x) * float(z))


main()
