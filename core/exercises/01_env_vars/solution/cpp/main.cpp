#include <cstdlib>
#include <iostream>
#include <string>

int main() {
    const char* value = std::getenv("APP_NAME");
    if (value == nullptr) {
        std::cout << "APP_NAME=MISSING\n";
    } else {
        std::cout << "APP_NAME=" << value << "\n";
    }
    return 0;
}
