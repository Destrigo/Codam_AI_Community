#include <httplib.h>
#include <nlohmann/json.hpp>
#include <cstdlib>
#include <iostream>
#include <string>

int main() {
    const char* env = std::getenv("CODAM_LABS_ECHO_URL");
    // Prefer env (set with --mock). Fallback: https://httpbin.org/post
    (void)env;
    // TODO: POST JSON {"name":"codam"}, print ECHO_OK:codam from response["json"]["name"]
    return 0;
}
