from Field import *
from Chunk import *
import copy

chunks_ = [ TheRIFFChunk(), # mandatory chunk
            TheFmtChunk(),
            TheFactChunk(),
            TheDataChunk(), # mandatory chunk
            TheListChunk() ]

class Wave():
    def __init__(self, fileName: str):

        try:
            self.file = open(fileName, 'rb')
        except IOError as e:
            raise e
        
        self.chunks = []

    # method to find and read all potential chunks in a file
    def read_wave(self):
        for chunk in chunks_.copy():
            try:
                positions = chunk.find_chunk(self.file)
                for pos in positions:
                    self.file.seek(pos)
                    chunk.read_chunk(self.file)
                    self.chunks.append(copy.deepcopy(chunk))
            except Exception as e:
                pass
                #print(e)

    def assert_wave(self):
        for chunk in self.chunks.copy():
            try:
                chunk.assert_chunk()
            except Exception as e:
                self.chunks.remove(chunk)
                #print(e)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s