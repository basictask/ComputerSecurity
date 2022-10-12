#%% Helper functions from previous classes
def fillupbyte(s, padn = 8, padchar = '0', mode = 'l'):
    if(len(s) % 8 == 0):
        return s
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

def hex2bin(s):
    return bin(int(s, 16))[2:]

def bin2hex(n):
    return hex(int(n, 2))[2:]

def hex2string(hex_message):
    ret = ""
    for i in range(0, len(hex_message), 2):
        ret += chr(int(hex_message[i:i+2], 16))
    return ret

def string2hex(message):
    ret = ""
    for c in message:
        ret += hex(ord(c))[2:].rjust(2, '0')
    return ret

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

#%% Tasks for the exam
def bin_xor(s, k):
    bin_s = bin(ord(s))[2:] # binary message
    bin_k = str(bin(k)[2:]) # binary key
    
    max_len = max(len(bin_s), len(bin_k))
    
    while(max_len % 8 != 0):
        max_len += 1
    
    bin_k = fillupbyte(bin_k, padn=max_len)
    bin_s = fillupbyte(bin_s, padn=max_len)
    
    result = ''
    for i in range(max_len):
        if(bin_s[i] == bin_k[i]):
            result = result + '0'
        else:
            result = result + '1'
    
    return chr(int(result, 2))
    
def encrypt_with_power(s, k):
    """
    >>> encrypt_with_power('Hello',250)
    '²A|lo'
    >>> string2hex(encrypt_with_power('Hello',250))
    'b2417c6c6f'
    >>> string2hex(encrypt_with_power(hex2string('acc5522cca'),250))
    '56e1422cca'
    >>> string2hex(encrypt_with_power(hex2string('acc5522cca'),123))
    'd7dc23cd0b'
    >>> string2hex(encrypt_with_power('I love Cryptography!!!',23))
    '5e314d2ef7642142737871756e667360716978202020'
    >>> encrypt_with_power('I love Cryptography!!!',0)
    'I love Cryptography!!!'
    >>> encrypt_with_power('With key 0, it will not be changed!!!',0)
    'With key 0, it will not be changed!!!'
    >>> encrypt_with_power(encrypt_with_power('Hello',123),123)
    'Hello'
    >>> encrypt_with_power(encrypt_with_power('Cryptography',10),10)
    'Cryptography'
    """
    result = ""
    for i in range(len(s)):
        result = result + bin_xor(s[i], k)
        k = k * k % 256
    return result

def encrypt_with_power2(s, k, mode):
    """
    >>> encrypt_with_power2('Hello',253,'encrypt')
    'µl=Í.'
    >>> encrypt_with_power2('Hello2',131,'encrypt')
    'Ël=Í.³'
    >>> string2hex(encrypt_with_power2('Hello',250,'encrypt'))
    'b2417c00ff'
    >>> string2hex(encrypt_with_power2(hex2string('acc5522cca'),250,'encrypt'))
    '56e1427e8e'
    >>> string2hex(encrypt_with_power2(hex2string('acc5522cca'),123,'encrypt'))
    'd7dc23cd0b'
    >>> string2hex(encrypt_with_power2('I love Cryptography!!!',23,'encrypt'))
    '5e314d2ef713445331f021d52ee6151091a9f8581040'
    >>> encrypt_with_power2('I am',0,'encrypt')
    'Ii°Ì'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',234,'encrypt'),234,'decrypt')
    'Hello'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',2,'encrypt'),2,'decrypt')
    'Hello'
    >>> encrypt_with_power2(encrypt_with_power2('Hello',2,'encrypt'),62,'decrypt')
    'tello'
    >>> encrypt_with_power2(encrypt_with_power2('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    for i in range(l_s):
        if(i > 0):
            if(k == 0 or k == 1):
                if(mode == 'encrypt'):
                    k = ord(s[i-1])
                elif(mode == 'decrypt'):
                    k = ord(result[i-1])

        result =  result + bin_xor(s[i], k)    
        k = k * k % 256
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
    string_n = fillupbyte(str(bin(n))[2:])

    result = ''.join([c1 + c0 for c0, c1 in zip(string_n[::2], string_n[1::2])])    
     
    result = int('0b' + fillupbyte(result, padn=2), 2)  
    
    return result

def encrypt_with_power_and_swap_every_second_bit(s, k, mode):
    """
    >>> encrypt_with_power_and_swap_every_second_bit('Hello',120,'encrypt')
    'üÚùEn'
    >>> encrypt_with_power_and_swap_every_second_bit('Hello',200,'encrypt')
    'LÚùEn'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit('Hello',250,'encrypt'))
    '7ebe8cf00f'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit(hex2string('acc5522cca'),250,'encrypt'))
    'a6eeb14e81'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit(hex2string('acc5522cca'),123,'encrypt'))
    '27d3d0fd04'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit('I love Cryptography!!!',23,'encrypt'))
    '9101bdde38ec7493f23fe119de1ad6e35155376b2373'
    >>> encrypt_with_power_and_swap_every_second_bit(encrypt_with_power_and_swap_every_second_bit('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap_every_second_bit(encrypt_with_power_and_swap_every_second_bit('Hello',234,'encrypt'),234,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap_every_second_bit(encrypt_with_power_and_swap_every_second_bit('Hello',2,'encrypt'),2,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap_every_second_bit(encrypt_with_power_and_swap_every_second_bit('Hello',2,'encrypt'),62,'decrypt')
    'tello'
    >>> encrypt_with_power_and_swap_every_second_bit(encrypt_with_power_and_swap_every_second_bit('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    """
    result = ''
    l_s = len(s)
    for i in range(l_s):
        if(mode == 'encrypt'):
            swap = chr(swap_every_second_bit(ord(s[i]))) # Swap the bits
            if(i > 0 and (k == 0 or k == 1)):
                k = ord(s[i - 1])
                result = result + bin_xor(swap, k)
            else:
                result = result + bin_xor(swap, k)
            k = k * k % 256
        
        elif(mode == 'decrypt'):
            if(i > 0 and (k == 0 or k == 1)):
                k = ord(result[i - 1])
                temp = bin_xor(s[i], k)
            else:
                temp = bin_xor(s[i], k)
            k = k * k % 256
            result = result + chr(swap_every_second_bit(ord(temp)))
    return result

def encrypt_with_power_and_swap_every_second_bit_8byte(s, k, mode):
    """
    >>> key1 = [1,2,3,4,5,6,7,8]
    >>> key2 = [34,76,87,98,33,99,1,234]
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte('Hello',key1,'encrypt'))
    '85989f989a'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte(hex2string('acc5522cca'),key1,'encrypt'))
    '5dc8a218c0'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte(hex2string('acc5522cca'),key2,'encrypt'))
    '7e86f67ee4'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte(hex2string('1234123123'),key2,'encrypt'))
    '0374765032'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte(hex2string('5646234325'),key2,'encrypt'))
    '8bc544e13b'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte('I love Cryptography!!!',key1,'encrypt'))
    '87129f9bbc9c178bf8b2b9a886bf80d26184e7666302'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte("To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer",key1,'encrypt'))
    'a99d13959f1a1797e514948fa13489df8081cb7361a8f5fd98723792f1cc55bb6436fbdb722817de0d25912a15eed115f48b304cd006a278d9bbb10ddad831d68d00dab5ff01dffff3b894f9463132abddfd8a30'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte('Hello world, now I can encpryt with longer key!!',key1,'encrypt'))
    '85989f989a16bc97f998910c09b9aefb509641bfe38d71edbdda112157d6d1eaf869d5625ddb1c3ade1091531ba67c53'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte('Our goal is to test out if our algorithm working well with splitting the input.',key1,'encrypt'))
    '8eb8b2149e9995945f92ba00a1bb21f8fba3e930eeaad96457eab1bf5bc4d1021d32dede57c115ff7c2a1e9016a7f55a809af5ddf771fb1798d53132095de1d1cc17dce8a139c58b80ff1c19dbccbc'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Hello',key1,'encrypt'),key1,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Hello',key2,'encrypt'),key2,'decrypt')
    'Hello'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Hello',key1,'encrypt'),key1,'decrypt')
    'Hello'
    >>> string2hex(encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Hello',key1,'encrypt'),key2,'decrypt'))
    '5be8c4f577'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Cryptography',key1,'encrypt'),key1,'decrypt')
    'Cryptography'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte("To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer",key1,'encrypt'),key1,'decrypt')
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer"
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Hello world, now I can encpryt with longer key!!',key1,'encrypt'),key1,'decrypt')
    'Hello world, now I can encpryt with longer key!!'
    >>> encrypt_with_power_and_swap_every_second_bit_8byte(encrypt_with_power_and_swap_every_second_bit_8byte('Our goal is to test out if our algorithm working well with joining the chunks.',key1,'encrypt'),key1,'decrypt')
    'Our goal is to test out if our algorithm working well with joining the chunks.'
    """
    result = ''
    for i in range(len(s)):
        result = result + encrypt_with_power_and_swap_every_second_bit(s[i], k[i % 8], mode)
    return result 

if(__name__ == "__main__"):
    import doctest
    print(doctest.testmod())