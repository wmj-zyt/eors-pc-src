//======================================================================
// 文件名称：thread_auto.c（自启动线程函数）
// 框架提供：苏大嵌入式（sumcu.suda.edu.cn）
// 更新记录：20230601-20241023
//======================================================================
#define GLOBLE_VAR     //【固定】includes.h定义的全局变量一处声明多处使用
#include "includes.h"  //【固定】包含总头文件


//======================================================================
//线程函数：thread_auto
//功能概要：自启动线程函数
//======================================================================
void thread_auto(void)
{
    printf("---------------------------------------------------------\n");   
    printf("★金葫芦提示★                                            \n");
    printf("【中文名称】推理工程                                      \n");
	 printf("【程序功能】                                              \n");
	 printf("      （1）蓝色闪烁；                                     \n");
	 printf("      （2）摄像头每采集一幅图像，产生中断                  \n");
    printf("      （3）CAM中断中，触发“CAM读取事件”                    \n");
    printf("      （4）图像读取线程读取图像，触发“图像预处理事件”       \n");
    printf("      （5）图像预处理线程进行图像预处理，触发“推理事件”      \n");
    printf("      （6）推理线程进行图像推理，触发“二次编程事件”         \n");
    printf("      （7）二次编程线程，可在此处进行二次编程               \n");
    printf("【硬件连接】见本工程05_UserBoard文件夹下user.h文件          \n");
    printf("--------------------------------------------------------\n\0"); 
    //【1】======启动部分（开头）==========================================
    //（1.1）【根据本函数所用的变量声明】声明main函数使用的局部变量
	   uint8_t mflag;    		    //摄像头CAM初始化状态标志
    //（1.2）【不变】关总中断
       DISABLE_INTERRUPTS;
    //（1.3）【根据本函数所用的变量赋初值】给主函数使用的局部变量赋初值
       mflag=0;
    //（1.4）【根据includes.h文件中声明的全局变量】给全局变量赋初值
       g_Time[0] = 0;             //时
       g_Time[1] = 0;	  	//分
   	 g_Time[2] = 0;	  	//秒
   	 g_img_pro_flag=0;   //图像正在处理标志
       // 初始化分类名称（字符串）数组(0-9)
       g_classification[0]=SORT0;
       g_classification[1]=SORT1;
       g_classification[2]=SORT2;
       g_classification[3]=SORT3;
       g_classification[4]=SORT4;
       g_classification[5]=SORT5;
       g_classification[6]=SORT6;
       g_classification[7]=SORT7;
       g_classification[8]=SORT8;
       g_classification[9]=SORT9;
    //（1.5）【根据所用到的外部硬件设备】进行用户外设模块初始化
    //（1.5.1）初始化蓝灯 
       gpio_init(LIGHT_BLUE,GPIO_OUTPUT,LIGHT_OFF);  //初始化蓝灯，输出，暗
    // （1.5.2）初始化其他硬件模块
       uart_init(UART_User, 1500000);           //初始化串口模块
    // （1.5.3）Timer定时器号、中断间隔(单位ms)  
       timer_init(TIMER_User, 20);   //设置TIMER_USER为20ms中断，中断函数会更新gTime
    // （1.5.3）初始化外部设备LCD，并给出初始显示  
       LCD_Init();       			           
       LCD_DrawRectangle(22,38,208,210,RED);	   //标注屏幕红框
       LCD_aotu(8,220,232,315,1);                 //画凹凸框（凸）
       LCD_ShowString(3,6,RED,WHITE,(const char *)"金葫芦AHL Inference template"); //字符串
    // (1.5.4) 初始化摄像头（必须通过）
       do  
       {
           printf("金葫芦提示：自启动线程【thread_auto】中初始化摄像头....");
           LCD_ShowString(30,60,RED,WHITE,(const char *)"Initialize camera..."); 
           mflag=cam_init();  
           if(mflag==0)
           {
              printf("OK\r\n");
              LCD_ShowString(30,75,RED,WHITE,(const char *)"OK"); 
           }   
           else
           {
              printf("有错误，请检查摄像头硬件是否插好！\r\n"); 
              LCD_ShowString(30,80,RED,WHITE,(const char *)"Error"); 
              LCD_ShowString(30,95,RED,WHITE,(const char *)"plugged in properly?"); 
           }
       } 
       while (mflag==1);
       LCD_DrawSurface(23,39,207,209,WHITE);    //清除摄像头使用的LCD区域
    //（1.6）【根据所使用的硬件模块中断】使能模块中断
       uart_enable_re_int(UART_User);
       timer_enable_int(TIMER_User);
       cam_enable_int();             //使能摄像头帧中断
    //（1.7）【不变】开总中断
	   ENABLE_INTERRUPTS;
    //【1】======启动部分（结尾）==========================================

    //【2】======操作系统部分（开始）=======================================
	//（2.1）声明线程变量
	   thread_t thd_imgget;
	   thread_t thd_imgpre;
	   thread_t thd_inference;
	   thread_t thd_secprg;
    //（2.2）创建事件字_EventWord
	   g_EventWord=event_create("g_EventWord",IPC_FLAG_PRIO);      
	//（2.3）创建用户线程
	   thd_imgget=thread_create("imgget", (void *)thread_imgget, 0, (1024*1024 * 5), 11, 20); 
	   thd_imgpre=thread_create("imgpre", (void *)thread_imgpre, 0, (1024*1024 * 5), 12, 20); 
	   thd_inference=thread_create("inference", (void *)thread_inference, 0, (1024*1024 * 20), 13, 20); 
	   thd_secprg=thread_create("secprg", (void *)thread_secprg, 0, (1024*1024 * 5), 14, 20); 
	//（2.4）启动用户线程
       thread_startup(thd_imgget);
       thread_startup(thd_imgpre);
       thread_startup(thd_inference);
       thread_startup(thd_secprg);
    //（2.5）阻塞本线程
       thread_block();
    //【2】======操作系统部分（结尾）========================================
}  













