def hex2bin(s):
    """ Converts a hexadecimal number to binary
    >>> hex2bin('f')
    '1111'
    >>> hex2bin('5')
    '101'
    >>> hex2bin('1')
    '1'
    """
    n = int(s, 16) 
    result = ''
    while(n > 0):
        result = str(n % 2) + result
        n = n >> 1    
    return result
    
def bin2hex(s):
    """ Converts a binary number to hexadecimal
    >>> bin2hex('1111')
    'f'
    >>> bin2hex('100001')
    '21'
    >>> bin2hex('1')
    '1'
    """    
    bnum = int(s)
    temp = 0
    mul = 1
    count = 1
    hexaDeciNum = ['0'] * 100 # Result stored here
      
    i = 0
    while(bnum != 0):
        rem = bnum % 10
        temp = temp + (rem * mul)
          
        if(count % 4 == 0): # If a group of 4 has completed
            if(temp < 10):
                hexaDeciNum[i] = chr(temp+48)
            else:
                hexaDeciNum[i] = chr(temp+55)
            mul = 1
            temp = 0
            count = 1
            i = i+1
              
        else:
            mul = mul*2
            count = count+1
        bnum = int(bnum/10)
          
    if(count != 1):
        hexaDeciNum[i] = chr(temp+48)
    if(count == 1):
        i = i-1
          
    # Reverse
    result = ''
    while i >= 0:
        result = result + hexaDeciNum[i]
        i = i-1    

    return result.lower()

def fillupbyte(s, padn = 8, padchar = '0', mode = 'l'):
    """ Pads a string received with a given character, to a given length, from right or left
    >>> fillupbyte('011')
    '00000011'
    >>> fillupbyte('1')
    '00000001'
    >>> fillupbyte('10111')
    '00010111'
    >>> fillupbyte('11100111')
    '11100111'
    >>> fillupbyte('111001111')
    '0000000111001111'
    """
    n = len(s)
    l = n
    while(l % padn != 0):
        l += 1
    result = ''
    j = 0
    for i in range(l):
        if(i < l-n):
            if(mode == 'l'):
                result = padchar + result
            else:
                result = result  + padchar
        else:
            if(mode == 'l'):
                result = result + s[j]
                j += 1
            else:
                result = s[::-1][j] + result
                j += 1
                
    return result

def int2base64(s):
    """ Converts an integer to base64 representation
    >>> int2base64(0x61)
    'YQ=='
    >>> int2base64(0x78)
    'eA=='
    """    
    integer = int(s)
    binary_string = ''
    while(integer > 0):
        digit = integer % 2
        binary_string += str(digit)
        integer = integer // 2
    binary_string = binary_string[::-1]

    padded_string = fillupbyte(binary_string, padn = 8)
    padded_6_string = fillupbyte(padded_string, padn = 6, mode = 'r')
    
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base64_table = letters + letters.lower() + ''.join([str(x) for x in range(10)]) + '+/'
    
    result = ''
    for i in range(0, len(padded_6_string), 6):
        chunk = padded_6_string[i:i+6]
        b64 = base64_table[int(chunk, 2)]
        result = result + b64
    
    result_padded = fillupbyte(result, padn = 4, padchar = '=', mode='r')
    return result_padded
    
def hex2base64(s):
    """ Converts a hexadecimal number to base64 representation
    >>> hex2base64('61')
    'YQ=='
    >>> hex2base64('123456789abcde')
    'EjRWeJq83g=='
    """
    binary_string = hex2bin(s)

    padded_string = fillupbyte(binary_string, padn = 8)
    padded_6_string = fillupbyte(padded_string, padn = 6, mode = 'r')
    
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base64_table = letters + letters.lower() + ''.join([str(x) for x in range(10)]) + '+/'
    
    result = ''
    for i in range(0, len(padded_6_string), 6):
        chunk = padded_6_string[i:i+6]
        b64 = base64_table[int(chunk, 2)]
        result = result + b64
    
    result_padded = fillupbyte(result, padn = 4, padchar = '=', mode='r')
    return result_padded 
    

if (__name__ == '__main__'):
    import doctest
    print(doctest.testmod())
