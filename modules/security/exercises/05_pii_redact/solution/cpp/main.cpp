#include <iostream>
#include <regex>
#include <string>

static std::string redact_pii(const std::string& text) {
    return std::regex_replace(text, std::regex(R"([\w.-]+@[\w.-]+)"), "[EMAIL]");
}

int main() {
    std::string out = redact_pii("contact marco@example.com please");
    std::cout << (out.find("[EMAIL]") != std::string::npos ? "PII_REDACTED" : "LEAK") << "\n";
    return 0;
}
