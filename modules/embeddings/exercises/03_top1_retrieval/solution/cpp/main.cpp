#include <iostream>
#include <map>
#include <string>
#include <vector>

static double sim(const std::vector<double>& a, const std::vector<double>& b) {
    double s = 0;
    for (size_t i = 0; i < a.size(); ++i) s += a[i] * b[i];
    return s;
}

int main() {
    std::vector<double> q = {1.0, 0.0};
    std::map<std::string, std::vector<double>> docs = {
        {"doc_a", {1.0, 0.0}},
        {"doc_b", {0.0, 1.0}},
    };
    std::string best;
    double best_score = -1;
    for (const auto& [name, vec] : docs) {
        double s = sim(q, vec);
        if (s > best_score) { best_score = s; best = name; }
    }
    std::cout << "TOP1:" << best << "\n";
    return 0;
}
