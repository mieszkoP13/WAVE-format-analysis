from abc import abstractmethod, ABC
from typing import Type

class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    PRPLE = '\033[35m'
    YELLW = '\033[33m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'

class Field(ABC):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian:str, isDataCrucial:bool):
        self.name = name
        self.size = size
        self.offset = offset
        self.encoding = encoding
        self.endian = endian

        # Infrorms if data of this field is vital to the analysis; if not, it shall not be displayable
        self.isDataCrucial = isDataCrucial
        self.data = None

    def __str__(self):
        return f'{bcolors.BLUE}Name: {self.name}{bcolors.ENDC}, '\
               f'{bcolors.YELLW}Size: {self.size}{bcolors.ENDC}, '\
               f'{bcolors.PRPLE}Data: { self.data if self.isDataCrucial else "..."}{bcolors.ENDC}, '\
               f'{bcolors.CYAN}Offset: {self.offset}{bcolors.ENDC}, '\
               f'{bcolors.GREEN}Encoding: {self.encoding}{bcolors.ENDC}, '\
               f'{bcolors.WHITE}Endian: {self.endian}{bcolors.ENDC}'
    
    @abstractmethod
    def read_field(self,file):
        pass


class TextField(Field):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian:str, isDataCrucial:bool):
        super().__init__(name, size, offset, encoding, endian, isDataCrucial)

    def read_field(self,file):
        self.data = file.read(self.size).decode(self.encoding)

class NumberField(Field):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian, isDataCrucial:bool):
        super().__init__(name, size, offset, encoding, endian, isDataCrucial)

    def read_field(self,file):
        self.data = int.from_bytes(file.read(self.size), self.endian)


class Chunk(ABC):
    def __init__(self, fields:Type[Field]=None):
        if fields is None:
            self.fields = []

        self.fields = fields

    @abstractmethod
    def read_chunk(self,file):
        pass

    def __str__(self):
        s=''
        for field in self.fields:
            s = s + str(field) + '\n'
        return s
    
    def fieldCount(self):
        return len(self.fields)

class TheRIFFChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Chunk ID',4,0,'UTF-8','big',True),
                        NumberField('Chunk Size',4,4,'UTF-32','little',True),
                        TextField('Format',4,8,'UTF-8','big',True)])
        
    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)


class TheFmtSubChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Subchunk1 ID',4,12,'UTF-8','big',True),
        NumberField('Subchunk1 Size',4,16,'UTF-8','little',True),
        NumberField('Audio Format',2,20,'UTF-8','little',True),
        NumberField('Number of Channels',2,22,'UTF-8','little',True),
        NumberField('Sample Rate',4,24,'UTF-32','little',True),
        NumberField('Byte Rate',4,28,'UTF-32','little',True),
        NumberField('Block Align',2,32,'UTF-8','little',True),
        NumberField('Bits Per Sample',2,34,'UTF-8','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        

class TheDataSubChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Subchunk2 ID',4,36,'UTF-8','big',True),
        NumberField('Subchunk2 Size',4,40,'UTF-32','little',True),
        TextField('Data',None,44,'ISO-8859-1','little',False)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        

def test(fileName):
    with open(fileName,'rb') as f:
        TRChunk = TheRIFFChunk()
        TFSChunk = TheFmtSubChunk()
        TDSChunk = TheDataSubChunk()
        TRChunk.read_chunk(f)
        TFSChunk.read_chunk(f)
        TDSChunk.read_chunk(f)
        print(TRChunk,end='')
        print(TFSChunk,end='')
        print(TDSChunk,end='')


if __name__ == '__main__':
    test('./sound-examples/ex1.wav')