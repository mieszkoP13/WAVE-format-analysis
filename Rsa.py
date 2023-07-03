
class Rsa:
    def __init__(self, key_size=512, block_size=16):
        # self.public_key, self.private_key = KeyGenerator(key_size).generateKeys()
        self.key_size = key_size
        self.block_size = block_size
        self.key = b"123secretkey123"
        # note that   len(iv) == block_size   !!!
        self.iv = b'a1aafaag3a2aaa4a'
        self.key_length = len(self.key)

    def pad(self, text):
        padding_length = self.block_size - (len(text) % self.block_size)
        padding = bytes([padding_length]) * padding_length
        return text + padding

    def unpad(self, padded_text):
        padding_length = padded_text[-1]
        return padded_text[:-padding_length]

    def encrypt_ecb(self, plaintext):
        padded_plaintext = self.pad(plaintext)
        encrypted = bytearray()
        for i in range(0, len(padded_plaintext), self.block_size):
            block = padded_plaintext[i:i + self.block_size]
            for j, byte in enumerate(block):
                encrypted_byte = byte ^ self.key[j % self.key_length]
                encrypted.append(encrypted_byte)
        return encrypted

    def decrypt_ecb(self, ciphertext):
        decrypted = bytearray()
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            for j, byte in enumerate(block):
                decrypted_byte = byte ^ self.key[j % self.key_length]
                decrypted.append(decrypted_byte)
        return self.unpad(decrypted)

    def xor_bytes(self,a, b):
        return bytes(x ^ y for x, y in zip(a, b))

    def encrypt_cbc(self,plaintext):
        padded_plaintext = self.pad(plaintext)
        encrypted = bytearray()
        previous_cipher_block = self.iv

        for i in range(0, len(padded_plaintext), self.block_size):
            block = padded_plaintext[i:i + self.block_size]
            xored_block = self.xor_bytes(block, previous_cipher_block)

            for j, byte in enumerate(xored_block):
                encrypted_byte = byte ^ self.key[j % self.key_length]
                encrypted.append(encrypted_byte)

            previous_cipher_block = encrypted[-self.block_size:]

        return encrypted


    def decrypt_cbc(self,ciphertext):
        decrypted = bytearray()
        previous_cipher_block = self.iv

        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]

            for j, byte in enumerate(block):
                decrypted_byte = byte ^ self.key[j % self.key_length]
                decrypted.append(decrypted_byte)

            decrypted[-self.block_size:] = self.xor_bytes(decrypted[-self.block_size:], previous_cipher_block)
            previous_cipher_block = block

        return self.unpad(decrypted)


# class tests

# ff=open('tessst.txt','rb')
# plaintext=ff.read().decode('raw_unicode_escape','backslashreplace')

# rsa = Rsa()

# encrypted = rsa.encrypt_ecb(plaintext.encode('latin1'))

# f=open('tessst_encr.txt','wb')
# f.write(encrypted.decode('latin1','backslashreplace').encode('raw_unicode_escape'))

# fff=open('tessst_encr.txt','rb')
# ciph=fff.read().decode('latin1','backslashreplace')

# decrypted = rsa.decrypt_ecb(ciph.encode('raw_unicode_escape'))

# f=open('tessst_decr.txt','wb')
# f.write(decrypted.decode('raw_unicode_escape','backslashreplace').encode('latin1'))

# ######################################################################################
# ######################################################################################

# ff=open('tessst.txt','rb')
# plaintext=ff.read().decode('raw_unicode_escape','backslashreplace')

# rsa = Rsa()

# encrypted = rsa.encrypt_cbc(plaintext.encode('latin1'))

# f=open('tessst_encr.txt','wb')
# f.write(encrypted.decode('latin1','backslashreplace').encode('raw_unicode_escape'))

# fff=open('tessst_encr.txt','rb')
# ciph=fff.read().decode('latin1','backslashreplace')

# decrypted = rsa.decrypt_cbc(ciph.encode('raw_unicode_escape'))

# f=open('tessst_decr.txt','wb')
# f.write(decrypted.decode('raw_unicode_escape','backslashreplace').encode('latin1'))