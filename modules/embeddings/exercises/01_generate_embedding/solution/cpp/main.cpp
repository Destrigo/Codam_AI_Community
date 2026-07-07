#include "codam_llm.hpp"
#include <iostream>

int main() {
    auto vec = codam::embeddings("hello");
    std::cout << "EMBED_DIM:" << vec.size() << "\n";
    return 0;
}
