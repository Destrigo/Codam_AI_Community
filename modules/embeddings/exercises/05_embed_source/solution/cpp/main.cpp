#include "codam_llm.hpp"
#include <cstdlib>
#include <iostream>

int main() {
    (void)codam::embeddings("test");
    bool mock = std::getenv("CODAMLINGS_MOCK") != nullptr;
    std::cout << (mock ? "EMBED_SOURCE:mock" : "EMBED_SOURCE:api") << "\n";
    return 0;
}
