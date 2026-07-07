#include "codam_llm.hpp"
#include <iostream>
#include <thread>

int main() {
    auto [host, prefix] = codam::parse_api_base(codam::mistral_api_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(10, 0);
    std::string path = prefix + "/fail_twice";

    for (int attempt = 0; attempt < 3; ++attempt) {
        auto res = cli.Get(path);
        if (res && res->status == 200) {
            std::cout << "RETRY_OK\n";
            return 0;
        }
        if (res && res->status == 503 && attempt < 2) {
            std::this_thread::sleep_for(std::chrono::seconds(1 << attempt));
            continue;
        }
        return 1;
    }
    return 1;
}
