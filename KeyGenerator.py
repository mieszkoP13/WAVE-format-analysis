import random

class KeyGenerator:
    def __init__(self, keysize):
        self.keysize=keysize
        self.primesize = keysize/2

    def is_prime(self, num):
        if num % 2 == 0 or num < 2:
            return False
        if num == 3:
            return True
        s = num - 1
        t = 0
        while s % 2 == 0:
            s = s // 2
            t += 1
        for trials in range(5): 
            a = random.randrange(2, num - 1)
            v = pow(a, s, num)
            if v != 1: 
                 i = 0
                 while v != (num - 1):
                    if i == t - 1:
                        return False
                    else:
                        i = i + 1
                        v = (v ** 2) % num
        return True

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.egcd(b%a,a)
        return (g, x - (b//a) * y, y)

    def generate_large_prime(self):
        while True:
            num = random.randrange(2**(self.primesize-1), 2**(self.primesize))
            if self.is_prime(num):
                return num
    
    def gcd(self, a, b):
        if b==0: 
            return a 
        else: 
            return self.gcd(b,a%b) 

    def mod_inv(self, a, m):
        if self.gcd(a, m) != 1: # a,m - relatively prime
            return None

        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3 
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def generate_keys(self):
        while True:
            p = 0
            q = 0
            while p == q or ((p-1)*(q-1)).bit_length() != self.keysize:
                p = self.generate_large_prime()
                q = self.generate_large_prime()
        
            phi = (p-1)*(q-1) 
            n = p * q

            while True:
                e = random.randrange(2 ** (self.keysize - 1), 2 ** (self.keysize))
        
                if self.gcd(e, phi) == 1 and e < phi:
                    break
        
            d = self.mod_inv(e,phi)
        
            publicKey=(e,n)
            privateKey=(d,n,e,p,q)

            if e.bit_length() == self.keysize and d.bit_length() == self.keysize:
                return (publicKey, privateKey)