from StepParser import *
from StringExtensions import *
from Encoder import Encoder

class Entity(object):
    """Any step entity"""
    def __init__(self, source):
        self.source = source

    def __str__(self):
        return self.source
    def __repr__(self):
        return self.source

class Token(Entity):
    """Token"""
    def __init__(self, source):
        self.id = ""
        self.name = ""

        self.arguments = None # Set(source)

        super().__init__(source)

    def __repr__(self):
        return "[{0}] {1}".format(self.id ,self.name)

class Set(Entity):
    def __init__(self, source):
        self.entities = []

        super().__init__(source)

class Identifier(Entity):
    
    def __init__(self, source):
        self.id = Encoder(source).unescape()

        super().__init__(source)

    def __repr__(self):
        return self.id 

class Anchor(Entity):
    def __init__(self, source):
        #strip first #
        self.id = source[1:]

        super().__init__(source)

    def __repr__(self):
        return self.id 

class NumericValue(Entity):
    def __init__(self, source):
        self.value = float(source)

        super().__init__(source)

    def __repr__(self):
        return str(self.value)


