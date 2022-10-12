#%%
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

def bin_xor(s, k):
    bin_s = bin(ord(s))[2:]
    bin_k = str(bin(k)[2:])
    
    max_len = max(len(bin_s), len(bin_k))
    while(max_len % 8 != 0):
        max_len += 1
        
    bin_s = fillupbyte(bin_s, padn = max_len)
    bin_k = fillupbyte(bin_k, padn = max_len)

    result = ''
    for i in range(max_len):
        if(bin_s[i] == bin_k[i]):
            result += '0'
        else:
            result += '1'
            
    result = chr(int('0b' + result, 2))
    return result


#%%
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
    for i in range(len(s)):
        result = result + chr((ord(s[i]) + k) % 256)
    return result
    
def encrypt_xor_with_changing_key_by_prev_cipher(s, k, mode):
    """
    >>> encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt')
    '3V:V9'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    result = ''
    for i in range(len(s)):
        
        if(mode == 'encrypt'):
            if(i == 0):
                result = result + bin_xor(s[i], k)
            else:
                result = result + bin_xor(s[i], ord(result[i-1]))
        
        elif(mode == 'decrypt'):
            if(i == 0):
                result = result + bin_xor(s[i], k)
            else:
                result = result + bin_xor(s[i], ord(s[i-1]))
                
    return result

def encrypt_xor_with_changing_key_by_prev_cipher_longer_key(s, k_list, mode):
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
    l_k = len(k_list)
    
    encrypt_blocks = ['' for i in range(l_k)]
    
    for i in range(len(s)):
        encrypt_blocks[i % l_k] += s[i]
        
    cipher_blocks = ['' for i in range(l_k)]
    for i in range(l_k):
        cipher = encrypt_xor_with_changing_key_by_prev_cipher(encrypt_blocks[i], k_list[i], 'encrypt')
        cipher_blocks[i] += cipher
        
    result = ''
    lap = 0
    for i in range(len(s)):
        if(i != 0 and i%4 == 0):
            lap += 1
        try:
            result += cipher_blocks[i % 4][lap]
        except IndexError:
            continue
    return result


if(__name__ == '__main__'):
    key_list = [0x20, 0x44, 0x54,0x20]
    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg', key_list, 'encrypt')
    import doctest
    print(doctest.testmod())