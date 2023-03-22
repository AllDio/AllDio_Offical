def get_str_number(intnumber,intmax):
    if type(intnumber) == int:
        max_length = len(str(intmax))
        max_digi = int('9' * int(max_length))
        if intnumber < max_digi:
            result = '0'*(len(str(max_digi))-len(str(intnumber))) + str(intnumber)
        else:
            result = intnumber
    else:
        result = False
    return result