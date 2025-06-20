def main():
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    while True:
        try:
            date = input("Date: ").rstrip().lstrip().replace(
                '/', '-').replace('" ', '').replace(' "', '').replace(' ', '-')
            date = date.split('-')
            temp = date[0].title()
            if temp in months:
                if check(date[1]):
                    date[0] = int(months.index(temp)) + 1
                    date[0] = str(date[0])
                    date[1] = date[1].replace(",", "")
                else:
                    continue
            if month(int(date[0])):
                continue
            if day(int(date[1])):
                continue
            print(f"{date[2]}-{date[0].zfill(2)}-{date[1].zfill(2)}")
            break
        except ValueError:
            pass


def month(m):
    if m > 12:
        return True


def day(d):
    if d > 31:
        return True


def check(d):
    try:
        int(d)
        return False
    except ValueError:
        return True


main()
