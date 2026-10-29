#include "includes.h"
//======================================================================
// 线程函数：thread_imgread
// 功能概要：图像读取（Image reading）
// 内部调用：
//======================================================================
void thread_imgget(void)
{
   // 【1】======启动部分（开始）======
   // （1.1）声明临时变量
   uint8_t tFlag;        // 摄像头CAM初始化状态标志
   uint32_t tLoopCount;  // 本线程循环次数
   uint32_t tEventState; // 事件返回参数使用
   uint32_t ti;          // 本线程临时变量
   // （1.2）初始化临时变量
   tFlag = 0;       // 摄像头CAM初始化状态标志
   tLoopCount = 0;  // 本线程循环次数
   tEventState = 0; // 事件返回参数使用
   ti = 0;          // 本线程临时变量
   // (1.3) 初始化摄像头
   do
   {
      printf("金葫芦提示：自启动线程【thread_auto】中初始化摄像头....");
      LCD_ShowString(30, 60, RED, WHITE, (const char *)"Initialize camera...");
      tFlag = cam_init();
      if (tFlag == 0)
      {
         printf("OK\r\n");
         LCD_ShowString(30, 75, RED, WHITE, (const char *)"OK");
      }
      else
      {
         printf("有错误，请检查摄像头硬件是否插好！\r\n");
         LCD_ShowString(30, 80, RED, WHITE, (const char *)"Error");
         LCD_ShowString(30, 95, RED, WHITE, (const char *)"plugged in properly?");
      }
   } while (tFlag == 1);
   LCD_DrawSurface(23, 39, 207, 209, WHITE); // 清除摄像头使用的LCD区域
   cam_enable_int();                         // 使能摄像头帧中断
   // 【1】======启动部分（结尾）======
   // 【2】======线程主循环（开始）======
   while (1)
   {
      printf("读取图像线程【thread_imgread】...\r\n");
      // （2.1）循环次数变量+1
      ti++;
      // （2.2）进入“CAM读取事件”CAM_GET_EVENT的等待状态
      event_recv(g_EventWord, CAM_GET_EVENT,
                 EVENT_FLAG_OR | EVENT_FLAG_CLEAR, WAITING_FOREVER, &tEventState);
      // （2.3）“CAM读取事件”已经触发，运行下列程序
      if (g_img_pro_flag == 0)
         goto thread_imgread_1; // 若可取图像标志=0
      // （2.4）有图像可读，则取图像、LCD显示图像
      cam_getimg(CAMIMG_W, CAMIMG_H, g_image1);            // 取图像
      LCD_DrawPixel(36, 48, CAMIMG_W, CAMIMG_H, g_image1); // LCD显示图像
      // （2.5） 允许获取新的图像,LCD及printf显示获取图像数
      g_img_pro_flag = 0;                // 图像显示已经完成
      printf("图像获取数ti=%d    ", ti); // 向PC打印获取图像数
      printf("Time=%02d:%02d:%02d\r\n", g_Time[0], g_Time[1], g_Time[2]);
      LCD_ShowString(20, 230, BLUE, GRAY, (const char *)"                      "); // 清显示行
      LCD_ShowString(20, 230, BLUE, GRAY, (const char *)NumToStr("Image Number:%d", ti));
      LCD_ShowString(160, 230, RED, GRAY, (const char *)NumToStr("%02d:%02d:%02d", g_Time[0], g_Time[1], g_Time[2]));
      if (ti <= 200)            //采集图像次数
         goto thread_imgread_1; // 小于20幅图像，继续获取
      // （2.6)获得一幅要需要推理的图像
      ti = 0;
      g_img_pro_flag = 1; // 图像处理尚未完成
      tLoopCount++;       // 本线程循环次数
                    // 通过LCD显示循环次数，printf输出循环次数
      LCD_DrawSurface(20, 245, 230, 310, GRAY); // 用着色矩形，清除将要使用的LCD区域
      LCD_ShowString(20, 245, BLUE, GRAY, (const char *)NumToStr("Inference Number:%d", tLoopCount));
      printf("进行推理的图像数tLoopCount=%d\r\n", tLoopCount);
      // （2.7）触发“图像预处理事件”
      event_send(g_EventWord, PRETREAT_EVENT);
   thread_imgread_1:
      __asm("nop");
   }
   // 【2】======线程主循环（结尾）======
}
