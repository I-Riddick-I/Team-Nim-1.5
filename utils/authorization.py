import random


def generate_code(length):
    def generator():
        for digit in range(length):
            yield random.randint(0, 9) * pow(10, digit)

    return sum(generator())
