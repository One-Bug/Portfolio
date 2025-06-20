def main():
    list = {}
    while True:
        try:
            item = input().upper()
            if item in list:
                list[item] = list[item] + 1
            else:
                list.update({item : 1})
        except EOFError:
            break

    for i in sorted(list.keys()):
        print(f"{list[i]} " + i)

main()
