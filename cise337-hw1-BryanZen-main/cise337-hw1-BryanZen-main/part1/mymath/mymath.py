def isPrime(n):
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True
    elif n == 1 | n == 2:
        return True
    else:
        return False


def gcd(a, b):
    if a == 0:
        return b
    return gcd(b % a, a)


def lcm(a, b):
    return int((a / gcd(a, b)) * b)


# Generates public key exponent
def pubkExp(k):
    for i in range(2, k):
        if gcd(i, k) == 1:
            return i
            break


# Generate private key exponent
def prikExp(x, y):
    if x > y:
        a = y
        m = x
    else:
        a = x
        m = y
    for i in range(1, y):
        if (a % m) * (i % m) % m == 1:
            return i
    return -1


# Returns the hash of a string message. Sum of its ascii characters.
def hash(s):
    return sum(bytearray(s, encoding='utf-8'))
