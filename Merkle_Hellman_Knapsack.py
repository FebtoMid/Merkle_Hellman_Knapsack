import random
from math import gcd

# Hàm tính nghịch đảo modulo
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None  # Không tồn tại nghịch đảo nếu a và m không nguyên tố cùng nhau
    else:
        # Thuật toán Euclid mở rộng
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            t = m
            # Cập nhật m và a
            m = a % m
            a = t
            # Cập nhật x0 và x1
            t = x0
            x0 = x1 - q * x0
            x1 = t
        # Đảm bảo x1 là số dương
        if x1 < 0:
            x1 += m0
        return x1

# Hàm tạo dãy superincreasing
def generate_superincreasing_sequence(n):
    w = []
    total = 0
    for _ in range(n):
        next_val = random.randint(total + 1, total * 2 + 1) if total > 0 else 1
        w.append(next_val)
        total += next_val
    return w

# Kiểm tra dãy superincreasing
def is_superincreasing_sequence(seq):
    total = 0  # Tổng các phần tử trước đó
    for num in seq:
        if num <= total:
            return False  # Nếu bất kỳ phần tử nào không thỏa mãn điều kiện, trả về False
        total += num  # Cập nhật tổng
    return True  # Nếu kiểm tra hết mà không vi phạm, trả về True

# Hàm tạo khóa
def generate_keys(n):
    # Tạo dãy superincreasing w
    w = generate_superincreasing_sequence(n)

    # Chọn q lớn hơn tổng các phần tử trong w
    total_w = sum(w)
    q = random.randint(total_w + 1, total_w * 2)

    # Chọn r sao cho gcd(r, q) = 1
    while True:
        r = random.randint(2, q - 1)
        if gcd(r, q) == 1:
            break

    # Tạo khóa công khai b
    b = [(r * wi) % q for wi in w]

    # Trả về khóa riêng và khóa công khai
    private_key = (w, q, r)
    public_key = b
    return private_key, public_key

# Hàm kiểm tra tính hợp lệ của q
def is_valid_q(w, q):
    total_w = sum(w)  # Tính tổng các phần tử trong w
    return q > total_w  # q phải lớn hơn tổng

# Hàm kiểm tra tính hợp lệ của r
def is_valid_r(r, q):
    return 2 <= r < q and gcd(r, q) == 1

# Hàm kiểm tra tính hợp lệ chung của r và q
def are_q_and_r_valid(w, q, r):
    return is_valid_q(w, q) and is_valid_r(r, q)

# Hàm tính b 
def calculate_b(w, q, r):
    # Kiểm tra đầu vào có hợp lệ không
    if not is_valid_q(w, q):
        raise ValueError("q không hợp lệ: q phải lớn hơn tổng các phần tử trong w.")
    if not is_valid_r(r, q):
        raise ValueError("r không hợp lệ: r phải nguyên tố cùng nhau với q và trong khoảng [2, q).")
    
    # Tính khóa công khai b
    b = [(r * wi) % q for wi in w]
    return b

# Hàm chuyển đổi chuỗi thành danh sách bit
def string_to_bits(s):
    result = []
    for char in s:
        bits = bin(ord(char))[2:].zfill(8)
        result.extend([int(b) for b in bits])
    return result

# Hàm chuyển đổi danh sách bit thành chuỗi
def bits_to_string(b):
    chars = []
    for i in range(0, len(b), 8):
        byte = b[i:i+8]
        bits = ''.join(str(bit) for bit in byte)
        chars.append(chr(int(bits, 2)))
    return ''.join(chars)

def encrypt(message, public_key):
    b = public_key
    encrypted_message = []
    
    for char in message:
        # Chuyển ký tự sang danh sách bit nhị phân (8 bit)
        bits = [int(bit) for bit in bin(ord(char))[2:].zfill(8)]
        
        # Mã hóa từng ký tự
        c = sum(mi * bi for mi, bi in zip(bits, b))
        
        # Lưu kết quả mã hóa
        encrypted_message.append(c)
    
    return encrypted_message

def decrypt(ciphertexts, private_key):
    w, q, r = private_key
    
    # Tính nghịch đảo modulo của r
    r_inv = mod_inverse(r, q)
    if r_inv is None:
        raise ValueError("Không tồn tại nghịch đảo modulo của r và q.")
    
    # Danh sách để lưu chuỗi giải mã
    decrypted_message = []
    
    for ciphertext in ciphertexts:
        # Tính c' cho từng phần tử ciphertext
        c_prime = (ciphertext * r_inv) % q
        
        # Giải bài toán knapsack
        message_bits = []
        for wi in reversed(w):
            if c_prime >= wi:
                message_bits.append(1)
                c_prime -= wi
            else:
                message_bits.append(0)
        message_bits.reverse()
        
        # Chuyển danh sách bit thành ký tự
        char = bits_to_string(message_bits)
        decrypted_message.append(char)
    
    # Trả về chuỗi giải mã
    return ''.join(decrypted_message)


# Ví dụ sử dụng
if __name__ == "__main__":
    n = 8  # Số bit trong thông điệp

    # Tạo khóa
    private_key, public_key = generate_keys(n)
    print("Khóa riêng:", private_key)
    print("Khóa công khai:", public_key)

    # Thông điệp cần mã hóa
    message_str = "Have Mid"  # Bạn có thể thay đổi thông điệp tại đây
    message_bits = string_to_bits(message_str)
    print("Thông điệp gốc:", message_bits)

    # Mã hóa
    ciphertext = encrypt(message_str, public_key)
    print("Bản mã:", ciphertext)

    # Giải mã
    decrypted_bits = decrypt(ciphertext, private_key)
    print("Thông điệp giải mã:", decrypted_bits)

   
