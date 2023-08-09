def factorial(n):
    if n < 0:
        raise ValueError("n Value must be non negative")
    if n == 0 or n == 1:
        return 1
    return n * (factorial(n - 1))

print(factorial(4))