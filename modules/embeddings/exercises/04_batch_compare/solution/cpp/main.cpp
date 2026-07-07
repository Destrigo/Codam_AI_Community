#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> docs = {"a", "b", "c"};
    for (const auto& d : docs) { (void)d.size(); }
    std::cout << "BATCH_OK\n";
    return 0;
}
