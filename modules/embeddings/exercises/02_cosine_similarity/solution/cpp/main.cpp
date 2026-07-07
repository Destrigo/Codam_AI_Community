#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

static double cosine(const std::vector<double>& a, const std::vector<double>& b) {
    double dot = 0, na = 0, nb = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        dot += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }
    return dot / (std::sqrt(na) * std::sqrt(nb));
}

int main() {
    std::cout << "SIMILARITY:" << std::fixed << std::setprecision(1) << cosine({1, 0, 0}, {1, 0, 0}) << "\n";
    return 0;
}
