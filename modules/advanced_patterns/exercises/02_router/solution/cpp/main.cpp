#include <iostream>
#include <string>

static std::string route(const std::string& q) {
    return q.rfind("what", 0) == 0 ? "rag" : "chat";
}

int main() {
    std::cout << "ROUTE:" << route("what is RAG") << "\n";
    return 0;
}
