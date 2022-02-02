def fib_gen():
    a = 1
    b = 1
    while True:
        yield a
        a = b
        b = a + b


def fibs(n):
    gen = fib_gen()
    for _ in range(n):
        print(next(gen), end=" ")


fibs(10)

