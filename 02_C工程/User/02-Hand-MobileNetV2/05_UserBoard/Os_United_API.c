//======================================================================
//文件名称：Os_United_API.c（RTOS函数通用桥接文件）
//框架提供：苏大嵌入式（sumcu.suda.edu.cn）
//更新记录：20241216-20250116
//文件内容：实现Harmony-RTOS的桥接
//======================================================================
#include "Os_United_API.h"

//======================================================================
//函数名称：event_recv_api
//函数返回：事件字的标志
//参数说明：event，事件id，
//          set，查询的标记，
//          option，EVENT_FLAG_AND|EVENT_FLAG_OR|EVENT_FLAG_CLEAR
//          timeout，WAITING_FOREVER|WAITING_NO
//          recved，事件字的标志
//功能概要：事件创建的桥接函数，让07文件夹可移植
//内部调用：无
//更改记录：WYH,20250116，消除警告错误
//======================================================================
void event_recv_api(event_t event, uint32_t set, uint8_t option, int32_t timeout, uint32_t *recved)
{
    if(option & EVENT_FLAG_AND)
    {
        if(option & EVENT_FLAG_CLEAR)
        {
            *recved=osEventFlagsWait(event,set,osFlagsWaitAll,timeout);
        }
        else
        {
            *recved=osEventFlagsWait(event,set,osFlagsWaitAll|osFlagsNoClear,timeout);
        }
    }
    else
    {
        if(option & EVENT_FLAG_CLEAR)
        {
            *recved=osEventFlagsWait(event,set,osFlagsWaitAny,timeout);
        }
        else
        {
            *recved=osEventFlagsWait(event,set,osFlagsWaitAny|osFlagsNoClear,timeout);
        }
    }
}

//======================================================================
//函数名称：thread_startup_api
//函数返回：void
//参数说明：         thread，线程id，
//                  set，查询的标记
//功能概要：线程创建的替代函数，让07文件夹可移植
//内部调用：无
//======================================================================
void thread_startup_api(thread_t thread){

}
