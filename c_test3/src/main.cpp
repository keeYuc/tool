#include<iostream>

//__declspec(dllexport) void test_1();

void test()
{
    std::cout << "use lib test" << std::endl;
}

void test_1()
{
    std::cout << "use lib test 1" << std::endl;
}
