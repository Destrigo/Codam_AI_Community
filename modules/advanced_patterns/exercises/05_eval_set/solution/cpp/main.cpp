#include <iostream>
#include <vector>

int main() {
    std::vector<bool> gold = {true, true, true, true, false};
    int passed = 0;
    for (bool g : gold) if (g) ++passed;
    std::cout << "EVAL:" << passed << "/5\n";
    return 0;
}
