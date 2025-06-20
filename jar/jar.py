class Jar:
    def __init__(self, capacity=12):
        if capacity > 0:
            self.capacity = capacity
            self.size = 0
        else:
            raise (ValueError)

    def __str__(self):
        cookies = ""
        for _ in range(self.size):
            cookies += "🍪"
        return cookies

    def deposit(self, n):
        if (self.size + n) <= self.capacity:
            self.size += n
        else:
            raise (ValueError)

    def withdraw(self, n):
        if n <= self.size:
            self.size -= n
        else:
            raise (ValueError)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity=12):
        self._capacity = capacity

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size


def main():
    jar = Jar()
    print(jar.capacity)


if __name__ == "__main__":
    main()
