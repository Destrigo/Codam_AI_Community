#pragma once

#include "codam_config.hpp"
#include <httplib.h>
#include <nlohmann/json.hpp>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>

namespace codam {

inline std::pair<std::string, std::string> parse_api_base(const std::string& base) {
    std::string host = "api.mistral.ai";
    std::string prefix = "/v1";
    if (base.rfind("http://", 0) == 0 || base.rfind("https://", 0) == 0) {
        size_t scheme_end = base.find("://") + 3;
        size_t path_start = base.find('/', scheme_end);
        if (path_start == std::string::npos) {
            host = base.substr(scheme_end);
        } else {
            host = base.substr(scheme_end, path_start - scheme_end);
            prefix = base.substr(path_start);
            if (prefix.back() == '/') {
                prefix.pop_back();
            }
        }
    }
    return {host, prefix};
}

inline std::unique_ptr<httplib::Client> make_api_client() {
    auto [host, _] = parse_api_base(mistral_api_base());
    auto cli = std::make_unique<httplib::Client>(host);
    cli->set_connection_timeout(30, 0);
    return cli;
}

inline httplib::Headers api_headers() {
    httplib::Headers headers = {{"Content-Type", "application/json"}};
    std::string api_key = mistral_api_key();
    if (!api_key.empty()) {
        headers.emplace("Authorization", "Bearer " + api_key);
    }
    return headers;
}

inline std::string chat_completion(const nlohmann::json& messages, int max_tokens = -1) {
    auto [host, prefix] = parse_api_base(mistral_api_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(30, 0);
    nlohmann::json payload = {{"model", mistral_model()}, {"messages", messages}};
    if (max_tokens >= 0) {
        payload["max_tokens"] = max_tokens;
    }
    auto res = cli.Post(prefix + "/chat/completions", api_headers(), payload.dump(), "application/json");
    if (!res || res->status != 200) {
        throw std::runtime_error("chat completion failed");
    }
    return nlohmann::json::parse(res->body)
        .at("choices").at(0).at("message").at("content").get<std::string>();
}

inline void append_sse_chunks(const std::string& body, std::string& output) {
    std::istringstream stream(body);
    std::string line;
    while (std::getline(stream, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        if (line.rfind("data:", 0) != 0) {
            continue;
        }
        std::string payload_line = line.substr(5);
        while (!payload_line.empty() && payload_line.front() == ' ') {
            payload_line.erase(payload_line.begin());
        }
        if (payload_line == "[DONE]" || payload_line.empty()) {
            continue;
        }
        auto parsed = nlohmann::json::parse(payload_line);
        if (parsed["choices"][0].contains("delta") &&
            parsed["choices"][0]["delta"].contains("content")) {
            output += parsed["choices"][0]["delta"]["content"].get<std::string>();
        }
    }
}

inline std::string chat_stream(const nlohmann::json& messages) {
    auto [host, prefix] = parse_api_base(mistral_api_base());
    httplib::Client cli(host);
    cli.set_connection_timeout(30, 0);
    nlohmann::json payload = {
        {"model", mistral_model()},
        {"messages", messages},
        {"stream", true},
    };
    auto res = cli.Post(prefix + "/chat/completions", api_headers(), payload.dump(), "application/json");
    if (!res || res->status != 200) {
        throw std::runtime_error("stream failed");
    }
    std::string output;
    append_sse_chunks(res->body, output);
    return output;
}

}  // namespace codam
