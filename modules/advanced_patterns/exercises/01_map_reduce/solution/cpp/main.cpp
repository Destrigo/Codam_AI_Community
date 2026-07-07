#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> chunks = {"aa", "bb"};
    int total = 0;
    for (const auto& c : chunks) total += static_cast<int>(c.size());
    std::cout << (total == 4 ? "MAP_REDUCE_OK" : "FAIL") << "\n";
    return 0;
}
