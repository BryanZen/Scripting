from crypt.rsa import Rsa
from mymath.mymath import hash
import random as rd

msg = 'Top secret message'
rsa = Rsa(rd.randint(500,1000))
print(hash(msg))
c, e = rsa.encrypt(hash(msg))
print(c,e)
print(rsa.decrypt(c, e))
print('Done')
