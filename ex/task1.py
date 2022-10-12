def test_function(lst_nums):
    lst_chars = [chr(x) for x in lst_nums]
    
    strng = ''.join(lst_chars)
    
    strng = strng.lower()
    
    stng_short = strng[2:10]
    
    stng_short = stng_short + stng_short
    
    return stng_short