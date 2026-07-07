#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, std::string> cache;
    auto get = [&](const std::string& p) {
        if (cache.count(p)) return cache[p];
        cache[p] = "x";
        return std::string("miss");
    };
    get("p");
    get("p");
    std::cout << (cache.count("p") && cache.size() == 1 ? "CACHE_HIT" : "MISS") << "\n";
    return 0;
}
