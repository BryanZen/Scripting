import sys, os
sys.path.insert(1, os.path.join(os.getcwd(), 'part1'))
from mymath.mymath import *
from crypt.rsa import Rsa

class TestRSA:
    def test_hash_1(self):
        assert hash('Top secret message') == 1758

    def test_hash_2(self):
        assert hash('Tranfer $5000 to me') == 1488

    def test_hash_3(self):
        assert hash('Rastapopulous send assist right now!') == 3542

    def test_prime_1(self):
        assert isPrime(67)
        assert not isPrime(77)

    def test_prime_2(self):
        assert isPrime(73)
        assert not isPrime(60)

    def test_pkeyExp_1(self):
        assert prikExp(15, 26) == 7

    def test_pkeyExp_2(self):
        assert prikExp(5228, 2061) == 1281

    def test_pkeyExp_3(self):
        assert prikExp(821, 9981) == 851

    def test_pkeyExp_4(self):
        assert prikExp(119919, 998777) == 966578

    def test_pkeyExp_5(self):
        assert prikExp(424, 32412) == -1

    def test_pkeyExp_6(self):
        assert prikExp(29, 29) == -1

    def test_pubkExp_1(self):
        assert gcd(pubkExp(15908), 15908) == 1

    def test_pubkExp_2(self):
        assert gcd(pubkExp(25), 25) == 1

    def test_pubkExp_3(self):
        assert gcd(pubkExp(999991), 999991) == 1

    def test_lcm_1(self):
        assert lcm(999,991) == 990009

    def test_lcm_2(self):
        assert lcm(382,8261) == 3155702


    def test_rsa_1(self):
        msg = 'Top secret message'
        rsa = Rsa(728)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)

    def test_rsa_2(self):
        msg = 'Tranfer $5000 to ME!'
        rsa = Rsa(99)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)

    def test_rsa_3(self):
        msg = 'Encryption is fun!'
        rsa = Rsa(2029)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)

    def test_rsa_4(self):
        msg = 'Seawolves! Rise and shine.'
        rsa = Rsa(911)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)


    def test_rsa_6(self):
        msg = 'You know who is here! Run'
        rsa = Rsa(628)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)

    def test_rsa_7(self):
        msg = 'You know who is here! Run'
        rsa = Rsa(5738)
        c, e = rsa.encrypt(hash(msg))
        assert rsa.decrypt(c, e) == hash(msg)
