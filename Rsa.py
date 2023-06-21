import random

class RSA:

    def __init__(self, block_size: int):
        self.block_size = block_size

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

    def generate_primes(self, min:int, max:int):
        primes = [i for i in range(min,max) if self.is_prime(i)]
        return random.choice(primes), random.choice(primes)
    
    def gcd(self, p, q):
        while q != 0:
            p, q = q, p%q
        return p
    
    def coprime(self, x: int, y: int):
        return self.gcd(x,y) == 1
    
    def generate_rsa_keys(self):
        p, q = self.generate_primes(0,1000)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = random.choice([i for i in range(2,phi_n) if self.coprime(i,phi_n)])
        d = pow(e, -1, phi_n)
        return (e, n), (d, n)
    
    def encrypt_data(self, data, public_key: tuple):
        e, n = public_key
        return [pow(ord(byte), e, n) for byte in data]
    
    def decrypt_data(self, encrypted_data, private_key: tuple):
        d, n = private_key
        return [pow(ord(encrypted_byte), d, n) for encrypted_byte in encrypted_data]
    
    def pad_message(self, message):
        num_pad_chars = self.block_size - (len(message) % self.block_size)
        padding = chr(num_pad_chars) * num_pad_chars
        return message + padding

    def remove_padding(self, padded_message):
        num_pad_chars = ord(padded_message[-1])
        return padded_message[:-num_pad_chars]

    def split_blocks(self, message):
        return [message[i: i+self.block_size] for i in range(0, len(message), self.block_size)]

    def encrypt_ecb(self, plaintext, key):
        padded_plaintext = self.pad_message(plaintext)
        blocks = self.split_blocks(padded_plaintext)
        encrypted_blocks = []

        for block in blocks:
            encrypted_blocks += self.encrypt_data(block,key)

        return ''.join(chr(x) for x in encrypted_blocks)

    def decrypt_ecb(self, ciphertext, key):
        blocks = self.split_blocks(ciphertext)
        decrypted_blocks = []

        for block in blocks:
            decrypted_blocks += self.decrypt_data(block,key)

        padded_plaintext = ''.join(chr(x) for x in decrypted_blocks)
        plaintext = self.remove_padding(padded_plaintext)
        return plaintext
    
    def xor_blocks(self, block1, block2):
        return ''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(block1, block2))

    def encrypt_cbc(self, plaintext, key, iv):
        padded_plaintext = self.pad_message(plaintext)
        blocks = self.split_blocks(padded_plaintext)
        encrypted_blocks = []
        previous_cipher_block = iv

        for block in blocks:
            xored_block = self.xor_blocks(block, previous_cipher_block)
            encrypted_block = self.encrypt_data(xored_block,key)
            previous_cipher_block = ''.join(chr(x) for x in encrypted_block)
            encrypted_blocks += encrypted_block

        return ''.join(chr(x) for x in encrypted_blocks)

    def decrypt_cbc(self, ciphertext, key, iv):
        blocks = self.split_blocks(ciphertext)
        decrypted_blocks = []
        previous_cipher_block = iv

        for block in blocks:
            decrypted_block = self.decrypt_data(block,key)
            blck = ''.join(chr(x) for x in decrypted_block)
            decrypted_blocks += self.xor_blocks(blck, previous_cipher_block)
            previous_cipher_block = block

        padded_plaintext = ''.join(decrypted_blocks)
        plaintext = self.remove_padding(padded_plaintext)
        return plaintext
    
########################################################
# demo
########################################################

rsa = RSA(8)

pub, priv = rsa.generate_rsa_keys()
print("Public key:",pub)
print("Private key:",priv)

########################################################

encrList = rsa.encrypt_data("ellodworld44555555a", pub)
ciphertxt = ''.join(chr(x) for x in encrList)
print("Ciphertext:", ciphertxt)
decrList = rsa.decrypt_data(ciphertxt, priv)
decryptedtxt = ''.join(chr(x) for x in decrList)
print("Decrypted text:", decryptedtxt)

########################################################

ciphertext = rsa.encrypt_ecb("Hellodworld!", pub)
print("Ciphertext ecb:", ciphertext)

decrypted_plaintext = rsa.decrypt_ecb(ciphertext, priv)
print("Decrypted text ecb:", decrypted_plaintext)

########################################################

ciphertext = rsa.encrypt_cbc("Hello, wosdfsdfrld!", pub, "111111113333")
print("Ciphertext:", ciphertext)

decrypted_plaintext = rsa.decrypt_cbc(ciphertext, priv, "111111113333")
print("Decrypted plaintext:", decrypted_plaintext)