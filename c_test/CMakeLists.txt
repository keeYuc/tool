cmake_minimum_required(VERSION 3.20)
project(c_test)

set(CMAKE_CXX_STANDARD 14)
link_libraries("/Users/keeyu/code/github/tool/c_test/libfoo.a" "/Users/keeyu/code/github/tool/c_test/libredis.a")
add_executable(c_test main.cpp)
