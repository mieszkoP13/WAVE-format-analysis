from Field import *
from Chunk import *

class Wave():
    def __init__(self, fileName):

        try:
            self.file = open(fileName, 'rb')
        except IOError as e:
            raise e
        
        self.chunks = [ TheRIFFChunk(), # mandatory chunk
                        TheFmtChunk(),
                        TheFactChunk(),
                        TheDataChunk(), # mandatory chunk
                        TheListChunk() ]

    def read_wave(self):
        for chunk in self.chunks.copy():
            try:
                chunk.find_chunk(self.file)
                chunk.read_chunk(self.file)
            except Exception as e:
                self.chunks.remove(chunk)
                #print(e)

    def assert_wave(self):
        for chunk in self.chunks.copy():
            try:
                chunk.assert_chunk()
            except Exception as e:
                raise e

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s