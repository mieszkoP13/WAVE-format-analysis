from Field import *
from Chunk import *
from Rsa import Rsa
import copy
import os

class Wave():

    rsa = Rsa()

    POSSIBLE_CHUNKS = [ TheRIFFChunk(), # mandatory chunk
                        TheFormatChunk(), # mandatory chunk
                        TheCueChunk(),
                        TheFactChunk(),
                        TheDataChunk(), # mandatory chunk
                        TheListChunk(),
                        TheInstrumentChunk(),
                        TheSampleChunk() ]

    def __init__(self, fileName: str):
        try:
            self.file = open(fileName, 'rb')
        except IOError as e:
            raise e
        
    chunks = []

    def reset(self, fileName):
        self.__init__(fileName)

    # method to find and read all potential chunks in a file
    def read_wave(self):
        for chunk in self.POSSIBLE_CHUNKS.copy():
            self.file.seek(0)
            try:
                positions = chunk.find_chunk(self.file)
                for pos in positions:
                    self.file.seek(pos)
                    chunk.read_chunk(self.file)
                    self.chunks.append(copy.deepcopy(chunk))
            except Exception as e:
                print(e)

    def create_clean_copy(self):

        originalFileName = f'{self.file.name}'
        newFileNameBase = os.path.splitext(originalFileName)[0] # ./sound-examples/ex1

        newFileName_noMeta = f'{newFileNameBase}_noMeta.wav' # ./sound-examples/ex1_noMeta.wav

        file_noMeta = open(newFileName_noMeta, 'wb')

        for chunk in self.chunks:
            if isinstance(chunk,TheRIFFChunk) or isinstance(chunk,TheFormatChunk) or isinstance(chunk,TheDataChunk):
                chunk.write_chunk(file_noMeta)

    def create_encrypted_copy(self, mode):
        originalFileName = f'{self.file.name}'
        newFileNameBase = os.path.splitext(originalFileName)[0] # ./sound-examples/ex1

        newFileName_encr = f'{newFileNameBase}_encr.wav' # ./sound-examples/ex1_encr.wav

        file_encr = open(newFileName_encr, 'wb')

        for chunk in self.chunks:
            if isinstance(chunk,TheDataChunk):
                chunk.fields[2].encoding = 'raw_unicode_escape'
                if mode == 'ecb':
                    encrypted_data_ebc = self.rsa.encrypt_ecb(chunk.fields[2].data)
                elif mode == 'cbc':
                    encrypted_data_ebc = self.rsa.encrypt_cbc(chunk.fields[2].data)

                chunk.fields[1].data = len(encrypted_data_ebc)
                chunk.fields[2].data = encrypted_data_ebc.decode('latin1','backslashreplace')
                chunk.write_chunk(file_encr)
                chunk.fields[2].encoding = 'latin1'
            else:
                chunk.write_chunk(file_encr)

        self.reset(newFileName_encr)
    
    def create_decrypted_copy(self, mode):
        originalFileName = f'{self.file.name}'
        newFileNameBase = os.path.splitext(originalFileName)[0] # ./sound-examples/ex1

        newFileName_decr = f'{newFileNameBase}_decr.wav' # ./sound-examples/ex1_decr.wav

        file_decr = open(newFileName_decr, 'wb')

        for chunk in self.chunks:
            if isinstance(chunk,TheDataChunk):
                chunk.fields[2].encoding = 'latin1'
                if mode == 'ecb':
                    decrypted_data_ebc = self.rsa.decrypt_ecb(chunk.fields[2].data.encode('raw_unicode_escape'))
                elif mode == 'cbc':
                    decrypted_data_ebc = self.rsa.decrypt_cbc(chunk.fields[2].data.encode('raw_unicode_escape'))

                chunk.fields[1].data = len(decrypted_data_ebc)
                chunk.fields[2].data = decrypted_data_ebc
                chunk.write_chunk(file_decr)
                chunk.fields[2].encoding = 'raw_unicode_escape'
            else:
                chunk.write_chunk(file_decr)

        self.reset(newFileName_decr)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s