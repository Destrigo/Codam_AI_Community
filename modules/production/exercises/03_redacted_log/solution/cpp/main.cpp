#include <iostream>
#include <string>

static std::string redact(const std::string& s) {
    std::string out = s;
    size_t pos = 0;
    const std::string secret = "sk-secret";
    while ((pos = out.find(secret, pos)) != std::string::npos) {
        out.replace(pos, secret.size(), "[REDACTED]");
        pos += 10;
    }
    return out;
}

int main() {
    std::string log = redact("key=sk-secret");
    std::cout << (log.find("[REDACTED]") != std::string::npos ? "LOG_REDACTED" : "LEAK") << "\n";
    return 0;
}
