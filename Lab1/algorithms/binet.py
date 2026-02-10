from decimal import Decimal, getcontext

def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    getcontext().prec = max(100, int(n * 0.21) + 20)
    sqrt5 = Decimal(5).sqrt()
    phi = (1 + sqrt5) / 2
    result = phi ** n / sqrt5
    return int(result + Decimal(0.5))