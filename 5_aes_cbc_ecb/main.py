#%% Helper functions
def encrypt_aes_ecb(message, key):
    from Crypto.Cipher import AES
    aes2 = AES.new(key, AES.MODE_ECB)
    decoded = aes2.encrypt(message)
    return decoded

#%%
def decrypt_aes_ecb(ciphertext, key):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> decrypt_aes_ecb(bytes([215, 221, 59, 138, 96, 94, 155, 69, 52, 90, 212, 108, 49, 65, 138, 179]),key)
    b'lovecryptography'
    >>> decrypt_aes_ecb(bytes([147, 140, 44, 177, 97, 209, 42, 239, 152, 124, 241, 175, 202, 164, 183, 18]),key)
    b'!!really  love!!'
    """
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)
    
def xor_byte_arrays(a1, a2):
    """
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([2,3,4,5]))
    b'\\x03\\x01\\x07\\x01'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([]))
    b'\\x01\\x02\\x03\\x04'
    >>> xor_byte_arrays(bytes([1,2,3,4]),bytes([1,2]))
    b'\\x01\\x02\\x02\\x06'
    >>> xor_byte_arrays(bytes([1,2,4,8,16,32,64,128]),bytes([1,1,1,1,1,1,1,1]))
    b'\\x00\\x03\\x05\\t\\x11!A\\x81'
    """
    target_len = max(len(a1), len(a2))
    a1 = a1.rjust(target_len, bytes([0]))
    a2 = a2.rjust(target_len, bytes([0]))
    
    result = bytearray(b'')
    for i in range(target_len):
        result.append(a1[i] ^ a2[i])
    result = bytes(result)
    
    return result
    
def decrypt_aes_cbc_with_ecb(message, key, iv):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> decrypt_aes_cbc_with_ecb(bytes([255, 18, 67, 115, 172, 117, 242, 233, 246, 69, 81, 156, 52, 154, 123, 171]),key,iv)
    b'hello world 1234'
    >>> decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64]),key,iv)
    b'lovecryptography'
    >>> decrypt_aes_cbc_with_ecb(bytes([171, 218, 160, 96, 193, 134, 73, 81, 221, 149, 19, 180, 31, 247, 106, 64] * 2),key,iv)
    b'lovecryptography6&\\x94\\x84`\\xd6\\x15\\x12E\\xbf\\xc8\\x0b>\\x0b\\xf6\\xf5'
    """
    result = bytearray(b'')
    
    for x in xor_byte_arrays(decrypt_aes_ecb(message[:16], key), iv): # Xor first with the original key
        result.append(x)
        
    for i in range(16, len(message), 16): # iterating over the message in 16 blocks
        for x in xor_byte_arrays(decrypt_aes_ecb(message[i:i+16], key), message[i-16:i]): # After that, xor with the encryption of the previous block
            result.append(x)
    return bytes(result)
        
def encrypt_aes_cbc_with_ecb(message, key, iv):
    """
    >>> key = bytes([57, 226, 240, 61, 125, 240, 75, 68, 22, 35, 124, 205, 144, 27, 118, 220])
    >>> iv = bytes([241, 147, 66, 129, 194, 34, 37, 51, 236, 69, 188, 205, 64, 140, 244, 204])
    >>> encrypt_aes_cbc_with_ecb(b'hello world 1234',key,iv)
    b'\\xff\\x12Cs\\xacu\\xf2\\xe9\\xf6EQ\\x9c4\\x9a{\\xab'
    >>> encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography'),key,iv)
    b'\\xab\\xda\\xa0`\\xc1\\x86IQ\\xdd\\x95\\x13\\xb4\\x1f\\xf7j@'
    >>> encrypt_aes_cbc_with_ecb(b'hello world 1234hello world 1234hello world 1234',key,iv)
    b'\\xff\\x12Cs\\xacu\\xf2\\xe9\\xf6EQ\\x9c4\\x9a{\\xab>\\xe3\\xc3\\xf5g\\xc7kYZpk>\\x88\\xf3\\x0f\\x16\\x13\\x85\\xb5\\x1d\\r+\\xdc\\xae\\xa1\\x1d\\x80\\xfa_F\\xb1\\xc0'
    >>> encrypt_aes_cbc_with_ecb(bytes(b'lovecryptography123456789abcdefhellooooooooooooo'),key,iv)
    b'\\xab\\xda\\xa0`\\xc1\\x86IQ\\xdd\\x95\\x13\\xb4\\x1f\\xf7j@\\xd7\\xf2\\xd1T\\xfe[\\xd1\\xb4d5\\x90\\xdc\\x1fj?\\x12\\xfd\\x15\\xcb\\x8b\\xa3\\x1c*\\xd4B\\x8fJs\\x03\\xf9\\x7f3'
    """
    result = bytearray(b'')
    
    for x in encrypt_aes_ecb(xor_byte_arrays(message[:16], iv), key): # Xor first with the original key
        result.append(x)
    
    vector = result
    for i in range(16, len(message), 16): # iterating over the message in 16 blocks
        for x in encrypt_aes_ecb(xor_byte_arrays(message[i:i+16], vector), key):
            result.append(x)
        vector = result[len(result)-16 : len(result)] # Assign new encryption vector
    
    return bytes(result)

if(__name__ == '__main__'):
    import doctest
    print(doctest.testmod())