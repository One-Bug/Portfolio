def main():
    due = 50
    while due > 0:
        print(f"Amount Due: {due}")
        inserted = int(input("Insert Coin: "))
        if inserted in {5, 10, 25, 50}:
            due = due - inserted
    if due <= 0:
        print(f"Change Owed: {due * -1}")


main()
