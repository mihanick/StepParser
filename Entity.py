from StepParser import *
from StringExtensions import *
from Encoder import Encoder

class Token:
    """Token"""
    def __init__(self, source):
        self.id = ""
        self.name = ""
        self.arguments = []

    def __repr__(self):
        return "[{0}] {1}".format(self.id ,self.name)

class Anchor:
    def __init__(self, source):
        #strip first #
        self.id = source[1:]

    def __repr__(self):
        return self.id 



