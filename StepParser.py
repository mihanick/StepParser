from Entity import *
from StringExtensions import *

# На входе #1503= IFCPROPERTYSINGLEVALUE('SelfClosing',$,IFCBOOLEAN(.F.),$);
def parse_definition(raw_line):
    result = None

    # #80= IFCAXIS2PLACEMENT3D(#78,#76,#74);
    if raw_line.strip().startswith('#'):
        id,remainder = raw_line.split('=', maxsplit = 1)

        id = id = id.strip()[1:] #remove first #hash
        remainder = remainder.strip()[:-1]#remove trailing ;semicolumn

        result = parse_token(remainder)

        result.id= id
    else:
        result = Entity(raw_line)

    return result

# на входе IFCPROPERTYSINGLEVALUE('SelfClosing',$,IFCBOOLEAN(.F.),$)
def parse_token(line):
    first_bracket = line.find('(')

    result = Token(line)
    result.name = line[:first_bracket].strip()
    attribute_line = line[first_bracket:].strip()
    s = Set(attribute_line)
    s.entities= parse_line(attribute_line)

    result.arguments = s

    return result

# На входе строчка: ($,'\X2\041D0435\X0\ \X2\043E043F0440043504340435043B0435043D\X0\',$,$,$,$,$,$)
def parse_line(line):
    result = []
    if line is not None:
        set_contents = split_set(line)
        for entity in set_contents:
            result.append(parse_entity(entity))

    return result

def parse_entity(line):

    if line == '':
        return None

	# https://habr.com/ru/post/460719/
	# Также символ $ означает null-значение, символ * используется если потомок сам присваивает значению атрибуту предка. Значения типа enum записываются между двумя точками — .ELEMENT.
    result = None
    first_symbol = line.strip()[0]

    if first_symbol == "\'":
        ss = line.strip()[1:-1]
        result = Identifier(ss)
    elif first_symbol == '(':
        result = Set(line)
        result.entities = parse_line(line)
    elif first_symbol == '$': # step null value
        result = None
    elif first_symbol == '*': # step undefined value
        result = None
    elif first_symbol == '.': # predefined words like .ELEMENT.
        result = Anchor(line)
    elif first_symbol == '#':
        result = Anchor(line)
    elif first_symbol.isnumeric() or first_symbol == '+' or first_symbol == '-':
        result = NumericValue(line)
    else:
        result = parse_token(line)

    return result

# https://towardsdatascience.com/how-to-do-efficient-file-handling-d1822d26cb64
def parse_file(filename):
    result = []
    block_size = 1024*8
    remainder = ''
    
    with open(filename) as fp:
        while True:
            chunk = fp.read(block_size)
            if not chunk:
                break
            v = remainder + chunk
            for line in v.splitlines():
                if line.rstrip().endswith(';'):
                    remainder = ''
                    parsed = parse_definition(line)
                    result.append(parsed)
                else:
                    remainder = line
                
    return result

