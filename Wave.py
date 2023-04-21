from Field import *
from Chunk import *

class Wave():
    chunks = [ TheRIFFChunk(), # mandatory chunk
               TheFmtChunk(),
               TheFactChunk(),
               TheDataChunk(), # mandatory chunk
               TheListChunk() ]

    def read_wave(self,file):
        for chunk in self.chunks.copy():
            try:
                chunk.find_chunk(file)
                chunk.read_chunk(file)
            except Exception as e:
                self.chunks.remove(chunk)
                #print(e)
            

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s