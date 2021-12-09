extern "C" void foo(int a, int b);
//extern "C" void redis();
extern "C" void calc(long ,float *,float *,float *,float *);
extern "C" void say_hello();
int main()
{
    foo(5, 7);
//    redis()
    float a[3]={1,2,3};
    float b[3]={1,2,3};
    float c[3]={1,2,3};
    float d[3]={1,2,3};
    say_hello();
    calc(3,a,b,c,d);
    say_hello();
    return 0;
}