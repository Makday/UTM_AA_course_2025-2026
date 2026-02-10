def matrix_mult(a, b):
    """Multiply two 2x2 matrices"""
    return [
        [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
        [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
    ]

def fibonacci(n):
    # Matrix [[0, 1], [1, 1]]
    step = [[0, 1], [1, 1]]
    fib = [[0, 1], [1, 1]]

    while n > 0:
        if (n & 1) != 0:  # Check if bit is set
            fib = matrix_mult(fib, step)
        step = matrix_mult(step, step)
        n >>= 1  # Right shift

    return fib[0][0]