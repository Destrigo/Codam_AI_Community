#include <iostream>
#include <vector>

int main() {
    std::vector<int> chunks = {0, 1, 2, 3, 4};
    std::vector<int> selected(chunks.begin(), chunks.begin() + 2);
    std::cout << (selected.size() == 2 ? "TRUNCATED_OK" : "FAIL") << "\n";
    return 0;
}
