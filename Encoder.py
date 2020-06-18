from StringExtensions import *

class Encoder:

    '''
    // Documentation on this can be found at 
	// http://www.buildingsmart-tech.org/implementation/get-started/string-encoding/string-encoding-decoding-summary
	// and in the stringconverter.java class thereby posted.
	//
	// available patterns are:
	//  ''                  -> '
	//  \\                  -> \
	//  \S\<1 char>         -> add 0x80 to the char
	//  \P[A-I]\            -> Use codepage ISO-8859-x where x is 1 for A, 2 for B, ... 9 for I. (eg '\PB\' sets ISO-8859-2)
	//  \X\<2 chars>        -> 1 byte hexadecimal unicode
	//  \X2\<4 chars>\X0\   -> 2 byte Unicode sequence (can be repeated until termination with \X0\)
	//  \X4\<8 chars>\X0\   -> 4 byte Unicode sequence (can be repeated until termination with \X0\)

	// A list of available code pages for .NET is available at
	// http://msdn.microsoft.com/en-us/library/system.text.encodinginfo.codepage.aspx
	// Unit tests have been performed with data from http://www.i18nguy.com/unicode/supplementary-test.html#utf8
	'''

    SingleApostrophToken = "\'"
    SingleBackslashToken = "\\"
    CodeTableToken = "\P"
    UpperAsciiToken = "\\S\\"
    Hex8Token = "\\X\\"
    Hex16Token = "\\X2\\"
    Hex32Token = "\\X4\\"
    LongHexEndToken = "\\X0\\"
    UpperAsciiShift = 0x80

    def ParseCodeTable(self):
        CodePageIds = 'ABCDEFGHI'
        raise UnicodeError('Cannot parse code page')

    def ParseUpperfAscii(self):
        self.val = right(self.val, self.UpperAsciiToken)
        #ich = byte(val[0]) + self.UpperAsciiShift
        #upperAscii = byte(ich)
        #l = OneByteDecoder.GetChars(upperAscii)
        l = chr(ord(self.val[0]) + self.UpperAsciiShift)
        self.val = self.val[1:]
        self.result+=l

    def ParseHex8(self):
        self.val = right(self.val,self.Hex8Token)
        self.result+= chr(int(self.Hex8Token+self.val[0],8))
        self.val = self.val[1:]
        

    def ParseHex(self, length_of_string=4):
        self.val = right(self.val,self.Hex16Token)#or Hex32Token
        
		# multiple sequences of stringLenght characters could follow until the
		# termination
        hexes, v = self.val.split(self.LongHexEndToken, maxsplit = 1)
        self.val = v

        a = []
        for i in range(0, len(hexes),length_of_string):
            a.append(chr(int(hexes[i:i + length_of_string],length_of_string*4)))

        l = ''.join(a)
        self.result+=l

    def __init__(self, value):
        self.val = value
        self.result = ''

    def unescape(self):
        while len(self.val) > 0:
            if self.val.startswith(self.CodeTableToken):
                self.ParseCodeTable()
            elif self.val.startswith(self.UpperAsciiToken):
                self.ParseUpperfAscii()
            elif self.val.startswith(self.Hex8Token):
                self.ParseHex8()
            elif self.val.startswith(self.Hex16Token):
                self.ParseHex(4)
            elif self.val.startswith(self.Hex32Token):
                self.ParseHex(8)
            elif self.val.startswith(self.SingleApostrophToken):
                self.result+= self.val[0]
                self.val = self.val[1:]
            elif self.val.startswith(self.SingleBackslashToken):
                self.result+= self.val[0]
                self.val = self.val[1:]
            else:
                self.result+= self.val[0]
                self.val = self.val[1:]

        return self.result
