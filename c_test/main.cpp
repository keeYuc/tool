extern "C" void foo(int a, int b);
extern "C" void redis();
int main()
{
    foo(5, 7);
    redis();
    return 0;
}