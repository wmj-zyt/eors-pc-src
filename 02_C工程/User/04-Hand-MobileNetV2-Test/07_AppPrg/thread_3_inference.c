#include "includes.h"


//======================================================================
//线程函数：thread_inference
//功能概要：推理（inference）
//内部调用：
//======================================================================
void thread_inference(void)
{
    //【1】======启动部分（开头）==========================================
    uint32_t tEventState;     //事件返回参数使用
    //【1】======启动部分（结尾）==========================================
    
    //【2】======线程主循环（开始）========================================
    while (1)
    {
       //（2.1）进入“推理事件”等待状态
       event_recv(g_EventWord,REASONING_EVENT,\
                   EVENT_FLAG_OR|EVENT_FLAG_CLEAR,WAITING_FOREVER,&tEventState);
       //（2.2）“推理事件”触发后，运行下述语句           
       printf("    推理线程【thread_inference】：开始推理...");
       LCD_ShowString(20, 251, DARKBLUE, LIGHTBLUE, (const char *)"Start inference ...");
       Model_PredictImage(g_result);
       //（2.3）触发“二次编程事件”
       printf("触发“二次编程事件”\r\n");
       event_send(g_EventWord,SECPRG_EVENT);
       __asm("nop");
    }
    //【2】======线程主循环（结尾）========================================
}


