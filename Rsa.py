import sympy
import os
from KeyGenerator import KeyGenerator
import rsa

class Rsa:
    def __init__(self, key_size=128):
        self.public_key, self.private_key = KeyGenerator(key_size).generate_keys()
        self.key_size = key_size
        self.block_size = (self.public_key[1].bit_length() - 1) // 8
        # note that   len(iv) == block_size   !!!
        self.iv = os.urandom((self.public_key[1].bit_length() - 1) // 8)

    def pad(self, text, block_size):
        padding_size = block_size - (len(text) % block_size)
        padding = bytes([padding_size] * padding_size)
        return text + padding

    def unpad(self, padded_text):
        padding_size = padded_text[-1]
        return padded_text[:-padding_size]

    def split_text(self, text, block_size):
        return [text[i : i + block_size] for i in range(0, len(text), block_size)]

    def bytes_to_int(self, b):
        return int.from_bytes(b, byteorder='big')

    def int_to_bytes(self, i, block_size):
        return i.to_bytes(block_size, byteorder='big')

    def encrypt_block(self, block):
        return pow(self.bytes_to_int(block), self.public_key[0], self.public_key[1])

    def decrypt_block(self, block):
        return self.int_to_bytes(pow(block, self.private_key[0], self.private_key[1]), self.block_size)

    def encrypt_ecb(self, plaintext):
        padded_text = self.pad(plaintext.encode('latin1'), self.block_size)
        blocks = self.split_text(padded_text, self.block_size)

        ciphertext_blocks = []
        for block in blocks:
            if self.bytes_to_int(block) >= self.public_key[1]:
                raise ValueError("Plaintext block too large for RSA key size")
            ciphertext_blocks.append(self.encrypt_block(block))

        ciphertext = b''.join(self.int_to_bytes(block, self.block_size + 1) for block in ciphertext_blocks)
        return ciphertext

    def decrypt_ecb(self, ciphertext):
        blocks = self.split_text(ciphertext, self.block_size + 1)

        plaintext_blocks = []
        for block in blocks:
            plaintext_blocks.append(self.decrypt_block(self.bytes_to_int(block)))

        padded_text = b''.join(plaintext_blocks)
        plaintext = self.unpad(padded_text)

        return plaintext.decode('latin1')  

    def encrypt_cbc(self, plaintext):
        padded_text = self.pad(plaintext.encode('latin1'), self.block_size)
        blocks = self.split_text(padded_text, self.block_size)

        ciphertext_blocks = []
        previous_block = self.iv
        for block in blocks:

            if(type(previous_block) == int):
                previous_block = self.int_to_bytes(previous_block, self.block_size + 1)
            
            xored_block = self.xor_bytes(block, previous_block)
            encrypted_block = self.encrypt_block(xored_block)
            ciphertext_blocks.append(encrypted_block)
            previous_block = encrypted_block

        ciphertext = b''.join(self.int_to_bytes(block, self.block_size + 1) for block in ciphertext_blocks)
        return ciphertext

    def decrypt_cbc(self, ciphertext):
        blocks = self.split_text(ciphertext, self.block_size + 1)

        plaintext_blocks = []
        previous_block = self.iv
        for block in blocks:

            if(type(previous_block) == int):
                previous_block = self.int_to_bytes(previous_block, self.block_size + 1)

            decrypted_block = self.decrypt_block(self.bytes_to_int(block))
            xored_block = self.xor_bytes(decrypted_block, previous_block)
            plaintext_blocks.append(xored_block)
            previous_block = self.bytes_to_int(block)

        padded_text = b''.join(plaintext_blocks)
        plaintext = self.unpad(padded_text)

        return plaintext.decode('latin1')

    def xor_bytes(self, a, b):
        return bytes(x ^ y for x, y in zip(a, b))