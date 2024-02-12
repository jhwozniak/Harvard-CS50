class Jar():
    def __init__(self, capacity=12, size=0):
        if capacity < 0:
            raise ValueError("Work with positive numbers only.")
        self.capacity = capacity
        self.size = size

    def __str__(self):
        return "🍪" * self.size

    #adds n cookies to the jar
    def deposit(self, n):
        if self._size + n > self._capacity:
            raise ValueError("Deposit exceeds capacity.")
        self._size += n

    #withdraws n cookies from the jar
    def withdraw(self, n):
        if self._size - n < 0:
            raise ValueError("Withdrawal exceeds actual size.")
        self._size -= n

    #getter for capacity
    @property
    def capacity(self):
        return self._capacity

    #getter for size
    @property
    def size(self):
        return self._size

    #setter for capacity
    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity

    #setter for size
    @size.setter
    def size(self, size):
        self._size = size


def main():
    jar = Jar()
    print(str(jar.capacity))
    jar.deposit(9)
    print(str(jar))
    jar.withdraw(6)
    print(str(jar))
main()

