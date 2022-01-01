#include "pch.h"
#include "TCalcFuncSets.h"
#include "plug.h"
#include<iostream>
//���ɵ�dll���������dll�뿽����ͨ���Ű�װĿ¼��T0002/dlls/����,���ڹ�ʽ���������а�





void TestPlugin1(int DataLen, float* pfOUT, float* pfINa, float* pfINb, float* pfINc)
{
    auto a = new GoSlice;
    a->len = DataLen;
    a->cap = DataLen;
    a->data = pfINa;
    auto b = new GoSlice;
    b->len = DataLen;
    b->cap = DataLen;
    b->data = pfINb;
    auto c = new GoSlice;
    c->len = DataLen;
    c->cap = DataLen;
    c->data = pfINc;
    auto flag = DoubleStarsDay(DataLen, *a, *b, *c);
    for (int i = 0; i < DataLen; i++)
    {
        pfOUT[i] = flag.r0;
        if (i==DataLen-1){
            pfOUT[i] = flag.r1;
        }
    }
}

void TestPlugin2(int DataLen, float* pfOUT, float* pfINa, float* pfINb, float* pfINc)
{
    for (int i = 0;i < DataLen;i++)
    {
        pfOUT[i] = pfINa[i] + pfINb[i] + pfINc[i];
        pfOUT[i] = pfOUT[i] / 3;
    }
}


//���صĺ���
PluginTCalcFuncInfo g_CalcFuncSets[] =
{
    {1, (pPluginFUNC) &TestPlugin1},
    {2, (pPluginFUNC) &TestPlugin2},
    {0, NULL},
};

//������TCalc��ע�ắ��
BOOL RegisterTdxFunc(PluginTCalcFuncInfo** pFun)
{
    if (*pFun == NULL)
    {
        (*pFun) = g_CalcFuncSets;
        return TRUE;
    }
    return FALSE;
}


void test()
{
    std::cout << "yes" << std::endl;
}
