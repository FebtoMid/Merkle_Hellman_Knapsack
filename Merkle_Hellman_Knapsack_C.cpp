#include <iostream>
#include <vector>
#include <random>
#include <numeric>
#include <bitset>
#include <algorithm>
#include <tuple>
#include <sstream>

using namespace std;

// Hàm tính nghịch đảo modulo
int mod_inverse(int a, int m) {
    int m0 = m, x0 = 0, x1 = 1;
    if (m == 1) return 0;
    while (a > 1) {
        int q = a / m;
        int t = m;
        m = a % m;
        a = t;
        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }
    if (x1 < 0) x1 += m0;
    return x1;
}

// Hàm tạo dãy superincreasing
vector<int> generate_superincreasing_sequence(int n) {
    vector<int> w;
    int total = 0;
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis;

    for (int i = 0; i < n; ++i) {
        int next_val = total > 0 ? dis(gen, uniform_int_distribution<>::param_type(total + 1, total * 2 + 1)) : 1;
        w.push_back(next_val);
        total += next_val;
    }
    return w;
}

// Kiểm tra dãy superincreasing
bool is_superincreasing_sequence(const vector<int>& seq) {
    int total = 0;
    for (int num : seq) {
        if (num <= total) return false;
        total += num;
    }
    return true;
}

// Hàm tạo khóa
tuple<vector<int>, int, int, vector<int>> generate_keys(int n) {
    vector<int> w = generate_superincreasing_sequence(n);
    int total_w = accumulate(w.begin(), w.end(), 0);
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dis(total_w + 1, total_w * 2);
    int q = dis(gen);

    int r;
    while (true) {
        r = dis(gen, uniform_int_distribution<>::param_type(2, q - 1));
        if (gcd(r, q) == 1) break;
    }

    vector<int> b;
    for (int wi : w) {
        b.push_back((r * wi) % q);
    }

    return make_tuple(w, q, r, b);
}

// Hàm kiểm tra tính hợp lệ của q
bool is_valid_q(const vector<int>& w, int q) {
    int total_w = accumulate(w.begin(), w.end(), 0);
    return q > total_w;
}

// Hàm kiểm tra tính hợp lệ của r
bool is_valid_r(int r, int q) {
    return r >= 2 && r < q && gcd(r, q) == 1;
}

// Hàm kiểm tra tính hợp lệ của dãy w
bool is_valid_w(const vector<int>& w) {
    return is_superincreasing_sequence(w);
}

// Hàm kiểm tra tính hợp lệ chung của r và q
bool are_q_and_r_valid(const vector<int>& w, int q, int r) {
    return is_valid_q(w, q) && is_valid_r(r, q);
}

// Hàm tính b 
vector<int> calculate_b(const vector<int>& w, int q, int r) {
    if (!is_valid_q(w, q)) {
        throw invalid_argument("q không hợp lệ: q phải lớn hơn tổng các phần tử trong w.");
    }
    if (!is_valid_r(r, q)) {
        throw invalid_argument("r không hợp lệ: r phải nguyên tố cùng nhau với q và trong khoảng [2, q).");
    }

    vector<int> b;
    for (int wi : w) {
        b.push_back((r * wi) % q);
    }
    return b;
}

// Hàm chuyển đổi chuỗi thành danh sách bit
vector<int> string_to_bits(const string& s) {
    vector<int> result;
    for (char c : s) {
        bitset<8> bits(c);
        for (int i = 7; i >= 0; --i) {
            result.push_back(bits[i]);
        }
    }
    return result;
}

// Hàm chuyển đổi danh sách bit thành chuỗi
string bits_to_string(const vector<int>& b) {
    string result;
    for (size_t i = 0; i < b.size(); i += 8) {
        bitset<8> byte;
        for (int j = 0; j < 8; ++j) {
            byte[j] = b[i + j];
        }
        result += static_cast<char>(byte.to_ulong());
    }
    return result;
}

vector<int> encrypt(const string& message, const vector<int>& public_key) {
    vector<int> encrypted_message;

    for (char c : message) {
        vector<int> bits = string_to_bits(string(1, c));

        // Mã hóa từng ký tự
        int sum = 0;
        for (size_t i = 0; i < bits.size(); ++i) {
            sum += bits[i] * public_key[i];
        }

        encrypted_message.push_back(sum);
    }

    return encrypted_message;
}

string decrypt(const vector<int>& ciphertext, const vector<int>& w, int q, int r) {
    int r_inv = mod_inverse(r, q);
    if (r_inv == -1) {
        throw invalid_argument("Không tồn tại nghịch đảo modulo của r và q.");
    }

    string decrypted_message;

    for (int c : ciphertext) {
        int c_prime = (c * r_inv) % q;

        // Giải bài toán knapsack
        vector<int> message_bits;
        for (auto wi = w.rbegin(); wi != w.rend(); ++wi) {
            if (c_prime >= *wi) {
                message_bits.push_back(1);
                c_prime -= *wi;
            } else {
                message_bits.push_back(0);
            }
        }

        // Chuyển danh sách bit thành ký tự
        decrypted_message += bits_to_string(message_bits);
    }

    return decrypted_message;
}

int main() {
    int n = 8;  // Số bit trong thông điệp

    // Menu lựa chọn cho khóa
    int choice;
    cout << "Chọn chức năng: \n1. Tạo khóa tự động\n2. Nhập khóa thủ công\nChọn: ";
    cin >> choice;
    cin.ignore(); // Xóa ký tự newline còn lại trong bộ đệm

    vector<int> private_key_w;
    int private_key_q;
    int private_key_r;
    vector<int> public_key;

    if (choice == 1) {
        // Tạo khóa tự động
        tuple<vector<int>, int, int, vector<int>> keys = generate_keys(n);
        private_key_w = get<0>(keys);
        private_key_q = get<1>(keys);
        private_key_r = get<2>(keys);
        public_key = get<3>(keys);
    } else if (choice == 2) {
        // Nhập khóa thủ công
        private_key_w.resize(n);
        cout << "Nhập dãy superincreasing w (mỗi phần tử cách nhau một dấu cách): ";
        for (int i = 0; i < n; ++i) {
            cin >> private_key_w[i];
        }

        // Kiểm tra dãy w có hợp lệ hay không
        if (!is_valid_w(private_key_w)) {
            cout << "Dãy w không hợp lệ! Dãy w phải là một dãy superincreasing." << endl;
            return 1;
        }

        cout << "Nhập giá trị q: ";
        cin >> private_key_q;

        // Kiểm tra tính hợp lệ của q
        if (!is_valid_q(private_key_w, private_key_q)) {
            cout << "q không hợp lệ! q phải lớn hơn tổng các phần tử trong w." << endl;
            return 1;
        }

        cout << "Nhập giá trị r: ";
        cin >> private_key_r;

        // Kiểm tra tính hợp lệ của r
        if (!is_valid_r(private_key_r, private_key_q)) {
            cout << "r không hợp lệ! r phải nguyên tố cùng nhau với q và trong khoảng [2, q)." << endl;
            return 1;
        }

        public_key = calculate_b(private_key_w, private_key_q, private_key_r);
    } else {
        cout << "Lựa chọn không hợp lệ!" << endl;
        return 1;
    }

    // In khóa và các thông tin khác
    cout << "\nKhóa riêng: ";
    for (int i : private_key_w) {
        cout << i << " ";
    }
    cout << "\nKhóa công khai: ";
    for (int i : public_key) {
        cout << i << " ";
    }
    cout << endl;

    // In ra giá trị của r và q
    cout << "Giá trị của r: " << private_key_r << endl;
    cout << "Giá trị của q: " << private_key_q << endl;

    // Menu lựa chọn chức năng mã hóa/giải mã
    cout << "Chọn chức năng: \n1. Mã hóa\n2. Giải mã\nChọn: ";
    cin >> choice;
    cin.ignore(); // Xóa ký tự newline còn lại trong bộ đệm

    if (choice == 1) {
        // Mã hóa
        string message_str;
        cout << "Nhập thông điệp cần mã hóa: ";
        getline(cin, message_str);
        cout << "Thông điệp gốc: " << message_str << endl;

        vector<int> ciphertext = encrypt(message_str, public_key);
        cout << "Bản mã: ";
        for (int c : ciphertext) {
            cout << c << " ";
        }
        cout << endl;

    } else if (choice == 2) {
        vector<int> ciphertext;
        cout << "Nhập bản mã (các số cách nhau bởi dấu cách): ";
        string line;
        getline(cin, line);  // Đọc cả dòng dữ liệu nhập vào
        
        stringstream ss(line);
        int temp;
        while (ss >> temp) {
            ciphertext.push_back(temp);
        }

        // In ra bản mã đã nhập
        cout << "Bản mã đã nhập: ";
        for (int c : ciphertext) {
            cout << c << " ";
        }
        cout << endl;

        // Tiến hành giải mã
        string decrypted_message = decrypt(ciphertext, private_key_w, private_key_q, private_key_r);
        cout << "Thông điệp giải mã: " << decrypted_message << endl;

    } else {
        cout << "Lựa chọn không hợp lệ!" << endl;
    }

    return 0;
}
