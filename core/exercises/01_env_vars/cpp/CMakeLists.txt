cmake_minimum_required(VERSION 3.16)
project(ex01_env_vars)
add_executable(main main.cpp)
target_compile_features(main PRIVATE cxx_std_17)
