from mymath.mymath import gcd, isPrime, pubkExp, prikExp, lcm
import random as rand


class Rsa:
    # initialize to set p, q, and n.
    def __init__(self, x):
        i = x
        primes = []
        while True:
            i += 1
            if i == x + 1001:
                raise ValueError("No prime numbers found in the range [X, X + 1000].")
            if isPrime(i):
                primes.append(i)
            if len(primes) == 2:
                self.p = primes[0]
                self.q = primes[1]
                break
        self.n = self.p * self.q

    # generates a cipher string for a message m
    def encrypt(self, m):
        self.k = lcm(self.p - 1, self.q - 1)
        self.e = pubkExp(self.k)
        return (m ** self.e) % self.n, self.e

    # decrypts a cipher string to get back original message
    def decrypt(self, c, e):
        self.d = prikExp(e, self.k)
        return (c ** self.d) % self.n
