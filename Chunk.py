from abc import abstractmethod, ABC
from typing import Type
from Field import *

class Chunk(ABC):
    def __init__(self, chunkName: str, chunkAssertID: str, fields:Type[Field]=None):
        if fields is None:
            self.fields = []

        self.chunkName = chunkName
        self.chunkAssertID = chunkAssertID
        self.fields = fields

    def find_chunk(self,file):
        fileTxt = file.read()
        # finding a postion of a chunk by its ID
        pos = fileTxt.find(f'{self.chunkAssertID}'.encode())

        # if it hasnt been found
        if pos == -1:
            file.seek(0)
            raise Exception("chunk not found")
        
        # if it was found, file cursor is set to that position
        file.seek(pos)

    @abstractmethod
    def read_chunk(self,file):
        pass

    @abstractmethod
    def assert_chunk(self,file):
        pass

    def __str__(self):
        s=f'{self.chunkName}\n'
        for field in self.fields:
            s = s + str(field) + '\n'
        return s
    
    def fieldCount(self):
        return len(self.fields)


class TheRIFFChunk(Chunk):

    def __init__(self):
        super().__init__('The RIFF Chunk','RIFF',[TextField('RIFF Chunk ID',4,'UTF-8','big',True),
                        NumberField('RIFF Chunk Size',4,'UTF-32','little',True),
                        TextField('RIFF type ID',4,'UTF-8','big',True)])
        
    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        file.seek(0)
    
    def assert_chunk(self):
        assert self.fields[0].data == 'RIFF', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
        assert self.fields[2].data == 'WAVE', f'Invalid {self.fields[2].name}'


class TheFmtChunk(Chunk):

    def __init__(self):
        super().__init__('The Fmt Chunk','fmt ', [TextField('Fmt Chunk ID',4,'UTF-8','big',True),
        NumberField('Fmt Chunk Size',4,'UTF-8','little',True),
        NumberField('Audio Format',2,'UTF-8','little',True),
        NumberField('Number of Channels',2,'UTF-8','little',True),
        NumberField('Sample Rate',4,'UTF-32','little',True),
        NumberField('Byte Rate',4,'UTF-32','little',True),
        NumberField('Block Align',2,'UTF-8','little',True),
        NumberField('Bits Per Sample',2,'UTF-8','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'fmt ', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
        assert self.fields[2].data > 0, f'Invalid {self.fields[2].name}'
        assert self.fields[3].data > 0, f'Invalid {self.fields[3].name}'
        assert self.fields[4].data > 0, f'Invalid {self.fields[4].name}'
        assert self.fields[5].data > 0, f'Invalid {self.fields[5].name}'
        assert self.fields[6].data > 0, f'Invalid {self.fields[6].name}'
        assert self.fields[7].data > 0, f'Invalid {self.fields[7].name}'
        

class TheDataChunk(Chunk):

    def __init__(self):
        super().__init__('The Data Chunk','data',[TextField('Data Chunk ID',4,'UTF-8','big',True),
        NumberField('Data Chunk Size',4,'UTF-32','little',True),
        TextField('Data Chunk Data',None,'ISO-8859-1','little',False)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'data', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
  
class TheFactChunk(Chunk):

    def __init__(self):
        super().__init__('The Fact Chunk','fact',[TextField('Fact Chunk ID',4,'UTF-8','big',True),
        NumberField('Fact Chunk Size',4,'UTF-32','little',True),
        TextField('Fact Chunk Data',None,'ISO-8859-1','little',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'fact', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'

class TheListChunk(Chunk):

    LIST_CHUNK_INFO_ID = [ 'IARL','IART','ICMS',
                           'ICMT','ICOP','ICRD',
                           'ICRP','IDIM','IDPI',
                           'IENG','IGNR','IKEY',
                           'ILGT','IMED','INAM',
                           'IPLT','IPRD','ISBJ',
                           'ISFT','ISRC','ISRF',
                           'ITCH', 'ITRK' ]

    # this init is incomplete and only contains 3 'preamble' fields which will or will not be followed by list of other subchunks
    def __init__(self):
        super().__init__('The List Chunk','LIST',[TextField('List Chunk ID',4,'UTF-8','big',True),
        NumberField('List Chunk Size',4,'UTF-32','little',True),
        TextField('List Type ID',4,'UTF-8','big',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].read_field(file)

        if self.fields[2].data == 'INFO':
            while(1):
                infoID = TextField('List Chunk ID',4,'UTF-8','big',True)
                infoID.read_field(file)
                
                if infoID.data not in self.LIST_CHUNK_INFO_ID:
                    break

                size = NumberField('List Chunk Size',4,'UTF-32','little',True)
                size.read_field(file)
                text = TextField('List Type ID',size.data,'UTF-8','big',True)
                text.read_field(file)

                self.fields.append(infoID)
                self.fields.append(size)
                self.fields.append(text)
        file.seek(0)
    
    def assert_chunk(self):
        assert self.fields[0].data == 'LIST', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'