from cs50 import get_int


def main():
    card = get_int("Number: ")
    digits = valid(card)
    valid2(card, digits)
    typeC(card, digits)


def valid(c):
    digits = 0
    while c != 0:
        c //= 10
        digits += 1
    if digits < 13:
        print("INVALID")
        exit(0)
    return digits


def valid2(c, d):
    val = 0
    for i in range(d // 2):
        temp = (c // pow(10, 1+2 * i))
        temp = temp % 10
        temp = temp * 2
        if temp >= 10:
            val = val + (temp % 10) + (temp // 10 % 10)
        else:
            val = val + temp
    if d % 2 == 1:
        for i in range((d // 2)+1):
            temp = (c // pow(10, 2*i))
            temp = temp % 10
            val = val + temp
    else:
        for i in range(d // 2):
            temp = (c // pow(10, 2*i))
            temp = temp % 10
            val = val+temp
    if val % 10 != 0:
        print("INVALID")
        exit(0)


def typeC(c, d):
    val1 = 0
    val2 = 0
    if (d == 15):
        val1 = c//pow(10, 14)
        val2 = c//pow(10, 13)
        val2 = val2 % 10
        if val1 == 3 and (val2 == 4 or val2 == 7):
            print("AMEX")
        else:
            print("INVALID")
            exit(0)
    if (d == 13):
        val1 = c//pow(10, 12)
        if (val1 == 4):
            print("VISA")
        else:
            print("INVALID")
            exit(0)
    if (d == 16):
        val1 = c // pow(10, 15)
        val2 = c // pow(10, 14)
        val2 = val2 % 10
        if (val1 == 4):
            print("VISA")
        else:
            if val1 == 5 and (val2 in range(1, 6)):
                print("MASTERCARD")
            else:
                print("INVALID")
                exit(0)


main()
