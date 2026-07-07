cmake_minimum_required(VERSION 3.16)

set(_codam_cmake_dir "${CMAKE_CURRENT_LIST_DIR}")
set(_codam_vendor "${_codam_cmake_dir}/../vendor")
set(_codam_include "${_codam_cmake_dir}/../include")

set(_json_header "${_codam_vendor}/nlohmann/json.hpp")
set(_httplib_header "${_codam_vendor}/httplib.h")

if(NOT EXISTS "${_json_header}")
    message(STATUS "Downloading nlohmann/json single header...")
    file(MAKE_DIRECTORY "${_codam_vendor}/nlohmann")
    file(DOWNLOAD
        "https://raw.githubusercontent.com/nlohmann/json/v3.11.3/single_include/nlohmann/json.hpp"
        "${_json_header}"
        SHOW_PROGRESS
    )
endif()

if(NOT EXISTS "${_httplib_header}")
    message(STATUS "Downloading cpp-httplib header...")
    file(DOWNLOAD
        "https://raw.githubusercontent.com/yhirose/cpp-httplib/v0.18.3/httplib.h"
        "${_httplib_header}"
        SHOW_PROGRESS
    )
endif()

add_library(codam_json INTERFACE)
target_include_directories(codam_json INTERFACE "${_codam_vendor}")

add_library(codam_httplib INTERFACE)
target_include_directories(codam_httplib INTERFACE "${_codam_vendor}")

function(add_codam_exercise target source)
    add_executable(${target} ${source})
    target_include_directories(${target} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
        "${_codam_include}"
    )
    target_link_libraries(${target} PRIVATE codam_json codam_httplib)
    target_compile_features(${target} PRIVATE cxx_std_17)
    if(WIN32)
        target_link_libraries(${target} PRIVATE ws2_32 crypt32)
    endif()
endfunction()
