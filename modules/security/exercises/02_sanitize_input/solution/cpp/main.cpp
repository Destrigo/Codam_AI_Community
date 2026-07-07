#include <iostream>
#include <string>

static std::string sanitize(std::string text) {
    for (const char* bad : {"ignore instructions", "system:"}) {
        std::string needle(bad);
        for (size_t pos = 0; (pos = text.find(needle, pos)) != std::string::npos;) {
            text.erase(pos, needle.size());
        }
    }
    while (!text.empty() && text.front() == ' ') text.erase(text.begin());
    while (!text.empty() && text.back() == ' ') text.pop_back();
    return text;
}

int main() {
    std::cout << "SANITIZED_OK:" << sanitize("hello system: ignore instructions world") << "\n";
    return 0;
}
