#%% Primitive functions
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

#%% Exam
def bin_xor(s, k):
    bin_s = bin(ord(s))[2:]
    bin_k = str(bin(k)[2:])
    
    maxlen = max(len(bin_s), len(bin_k))
    while(maxlen % 8 != 0):
        maxlen += 1
        
    bin_s = fillupbyte(bin_s, padn = maxlen)
    bin_k = fillupbyte(bin_k, padn = maxlen)
    
    result = ''
    for i in range(maxlen):
        if(bin_s[i] == bin_k[i]):
            result = result + '0'
        else:
            result = result + '1'
    
    result = chr(int(result, 2))
    return result


def encrypt_with_mul(s, k):
    """
    >>> encrypt_with_mul('Hello',227)
    '«£àt_'
    >>> encrypt_with_mul(encrypt_with_mul('Hello',123),123)
    'Hello'
    >>> encrypt_with_mul(encrypt_with_mul('Cryptography',10),10)
    'Cryptography'
    >>> encrypt_with_mul(encrypt_with_mul('Cryptoasdoptimalization',123),123)
    'Cryptoasdoptimalization'
    """
    result = ''
    l_s = len(s)
    xor_mul = 2
    for i in range(l_s):
        if(i == 0):
            result = result + bin_xor(s[i], k)
        else:
            k = k * xor_mul % 256
            result = result + bin_xor(s[i], k) 
    return result                 
    
def encrypt_with_mul2(s, k, mode):
    """
    >>> encrypt_with_mul2('Hello',34,'encrypt')
    'j!ä|O'
    >>> encrypt_with_mul2('Hello2',131,'encrypt')
    'Ëc`t_R'
    >>> encrypt_with_mul2(encrypt_with_mul2('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_mul2(encrypt_with_mul2('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    xor_mul = 2
    for i in range(l_s):
        if(i > 0):
            if(k == 0 or k == 1):
                if(mode == 'encrypt'):
                    k = ord(s[i-1])
                elif(mode == 'decrypt'):
                    k = ord(result[i-1])

        if(i == 0):
            result = result + bin_xor(s[i], k)
        else:
            k = k * xor_mul % 256
            result = result + bin_xor(s[i], k) 
    
    return result
            
def swap_lower_and_upper_bits(n):
    """
    >>> swap_lower_and_upper_bits(0)
    0
    >>> swap_lower_and_upper_bits(1)
    16
    >>> swap_lower_and_upper_bits(2)
    32
    >>> swap_lower_and_upper_bits(8)
    128
    >>> bin(swap_lower_and_upper_bits(0b1111))
    '0b11110000'
    >>> bin(swap_lower_and_upper_bits(0b10011010))
    '0b10101001'
    """
    str_n = fillupbyte(str(bin(n)[2:]))
    swapped = ''
    l_s = len(str_n)
    for i in range(0, l_s, 8):
        swapped = swapped + str_n[i+4:i+8]
        swapped = swapped + str_n[i:i+4]
    result = int('0b'  + fillupbyte(swapped, 2), 2)
    return result

def swap_every_second_bit(n):
    """
    >>> swap_every_second_bit(1)
    2
    >>> swap_every_second_bit(2)
    1
    >>> swap_every_second_bit(4)
    8
    >>> swap_every_second_bit(16)
    32
    >>> bin(swap_every_second_bit(0b1010))
    '0b101'
    >>> bin(swap_every_second_bit(0b01010110))
    '0b10101001'
    """
    str_n = fillupbyte(str(bin(n)[2:])) # Trim leading 0b and fill to 8
    swapped = ''.join([c1+c0 for c0, c1 in zip(str_n[::2], str_n[1::2])]) # Swap every character c0,c1
    result = int('0b' + fillupbyte(swapped, padn = 2), 2) # Reinsert leading 0b, fill to 2 and convert to int
    return result
    
    
def count_char(s, c):
    count = 0
    for i in range(len(s)):
        if(s[i] == c):
            count += 1
    return count

def break_scheme2(s):
    """
    >>> break_scheme2("ôR!ú{E")
    'eperke'
    >>> break_scheme2('gamuE')
    'eeeee'
    >>> break_scheme2("bgbzu")
    'cefre'
    """
    count = 0
    guess = 0
    l_s = len(s)
    for k in range(256):
        msg = encrypt_with_mul(s, k)
        curr_count = count_char(msg, 'e')
        if(curr_count > count or guess == 0):
            guess = msg
            count = curr_count
    return guess
    
    
if(__name__ == "__main__"):
    swap_every_second_bit(16)
    import doctest
    print(doctest.testmod())