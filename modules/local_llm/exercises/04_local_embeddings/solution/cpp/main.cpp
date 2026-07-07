#include "codam_llm.hpp"
#include <iostream>

int main() {
    (void)codam::embeddings("local");
    std::cout << "LOCAL_EMBED_OK\n";
    return 0;
}
