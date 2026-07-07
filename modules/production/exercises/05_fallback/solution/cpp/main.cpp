#include <iostream>

int main() {
    bool primary = false;
    std::cout << (!primary ? "FALLBACK_OK" : "PRIMARY_OK") << "\n";
    return 0;
}
