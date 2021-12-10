cmake_minimum_required(VERSION 3.20)
project(test5 C)

set(CMAKE_C_STANDARD 99)
link_libraries("/Users/keeyu/code/github/tool/test5/libfoo.a")
add_executable(test5 main.c)
