from abc import abstractmethod, ABC
from typing import Type
from Field import Field

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