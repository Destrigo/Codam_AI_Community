#pragma once

#include <cstdlib>
#include <string>

namespace codam {

inline std::string getenv_or(const char* key, const std::string& fallback = "") {
    const char* value = std::getenv(key);
    return value ? std::string(value) : fallback;
}

inline constexpr const char* kMistralApiBaseDefault = "https://api.mistral.ai/v1";
inline constexpr const char* kMistralModelDefault = "mistral-small-latest";

inline std::string mistral_api_base() {
    std::string base = getenv_or("MISTRAL_API_BASE", kMistralApiBaseDefault);
    if (!base.empty() && base.back() == '/') {
        base.pop_back();
    }
    return base;
}

inline std::string mistral_api_key() {
    return getenv_or("MISTRAL_API_KEY");
}

inline std::string mistral_model() {
    return getenv_or("MISTRAL_MODEL", kMistralModelDefault);
}

}  // namespace codam
