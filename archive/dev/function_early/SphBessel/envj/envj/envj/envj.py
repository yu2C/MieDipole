import math

def envj(n, z):
    n = max(1, abs(n))
    result = 0.5 * math.log10(6.28 * n) - n * math.log10(1.36 * z / n)
    return result

