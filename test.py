import random
from math import gcd

def string_to_bits(s):
    result = []
    for char in s:
        bits = bin(ord(char))[2:].zfill(8)
        result.extend([int(b) for b in bits])
    return result

def bits_to_string(b):
    chars = []
    for i in range(0, len(b), 8):
        byte = b[i:i+8]
        bits = ''.join(str(bit) for bit in byte)
        chars.append(chr(int(bits, 2)))
    return ''.join(chars)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Tạo khóa
    result = string_to_bits('AB')
    print("Result:", bits_to_string(result))
    
# git git git