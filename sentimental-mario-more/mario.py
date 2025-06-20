from cs50 import get_int

height = 0
while height < 1 or height > 8:
    height = get_int("Heigth:")
for i in range(height):
    for j in range(height-(i+1)):
        print(" ", end="")
    for k in range(i+1):
        print("#", end="")
    print("  ", end="")
    for l in range(i+1):
        print("#", end="")
    print()
