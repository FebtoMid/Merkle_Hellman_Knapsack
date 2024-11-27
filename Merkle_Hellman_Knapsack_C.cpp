#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <numeric>

// Hàm tính GCD
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Hàm tính nghịch đảo modular
int mod_inverse(int a, int m) {
    int m0 = m, x0 = 0, x1 = 1;
    if (gcd(a, m) != 1) {
        return -1; // Không tồn tại nghịch đảo modular
    }
    while (a > 1) {
        int q = a / m;
        int t = m;
        m = a % m;
        a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    return (x1 + m0) % m0;
}

// Hàm sinh dãy siêu tăng
std::vector<int> generate_superincreasing_sequence(int n) {
    std::vector<int> w;
    int total = 0;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 10);

    for (int i = 0; i < n; ++i) {
        int next_val = total + dis(gen);
        w.push_back(next_val);
        total += next_val;
    }
    return w;
}

// Kiểm tra dãy có phải dãy siêu tăng không
bool is_superincreasing_sequence(const std::vector<int>& seq) {
    int total = 0;
    for (int num : seq) {
        if (num <= total) {
            return false;
        }
        total += num;
    }
    return true;
}

// Hàm tạo khóa công khai và khóa riêng
std::pair<std::vector<int>, std::vector<int>> generate_keys(int n) {
    std::vector<int> w = generate_superincreasing_sequence(n);
    int total_w = std::accumulate(w.begin(), w.end(), 0);
    int q = total_w + 1 + rand() % (total_w);
    int r = 0;
    do {
        r = 2 + rand() % (q - 2);
    } while (gcd(r, q) != 1);
    
    std::vector<int> b;
    for (int wi : w) {
        b.push_back((r * wi) % q);
    }
    return {w, b};
}

// Hàm mã hóa
std::vector<int> encrypt(const std::string& message, const std::vector<int>& public_key) {
    std::vector<int> encrypted_message;
    for (char c : message) {
        std::vector<int> bits(8);
        for (int i = 0; i < 8; ++i) {
            bits[7 - i] = (c >> i) & 1;
        }
        int c = 0;
        for (size_t i = 0; i < bits.size(); ++i) {
            c += bits[i] * public_key[i];
        }
        encrypted_message.push_back(c);
    }
    return encrypted_message;
}

// Hàm giải mã
std::string decrypt(const std::vector<int>& ciphertexts, const std::vector<int>& private_key) {
    std::vector<int> w = private_key;
    int q = std::accumulate(w.begin(), w.end(), 0) * 2; // Sử dụng tổng của w để ước tính q
    int r = 2 + rand() % (q - 2); // Thử mô phỏng một giá trị r (thực tế sẽ lấy từ khóa riêng)

    int r_inv = mod_inverse(r, q);
    if (r_inv == -1) {
        throw std::invalid_argument("Không thể tính nghịch đảo modular của r và q.");
    }

    std::string decrypted_message;
    for (int ciphertext : ciphertexts) {
        int c_prime = (ciphertext * r_inv) % q;
        std::vector<int> message_bits(w.size(), 0);
        for (int i = w.size() - 1; i >= 0; --i) {
            if (c_prime >= w[i]) {
                message_bits[i] = 1;
                c_prime -= w[i];
            }
        }
        char c = 0;
        for (size_t i = 0; i < message_bits.size(); ++i) {
            c |= (message_bits[i] << (7 - i));
        }
        decrypted_message.push_back(c);
    }
    return decrypted_message;
}

int main() {
    // Tạo khóa
    int n = 8;
    auto [private_key, public_key] = generate_keys(n);

    // In khóa riêng và công khai
    std::cout << "Khóa riêng: ";
    for (int val : private_key) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    std::cout << "Khóa công khai: ";
    for (int val : public_key) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    // Nhập thông điệp
    std::string message;
    std::cout << "Nhập thông điệp cần mã hóa: ";
    std::getline(std::cin, message);

    // Mã hóa
    std::vector<int> ciphertext = encrypt(message, public_key);
    std::cout << "Bản mã: ";
    for (int val : ciphertext) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    // Giải mã
    try {
        std::string decrypted_message = decrypt(ciphertext, private_key);
        std::cout << "Kết quả giải mã: " << decrypted_message << "\n";
    } catch (const std::exception& e) {
        std::cout << "Lỗi trong quá trình giải mã: " << e.what() << "\n";
    }

    return 0;
}
