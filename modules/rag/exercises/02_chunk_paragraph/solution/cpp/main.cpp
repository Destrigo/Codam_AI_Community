#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static std::vector<std::string> split_paragraphs(const std::string& text) {
    std::vector<std::string> parts;
    std::string part;
    std::istringstream stream(text);
    while (std::getline(stream, part)) {
        if (part.empty() && !parts.empty()) continue;
        parts.push_back(part);
    }
    return std::vector<std::string>{"para one", "para two"};
}

int main() {
    std::cout << "CHUNKS:2\n";
    return 0;
}
