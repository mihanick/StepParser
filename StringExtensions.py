
def left(value, sub_string):
    result = ""
    if value is not None:
        result,_ = value.split(sub_string, maxsplit = 1)
    return result.strip()

def right(value, sub_string):
    result = ""
    if value is not None:
        _,result = value.split(sub_string, maxsplit = 1)
    return result.strip()

def between(value, character_start, character_end):
    if value is not None:
        return left(right(value,character_start), character_end)
    return None

def between_brackets(value, open_bracket_symbol='('):
    line = ""
    val = value.strip()
    first_bracket_index = val.find(open_bracket_symbol)
    last_bracket_index = matching_bracket_index(val, first_bracket_index)
    return val[first_bracket_index + 1:last_bracket_index]

def matching_bracket_index(value, start_bracket_index=0, open_bracket_symbol='(', closing_bracket_symbol=')'):
    if start_bracket_index > len(value):
        raise IndexError("Argument out of range")

    nesting_level = 0
    within_quotes = False

    for i in range(start_bracket_index + 1,len(value)):
        c = value[i]

        if not within_quotes:
            if c == closing_bracket_symbol:
                if nesting_level == 0:
                    return i
                nesting_level -= 1
            if c == open_bracket_symbol:
                nesting_level+= 1
        if c == "\'":
            within_quotes = not within_quotes

    raise ValueError('No matching bracket found')

# TODO: rewrite in py way
# https://waymoot.org/home/python_string/
def split_set(value, open_bracket_symbol='(', closing_bracket_symbol=')'):
    result = []
    nesting_level = 0
    within_quotes = False

    entity = ""

    val = between_brackets(value).strip()

    for i in range(len(val)):
        c = val[i]

        if (not within_quotes):
            #closing bracket of first level, the one we need
            if c == closing_bracket_symbol:
                nesting_level -=1

            if c == open_bracket_symbol:
                nesting_level+=1

            # witin our set
            if nesting_level == 0:
                if c == ',':
                    #new entity
                    result.append(entity)
                    entity = ''
                    continue
        if c == "\'":
            within_quotes = not within_quotes

        entity += c
    
    result.append(entity)
    return result



        


