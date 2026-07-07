#include "codam_config.hpp"
#include <iostream>

int main() {
    std::string model = codam::getenv_or("OLLAMA_MODEL", "llama3.2");
    std::cout << "MODEL_OK:" << model << "\n";
    return 0;
}
