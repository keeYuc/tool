
extern "C"
{
    void test();
    bool RegisterTdxFunc(void* pFun);
}
//extern void TestPlugin1(int DataLen, float* pfOUT, float* pfINa, float* pfINb, float* pfINc);
int main()
{
    test();
    RegisterTdxFunc((void*)test);
}