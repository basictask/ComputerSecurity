#%% Helper functions
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

def left_shift_rot(s, rotn = 1, mode = 'l'):
    l = len(s)
    result = ['x' for x in range(l)]

    if(mode == 'r'): # I have implemented right rotation first by accident so here it will stay    
        for i in range(rotn, l):
            result[i] = s[i-rotn]
    
        for i in range(rotn):
            result[i] = s[l - rotn + i]

    elif(mode == 'l'):
        for i in range(l - rotn):
            result[i] = s[i + rotn]
        
        for i,j in enumerate(range(l - rotn, l)):
            result[j] = s[i]

    result = ''.join(result)

    return result

def bit_permutation(bit, key): # Ref: teacher code
    result = ""
    for k in key:
        result += bit[k-1]
    return result
    
#%% Functions for the task
def bytes2binary(b):
    """
    >>> bytes2binary(b'\\x01')
    '00000001'
    >>> bytes2binary(b'\\x03')
    '00000011'
    >>> bytes2binary(b'\\xf0')
    '11110000'
    >>> bytes2binary(b'\\xf0\\x80')
    '1111000010000000'
    """
    return fillupbyte(bin(int.from_bytes(b, byteorder='big'))[2:])

def binary2bytes(s):
    """
    >>> binary2bytes('00000001')
    b'\\x01'
    >>> binary2bytes('00000011')
    b'\\x03'
    >>> binary2bytes('11110000')
    b'\\xf0'
    >>> binary2bytes('1111000010000000')
    b'\\xf0\\x80'
    """
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def bin_xor(k1, k2):
    """
    >>> bin_xor('1011','0000')
    '1011'
    >>> bin_xor('1','0000')
    '0001'
    >>> bin_xor('1101','1011')
    '0110'
    >>> bin_xor('10101010','01010101')
    '11111111'
    """
    target_len = max(len(k1), len(k2))
    k1 = fillupbyte(k1, padn=target_len)
    k2 = fillupbyte(k2, padn=target_len)
    
    result = ''
    for a,b in zip(k1, k2):
        if(a == b):
            result += '0'
        else:
            result += '1'
    return result
        

def create_DES_subkeys(inp):
    """
    >>> create_DES_subkeys('0001001100110100010101110111100110011011101111001101111111110001')
    ['000110110000001011101111111111000111000001110010', '011110011010111011011001110110111100100111100101', '010101011111110010001010010000101100111110011001', '011100101010110111010110110110110011010100011101', '011111001110110000000111111010110101001110101000', '011000111010010100111110010100000111101100101111', '111011001000010010110111111101100001100010111100', '111101111000101000111010110000010011101111111011', '111000001101101111101011111011011110011110000001', '101100011111001101000111101110100100011001001111', '001000010101111111010011110111101101001110000110', '011101010111000111110101100101000110011111101001', '100101111100010111010001111110101011101001000001', '010111110100001110110111111100101110011100111010', '101111111001000110001101001111010011111100001010', '110010110011110110001011000011100001011111110101']
    """
    from matrices import key_shifts, PC1, PC2
    
    inp = bit_permutation(inp, PC1)

    k1 = inp[:28]
    k2 = inp[28:]

    result = []
    for i in range(len(key_shifts)):
        k1 = left_shift_rot(k1, key_shifts[i])
        k2 = left_shift_rot(k2, key_shifts[i])

        result.append(bit_permutation(k1 + k2, PC2))
    
    return result

#%% Functions for the DES algorithm

def f(message, key):
    """
    >>> f('11110000101010101111000010101010','000110110000001011101111111111000111000001110010')
    '00100011010010101010100110111011'
    """
    from matrices import E
    
    # 1. expand from 32 to 48 bits using the E matrix       
    E = [x-1 for x in E]
    expanded = ''
    for i in range(len(E)):
        expanded += message[E[i]]

    # 2. xor with the key
    expanded = bin_xor(expanded, key)
    
    # 3. get the S-boxes and use them as indices
    from matrices import S
    result = ''
    sbox_i = 0
    for i in range(0, len(expanded), 6):
        B = expanded[i:i+6] # Getting the next block from B
        Sbox = S[sbox_i]
        sbox_i += 1
        
        row = int(B[0] + B[5], 2) # first and last bit: 0...3
        col = int(B[1:5], 2) # middle 4 bits: 0...15
        
        result += fillupbyte(bin(Sbox[row][col])[2:], padn=4, mode='l')
      
    # 4. shuffle based on P    
    from matrices import P
    result = bit_permutation(result, P)
    return result

def encrypt_DES(key, message):
    """
    >>> encrypt_DES(b'\\x13\\x34\\x57\\x79\\x9b\\xbc\\xdf\\xf1',b'\\x01\\x23\\x45\\x67\\x89\\xab\\xcd\\xef')
    b'\\x85\\xe8\\x13T\\x0f\\n\\xb4\\x05'
    """
    bin_m = bytes2binary(message)
    bin_k = bytes2binary(key)
    
    maxlen = max(len(bin_m), len(bin_k))
    bin_m = fillupbyte(bin_m, padn=maxlen)
    bin_k = fillupbyte(bin_k, padn=maxlen)
    
    K = create_DES_subkeys(bin_k)
    
    from matrices import IP
    bin_m = bit_permutation(bin_m, IP)

    # Separate into left and right
    L0 = bin_m[0:int(len(bin_m)/2)]
    R0 = bin_m[int(len(bin_m)/2):len(bin_m)]
    
    for i in range(16):
        L1 = R0
        R1 = bin_xor(L0, f(R0, K[i]))
        L0 = L1
        R0 = R1
    
    from matrices import IP_inverse
    result = R0+L0
    result = bit_permutation(result, IP_inverse)
    result = binary2bytes(result)
    return result

def are_random_tests_all_passes(n, byte_len = 8):
    """
    >>> are_random_tests_all_passes(100)
    True
    """
    from Crypto.Cipher import DES
    import numpy as np
    
    result = True
    for i in range(n):
        key = np.random.bytes(byte_len)
        msg = np.random.bytes(byte_len)
        
        if(encrypt_DES(key, msg) != DES.new(key, DES.MODE_ECB).encrypt(msg)):
            result = False
    
    return result

if(__name__ == '__main__'):
    import doctest
    print(doctest.testmod())

