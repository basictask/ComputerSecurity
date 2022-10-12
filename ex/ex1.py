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

def bin_xor(s, k):
    bin_s = bin(ord(s))[2:]
    bin_k = str(bin(k)[2:])
    
    max_len = max(len(bin_s), len(bin_k))
    while(max_len % 8 != 0):
        max_len += 1
        
    bin_s = fillupbyte(bin_s, padn = max_len)
    bin_k = fillupbyte(bin_k, padn = max_len)
    
    result = '0'
    for i in range(max_len):
        if(bin_s[i] == bin_k[i]):
            result += '0'
        else:
            result += '1'
    
    result = chr(int(result, 2))
    
    return result

#%% Exam functions
def encrypt_with_power(s, k):
    """
    >>> encrypt_with_power('Hello',250)
    '²A|lo'
    >>> encrypt_with_power(encrypt_with_power('Hello',123),123)
    'Hello'
    >>> encrypt_with_power(encrypt_with_power('Cryptography',10),10)
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    
    for i in range(l_s):
        result = result + bin_xor(s[i], k)
        k = k * k % 256
    
    return result

def encrypt_with_power2(s, k, mode):
    """
    >>> encrypt_with_power2('Hello',253,'encrypt')
    'µl=Í.'
    >>> encrypt_with_power2('Hello2',131,'encrypt')
    'Ël=Í.³'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power2(encrypt_with_power2('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    for i in range(l_s):
        if(mode == 'encrypt'):
            if(i > 0 and (k == 0 or k == 1)):
                k = ord(s[i - 1])
        
        elif(mode == 'decrypt'):
            if(i > 0 and (k == 0 or k == 1)):
                k = ord(result[i - 1])        
        
        result = result + bin_xor(s[i], k)
        k = k * k % 256
        
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
    s = fillupbyte(bin(n)[2:])
    
    swap = ''
    for i in range(0, len(s), 8):
        swap = swap + s[i+4 : i+8]
        swap = swap + s[i : i+4]

    result = int('0b' + swap, 2)

    return result


def encrypt_with_power_and_swap(s, k, mode):
    """
    >>> encrypt_with_power_and_swap('Hello',11,'encrypt')
    '4ÁÕÐê'
    >>> encrypt_with_power_and_swap(encrypt_with_power_and_swap('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap(encrypt_with_power_and_swap('Cryptography',12,'encrypt'),12,'decrypt')
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    for i in range(l_s):
        if(mode == 'encrypt'):
            swap = chr(swap_lower_and_upper_bits(ord(s[i])))
            
            if(i > 0 and (k == 0 or k == 1)):
                k = ord(s[i - 1])
            
            result = result + bin_xor(swap, k)
            k = k * k % 256
        
        elif(mode == 'decrypt'):

            if(i > 0 and (k == 0 or k == 1)):
                k = ord(result[i - 1])        

            temp = bin_xor(s[i], k)
            k = k * k % 256
            result = result + chr(swap_lower_and_upper_bits(ord(temp)))
            
    return result


if(__name__ == "__main__"):
    import doctest
    print(doctest.testmod())