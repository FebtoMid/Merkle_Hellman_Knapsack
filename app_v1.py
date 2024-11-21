import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from math import gcd


# Các hàm hỗ trợ
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    else:
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            t = m
            m = a % m
            a = t
            t = x0
            x0 = x1 - q * x0
            x1 = t
        return x1 + m0 if x1 < 0 else x1


def generate_superincreasing_sequence(n):
    w = []
    total = 0
    for _ in range(n):
        next_val = random.randint(total + 1, total * 2 + 1) if total > 0 else 1
        w.append(next_val)
        total += next_val
    return w

def is_superincreasing_sequence(seq):
    total = 0  # Tổng các phần tử trước đó
    for num in seq:
        if num <= total:
            return False  # Nếu bất kỳ phần tử nào không thỏa mãn điều kiện, trả về False
        total += num  # Cập nhật tổng
    return True  # Nếu kiểm tra hết mà không vi phạm, trả về True

def generate_keys(n):
    w = generate_superincreasing_sequence(n)
    total_w = sum(w)
    q = random.randint(total_w + 1, total_w * 2)
    while True:
        r = random.randint(2, q - 1)
        if gcd(r, q) == 1:
            break
    b = [(r * wi) % q for wi in w]
    private_key = (w, q, r)
    public_key = b
    return private_key, public_key


def encrypt(message, public_key):
    b = public_key
    encrypted_message = []
    for char in message:
        bits = [int(bit) for bit in bin(ord(char))[2:].zfill(8)]
        c = sum(mi * bi for mi, bi in zip(bits, b))
        encrypted_message.append(c)
    return encrypted_message


def decrypt(ciphertexts, private_key):
    w, q, r = private_key
    r_inv = mod_inverse(r, q)
    if r_inv is None:
        raise ValueError("Không tồn tại nghịch đảo modular của r và q.")
    decrypted_message = []
    for ciphertext in ciphertexts:
        c_prime = (ciphertext * r_inv) % q
        message_bits = []
        for wi in reversed(w):
            if c_prime >= wi:
                message_bits.append(1)
                c_prime -= wi
            else:
                message_bits.append(0)
        message_bits.reverse()
        char = chr(int(''.join(map(str, message_bits)), 2))
        decrypted_message.append(char)
    return ''.join(decrypted_message)


# Kiểm tra tính hợp lệ của khóa riêng
def check_private_key(private_key):
    try:
        w, q, r = private_key
        if not all(isinstance(i, int) for i in w) or not isinstance(q, int) or not isinstance(r, int):
            return False, "Khóa riêng phải chứa các giá trị số nguyên."
        if not all(w[i] > sum(w[:i]) for i in range(1, len(w))):
            return False, "Dãy w không phải là dãy siêu tăng."
        if q <= sum(w):
            return False, "q phải lớn hơn tổng các phần tử trong w."
        if gcd(r, q) != 1:
            return False, "r và q phải nguyên tố cùng nhau."
        return True, None
    except Exception as e:
        return False, str(e)


# Giao diện Tkinter
class MerkleHellmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Merkle-Hellman Knapsack Encryption")

        # Khung tạo khóa
        frame_key = ttk.LabelFrame(root, text="Tạo khóa")
        frame_key.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(frame_key, text="Khóa riêng:").grid(row=0, column=0, sticky="w")
        self.private_key_entry = ttk.Entry(frame_key, width=70)
        self.private_key_entry.grid(row=0, column=1)

        ttk.Label(frame_key, text="Khóa công khai:").grid(row=1, column=0, sticky="w")
        self.public_key_entry = ttk.Entry(frame_key, width=70)
        self.public_key_entry.grid(row=1, column=1)

        self.generate_key_button = ttk.Button(frame_key, text="Tạo khóa ngẫu nhiên", command=self.generate_keys)
        self.generate_key_button.grid(row=2, column=0, pady=5)

        self.check_key_button = ttk.Button(frame_key, text="Kiểm tra khóa thủ công", command=self.check_keys)
        self.check_key_button.grid(row=2, column=1, pady=5)

        # Khung mã hóa/giải mã
        frame_encrypt = ttk.LabelFrame(root, text="Mã hóa/giải mã")
        frame_encrypt.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(frame_encrypt, text="Thông điệp:").grid(row=0, column=0, sticky="w")
        self.message_entry = ttk.Entry(frame_encrypt, width=70)
        self.message_entry.grid(row=0, column=1)

        self.encrypt_button = ttk.Button(frame_encrypt, text="Mã hóa", command=self.handle_encrypt)
        self.encrypt_button.grid(row=1, column=0, pady=5)

        self.decrypt_button = ttk.Button(frame_encrypt, text="Giải mã", command=self.handle_decrypt)
        self.decrypt_button.grid(row=1, column=1, pady=5)

        ttk.Label(frame_encrypt, text="Bản mã:").grid(row=2, column=0, sticky="w")
        self.ciphertext_entry = ttk.Entry(frame_encrypt, width=70)
        self.ciphertext_entry.grid(row=2, column=1)

        ttk.Label(frame_encrypt, text="Kết quả giải mã:").grid(row=3, column=0, sticky="w")
        self.decrypted_message_entry = ttk.Entry(frame_encrypt, width=70)
        self.decrypted_message_entry.grid(row=3, column=1)

    def generate_keys(self):
        private_key, public_key = generate_keys(8)
        self.private_key_entry.delete(0, tk.END)
        self.private_key_entry.insert(0, str(private_key))
        self.public_key_entry.delete(0, tk.END)
        self.public_key_entry.insert(0, str(public_key))

    def check_keys(self):
        try:
            private_key = eval(self.private_key_entry.get())
            valid, error = check_private_key(private_key)
            if not valid:
                messagebox.showerror("Lỗi", error)
                return
            w, q, r = private_key
            public_key = [(r * wi) % q for wi in w]
            self.public_key_entry.delete(0, tk.END)
            self.public_key_entry.insert(0, str(public_key))
            messagebox.showinfo("Thành công", "Khóa riêng hợp lệ và khóa công khai đã được tính toán.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def handle_encrypt(self):
        if not self.private_key_entry.get():
            messagebox.showerror("Lỗi", "Khóa riêng đang trống! Vui lòng tạo hoặc nhập khóa riêng.")
            return

        if not self.public_key_entry.get():
            self.check_keys()

        try:
            private_key = eval(self.private_key_entry.get())
            valid, error = check_private_key(private_key)
            if not valid:
                messagebox.showerror("Lỗi", error)
                return
            public_key = list(map(int, self.public_key_entry.get().strip("[]").split(",")))
            message = self.message_entry.get()
            ciphertext = encrypt(message, public_key)
            self.ciphertext_entry.delete(0, tk.END)
            self.ciphertext_entry.insert(0, str(ciphertext))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình mã hóa: {e}")

    def handle_decrypt(self):
        if not self.private_key_entry.get():
            messagebox.showerror("Lỗi", "Khóa riêng đang trống! Vui lòng tạo hoặc nhập khóa riêng.")
            return

        if not self.public_key_entry.get():
            self.check_keys()

        try:
            private_key = eval(self.private_key_entry.get())
            valid, error = check_private_key(private_key)
            if not valid:
                messagebox.showerror("Lỗi", error)
                return
            ciphertexts = list(map(int, self.ciphertext_entry.get().strip("[]").split(",")))
            decrypted_message = decrypt(ciphertexts, private_key)
            self.decrypted_message_entry.delete(0, tk.END)
            self.decrypted_message_entry.insert(0, decrypted_message)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi trong quá trình giải mã: {e}")


# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = MerkleHellmanApp(root)
    root.mainloop()
