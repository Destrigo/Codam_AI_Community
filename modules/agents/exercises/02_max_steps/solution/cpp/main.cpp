#include <iostream>

int main() {
    int max_steps = 5;
    for (int i = 0; i < 10; ++i) {
        if (i + 1 >= max_steps) break;
    }
    std::cout << "MAX_STEPS_OK\n";
    return 0;
}
