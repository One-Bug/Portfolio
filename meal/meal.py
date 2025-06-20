def main():
    time = convert(input("What time is it? ").rstrip().lstrip())
    if time >= 7 and time <= 8:
        print("breakfast time")
    elif time >= 12 and time <= 13:
        print("lunch time")
    elif time >= 18 and time <= 19:
        print("dinner time")
    else: print("Not a meal time")


def convert(time):
    f = time.strip(".amp")
    hours, minutes = f.split(":")
    minutes = float(minutes)/60
    if time.find("p.m") != -1:
        time = float(hours) + 12 + minutes
        return time
    else:
        time = float(hours) + minutes
        return time


if __name__ == "__main__":
    main()
