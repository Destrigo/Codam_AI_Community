#include <iostream>
#include <string>
#include <vector>

static std::vector<std::string> chunk(const std::string& text, size_t size) {
    std::vector<std::string> out;
    for (size_t i = 0; i < text.size(); i += size) {
        out.push_back(text.substr(i, size));
    }
    return out;
}

int main() {
    std::cout << "CHUNKS:" << chunk("abcdefghij", 4).size() << "\n";
    return 0;
}
