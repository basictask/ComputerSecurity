#%% Ref: own implementation.
def fillupbyte(s, padn = 8, padchar = '0', mode = 'l'):
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

#%% Ref: own implementation
def swap_lower_and_upper_bits(n):
    str_n = fillupbyte(str(bin(n)[2:]))
    swapped = ''
    l_s = len(str_n)
    for i in range(0, l_s, 8):
        swapped = swapped + str_n[i+4:i+8]
        swapped = swapped + str_n[i:i+4]
    result = int('0b'  + fillupbyte(swapped, 2), 2)
    return result

#%% Ref: own implementation
def swap_every_second_bit(n):
    str_n = fillupbyte(str(bin(n)[2:])) # Trim leading 0b and fill to 8
    swapped = ''.join([c1+c0 for c0, c1 in zip(str_n[::2], str_n[1::2])]) # Swap every character c0,c1
    result = int('0b' + fillupbyte(swapped, padn = 2), 2) # Reinsert leading 0b, fill to 2 and convert to int
    return result

#%% Ref: https://codescracker.com/python/program/python-program-convert-binary-to-decimal.htm
def bin2dec(binary):
    binary1 = int(binary)
    decimal, i, n = 0, 0, 0
      
    while(binary1 != 0):
        dec = binary1 % 10
        decimal = decimal + dec * pow(2, i)
        binary1 = binary1//10
        i += 1
    return(decimal)
 
#%% Ref: https://www.geeksforgeeks.org/python-program-to-convert-decimal-to-hexadecimal/
def dec2hex(decimal):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3',
                        4: '4', 5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B',
                        12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    if(decimal <= 0):
        return ''
    remainder = decimal % 16
    return dec2hex(decimal//16) + conversion_table[remainder]

#%% Ref: teacher code
def bin2hex(n):
    return hex(int(n, 2))[2:]

#%% Ref: teacher code
def hex2bin(s):
    return bin(int(s, 16))[2:]

#%% Ref: teacher code
def string2hex(message):
    ret = ""
    for c in message:
        ret += hex(ord(c))[2:].rjust(2, '0')
    return ret

#%% Ref: teacher code
def hex2string(hex_message):
    ret = ""
    for i in range(0, len(hex_message), 2):
        ret += chr(int(hex_message[i:i+2], 16))
    return ret

#%% Ref: teacher code
def hex_xor(hex1, hex2):
    target_len = max(len(hex1),len(hex2))
    bin1 = hex2bin(hex1).rjust(target_len*4,'0')
    bin2 = hex2bin(hex2).rjust(target_len*4,'0')
    bin3 = ""
    for i in range(len(bin1)):
        b1 = bin1[i]
        b2 = bin2[i]
        if b1 == b2:
            bin3 += "0"
        else:
            bin3 += "1"
    return bin2hex(bin3).rjust(target_len,'0')

#%% Ref: teacher code
def char_xor(a, b):
    if a == b:
        return '0'
    else:
        return '1'

#%% Ref: teacher code
def create_repeated_key(key,target_len):
    ret = ""
    inner_counter = 0
    for i in range(target_len):
        ret += key[inner_counter]
        inner_counter = (inner_counter + 1) % len(key)
    return ret

#%% Ref: teacher code
def encrypt_single_byte_xor(input_message,key):
    long_key = create_repeated_key(key,len(input_message))
    return hex_xor(input_message,long_key)

#%% Ref: teacher code
def count_simple_text_chars(string):
    valid_characters = "abcdefghijklmnopqrstuvxyz'- \"ABCDEFGHIJKLMNOPQRSTUVXYZ"
    count = 0
    for c in string:
        if c in valid_characters:
            count += 1
    return count

#%% Ref: teacher code
def decrypt_single_byte_xor(cipher):
    best = None
    best_count = None 
    for key in range(256):
        hex_key = hex(key)[2:]
        decrypted_message = hex2string(encrypt_single_byte_xor(cipher, hex_key))
        actual_count = count_simple_text_chars(decrypted_message)
        if best is None or best_count < actual_count:
            best = decrypted_message
            best_count = actual_count
    return best