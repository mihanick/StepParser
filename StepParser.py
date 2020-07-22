from Entity import *
from StringExtensions import *

# Parallel processing with Pool.apply_async()
import multiprocessing as mp

# На входе #1503= IFCPROPERTYSINGLEVALUE('SelfClosing',$,IFCBOOLEAN(.F.),$);
def parse_definition(raw_line):
    result = None

    # #80= IFCAXIS2PLACEMENT3D(#78,#76,#74);
    if raw_line.strip().startswith('#'):
        id,remainder = raw_line.split('=', maxsplit = 1)

        id = id.strip()[1:] #remove first #hash
        remainder = remainder.strip()[:-1]#remove trailing ;semicolumn

        result = parse_token(remainder)

        result.id= id
    else:
        result = Encoder(raw_line).unescape()

    return result

# на входе IFCPROPERTYSINGLEVALUE('SelfClosing',$,IFCBOOLEAN(.F.),$)
def parse_token(line):
    first_bracket = line.find('(')

    result = Token(line)
    result.name = line[:first_bracket].strip()
    attribute_line = line[first_bracket:].strip()
    result.arguments = parse_set(attribute_line)

    return result

# На входе строчка: ($,'\X2\041D0435\X0\ \X2\043E043F0440043504340435043B0435043D\X0\',$,$,$,$,$,$)
def parse_set(line):
    result = []
    if line is not None:
        set_contents = split_set(line)
        for entity in set_contents:
            result.append(parse_entity(entity))

    return result

def parse_entity(line):

    if line == '':
        return None
    line = line.strip()

	# https://habr.com/ru/post/460719/
	# Также символ $ означает null-значение, символ * используется если потомок сам присваивает значению атрибуту предка. Значения типа enum записываются между двумя точками — .ELEMENT.
    result = None
    first_symbol = line[0]

    if first_symbol == "\'":
        ss = line.strip()[1:-1]
        result = Encoder(ss).unescape()
    elif first_symbol == '(':
        result = parse_set(line)
    elif first_symbol == '$': # step null value
        result = None
    elif first_symbol == '*': # step undefined value
        result = None
    elif first_symbol == '.': # predefined words like .ELEMENT.
        result = line
    elif first_symbol == '#':
        result = Anchor(line)
    elif first_symbol.isnumeric() or first_symbol == '+' or first_symbol == '-':
        result = float(line)
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

def pool_parse_file(filename):
    result = []
    block_size = 1024*8
    remainder = ''
    pool = mp.Pool(mp.cpu_count())

    results = []

    def collect(res):
        global results
        results.append(res)


    with open(filename) as fp:
        while True:
            chunk = fp.read(block_size)
            if not chunk:
                break
            v = remainder + chunk
            
            for line in v.splitlines():
                if line.rstrip().endswith(';'):
                    remainder = ''
                    # lines.append(line)
                    pool.apply_async(parse_definition, args=(line), callback=collect)
                else:
                    remainder += line
    
    #result = pool.map(parse_definition, [line for line in lines])
    pool.close()          
    pool.join()

    result.extend(results)
    return result