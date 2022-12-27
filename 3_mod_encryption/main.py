# Imports from previous weeks --> tests have been deleted
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

def bin2dec(binary):
    binary1 = int(binary)
    decimal, i, n = 0, 0, 0
      
    while(binary1 != 0):
        dec = binary1 % 10
        decimal = decimal + dec * pow(2, i)
        binary1 = binary1//10
        i += 1
    return(decimal)
    
def dec2hex(decimal):
    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3',
                        4: '4', 5: '5', 6: '6', 7: '7',
                        8: '8', 9: '9', 10: 'A', 11: 'B',
                        12: 'C', 13: 'D', 14: 'E', 15: 'F'}

    if(decimal <= 0):
        return ''

    remainder = decimal % 16
    return dec2hex(decimal//16) + conversion_table[remainder]

def bin2hex(n):
    decimal = bin2dec(n)
    return dec2hex(decimal)

def hex2bin(s):
    n = int(s, 16) 
    result = ''
    while(n > 0):
        result = str(n % 2) + result
        n = n >> 1    
    return result

def hex_xor(s1, s2):
    maxlen = -1
    if(len(s1) > len(s2)):
        maxlen = len(s1)
    else:
        maxlen = len(s2)
    
    s1_bin = list(hex2bin(s1))
    s2_bin = list(hex2bin(s2))
    
    l1 = len(s1_bin) 
    l2 = len(s2_bin)
    
    if(l1 > l2):
        while(l1 != l2):
            s2_bin.insert(0,'0')
            l2 = len(s2_bin)
    
    elif(l1 < l2):
        while(l1 != l2):
            s1_bin.insert(0,'0')
            l1 = len(s2_bin)
    
    s_xor = ''
    for i,j in zip(s1_bin, s2_bin):
        b1 = bool(int(i))
        b2 = bool(int(j))
        s_xor = s_xor + str(int((b1^b2)))
    
    s_xor_pad = fillupbyte(s_xor, padn=4)
    
    result = bin2hex(s_xor_pad) 
    
    res_len = len(result)
    while(res_len != maxlen):
        result = '0' + result
        res_len = res_len+1
    
    return result.lower()

def string2hex(s):
    result = ""
    for c in s:
        result += hex(ord(c))[2:]
    return result

def hex2string(s):
    result = ""
    for i in range(0, len(s), 2):
        result += chr(int(s[i:i+2], 16))
    return result

# Methods for the current task
def encrypt_by_add_mod(s, k):
    """
    >>> encrypt_by_add_mod('Hello',123)
    'Ãàççê'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Hello',123),133)
    'Hello'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Cryptography',10),246)
    'Cryptography'
    """
    result = ''
    for x in s:
        result += chr((ord(x) + k) % 256) # Convert to ascii --> add --> mod
    return result
    
def encrypt_xor_with_changing_key_by_prev_cipher(s, k, mode, key_len=2):
    """
    >>> encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt')
    '3V:V9'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    if(mode not in ['encrypt','decrypt']):
        raise Exception('Invalid mode parameter submitted: valid modes are: encrypt, decrypt')
    
    result = ''
    hex_message = string2hex(s) 
    hex_key = hex(k)[2:] # Trim the 0x from beginning
    l_m = len(hex_message)
    
    for i in range(0, l_m, key_len): # Stepping in the message in 2-blocks
        to_encrypt = hex_message[i:i+2]
        encrypt_block = hex_xor(to_encrypt, hex_key)
        result = result + encrypt_block
        if(mode == 'encrypt'):
            hex_key = encrypt_block
        else:
            hex_key = to_encrypt
            
    return hex2string(result)

def encrypt_xor_with_changing_key_by_prev_cipher_longer_key(s, key_list, mode):
    """
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg', key_list, 'encrypt')
    'A&7D$@P'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('aaabbbb', key_list, 'encrypt')
    'A%5B#GW'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg',key_list,'encrypt'), key_list,'decrypt')
    'abcdefg'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(encrypt_xor_with_changing_key_by_prev_cipher_longer_key('Hellobello, it will work for a long message as well',key_list,'encrypt'),key_list,'decrypt')
    'Hellobello, it will work for a long message as well'
    """
    
    key_len = 4
    key_list_len = len(key_list)
    l_m = len(s)
    
    msg_map = {i:"" for i in range(key_list_len)}
    key_map = {i:x for i,x in enumerate(key_list)}
    
    for i,x in enumerate(s):
        msg_map[i % key_list_len] += x
    
    key_map_encrypt = {i:"" for i in range(key_list_len)}
    for i in key_map_encrypt.keys():
        msg_to_code = msg_map[i]
        key_to_code = key_map[i]
        encoded_msg = encrypt_xor_with_changing_key_by_prev_cipher(msg_to_code, key_to_code, mode)
        key_map_encrypt[i] += encoded_msg
    
    total = 0
    for i in range(len(key_map_encrypt.keys())):
        total += len(key_map_encrypt[i])
    
    result = ''
    lap = 0
    for i in range(total):
        if(i != 0 and i%4 == 0):
            lap += 1
        try:
            result += key_map_encrypt[i % 4][lap]
        except IndexError:
            continue
    
    return result

#%%
# 'h\x07k\x02k\x1c<\x1cs\x1e\x7f\x1e{'

if(__name__ == '__main__'):
    key_list = [0x20, 0x44, 0x54,0x20]
    import doctest
    print(doctest.testmod())