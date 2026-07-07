#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> votes = {"a", "a", "b"};
    std::map<std::string, int> counts;
    for (const auto& v : votes) ++counts[v];
    int best = 0;
    for (const auto& [k, c] : counts) best = std::max(best, c);
    std::cout << "VOTE:" << best << "\n";
    return 0;
}
