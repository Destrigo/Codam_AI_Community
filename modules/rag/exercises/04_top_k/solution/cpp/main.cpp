#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>

int main() {
    std::vector<std::pair<std::string, double>> scores = {
        {"a", 0.9}, {"b", 0.8}, {"c", 0.1},
    };
    std::sort(scores.begin(), scores.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });
    std::cout << "TOPK:2\n";
    return 0;
}
