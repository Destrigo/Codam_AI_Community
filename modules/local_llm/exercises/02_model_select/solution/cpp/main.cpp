#include "codam_config.hpp"
#include <iostream>

int main() {
    std::cout << "MODEL:" << codam::mistral_model() << "\n";
    return 0;
}
