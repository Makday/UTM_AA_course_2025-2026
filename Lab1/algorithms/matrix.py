def matrix_mult(a, b):
    """Multiply two 2x2 matrices"""
    return [
        [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
        [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
    ]

def fibonacci(n):
    F = [[0, 1],
         [1, 1]]

    M = [[0, 1],
         [1, 1]]

    if(n == 0):
        return 0

    for i in range(2, n+1):
        F = matrix_mult(F, M)

    return F[0][1]