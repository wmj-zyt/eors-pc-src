#include "includes.h"

//======================================================================
// 线程函数：thread_secprg
// 功能概要：二次编程（Secondary programming）
// 内部调用：
//======================================================================
void thread_secprg(void)
{
    // 【1】======启动部分（开头）==========================================
    uint32_t tEventState; // 事件返回参数使用
    int i, j, k;
    i = 0;
    j = 0;
    // 【1】======启动部分（结尾）==========================================

    // 【2】======线程主循环（开始）========================================
    while (1)
    {
        // （2.1）进入“二次编程事件”等待状态
        event_recv(g_EventWord, SECPRG_EVENT,
                   EVENT_FLAG_OR | EVENT_FLAG_CLEAR, WAITING_FOREVER, &tEventState);
        // （2.2）“二次编程事件”触发后，运行下述语句
        if (g_img_pro_flag == 0)
            goto thread_secprg_1; // 若图像标志=0
                                  // （2.3）g_img_pro_flag=1，可以进行工作，根据推理结果进行二次编程
        printf("二次编程线程【thread_secprg】：二次编程处，可根据推理结果进行二次编程...\r\n");
        LCD_ShowString(135, 260, DARKBLUE, GRAY, (const char *)"compeleted");
        k = (int)(g_result[0] * 10000);
        for (i = 0; i < SortNum; i++)
        {
            printf("推理类别 %s,", g_classification[i]);
            printf("置信度为 %1.4f\r\n", g_result[i]);
            if ((int)(g_result[i] * 10000) >= k)
            {
                k = (int)(g_result[i] * 10000);
                j = i;
            }
        }
        printf("推理结果为：%s,", g_classification[j]); // 向PC输出推理结果
        printf("置信度=%2.2f", g_result[j] * 100);
        uart_send1(UART_Debug, 37); // printf("%")打印不出%
        printf("\r\n");
        LCD_ShowString(20, 275, RED, GRAY, (const char *)NumToStr("Inference result:")); // 向LCD输出推理结果
        LCD_ShowString(160, 275, RED, GRAY, g_classification[j]);
        LCD_ShowString(20, 290, BLUE, GRAY, (const char *)NumToStr("Confidence level:%2.2f", g_result[j] * 100));
        LCD_ShowString(198, 290, BLUE, GRAY, (const char *)"%");
        // （2.4）一幅图像识别完成，恢复图像标志=0，以便 Cam_Handler中设置可取下一幅图像
        g_img_pro_flag = 0; // 一副图像推理完成，恢复图像标志=0，可以进行新的工作流程
    thread_secprg_1:
        __asm("nop");
    }
    // 【2】======线程主循环（结尾）========================================
}
