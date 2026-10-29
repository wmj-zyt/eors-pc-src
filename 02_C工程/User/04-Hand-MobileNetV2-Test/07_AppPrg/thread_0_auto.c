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
    printf("【中文名称】串口验证                                      \n");
	printf("【程序功能】                                              \n");
	printf("      （1）蓝色闪烁；                                     \n");
	printf("      （2）通过用户串口（UART_User)，接收PC机发出的图像    \n");
    printf("           进行推理，LCD显示推理结果                      \n");
    printf("【硬件连接】见本工程05_UserBoard文件夹下user.h文件         \n");
    printf("--------------------------------------------------------\n\0"); 
    //【1】======启动部分（开头）==========================================
    //（1.1）【根据本函数所用的变量声明】声明main函数使用的局部变量

    //（1.2）【不变】关总中断
    DISABLE_INTERRUPTS;
    //（1.3）【根据本函数所用的变量赋初值】给主函数使用的局部变量赋初值

    //（1.4）【根据includes.h文件中声明的全局变量】给全局变量赋初值
    g_Time[0] = 0;      //时
   	g_Time[1] = 0;	  	//分
   	g_Time[2] = 0;	  	//秒
   	g_img_pro_flag=0;
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
    uart_init(UART_User, 115200);           //初始化串口模块
    // （1.5.3）Timer定时器号、中断间隔(单位ms)  
    timer_init(TIMER_User, 20);   //设置TIMER_USER为20ms中断，中断函数会更新gTime
    // （1.5.3）初始化外部设备LCD，并给出初始显示  
    LCD_Init();  
    LCD_ShowString(10,6,RED,WHITE,(const char *)" 金葫芦AHL-EORS  UART-Test"); //字符串
    LCD_DrawRectangle(22,38,208,210,RED);	    //标注屏幕红框
    LCD_aotu(8,215,232,315,1);                 //画红框下部的凹凸框（凸）
    

    //（1.6）【根据所使用的硬件模块中断】使能模块中断
    uart_enable_re_int(UART_User);
    timer_enable_int(TIMER_User);
    // cam_enable_int();             //使能摄像头帧中断
    //（1.7）【不变】开总中断
	ENABLE_INTERRUPTS;
    //【1】======启动部分（结尾）==========================================

    //【2】======操作系统部分（开始）=======================================
	//（2.1）声明线程变量
	thread_t thd_inference;
	thread_t thd_secprg;
    thread_t thd_unframe;
    thread_t thd_imgpre;

	//（2.2）创建事件字_EventWord
	g_EventWord=event_create("g_EventWord",IPC_FLAG_PRIO);      
	//（2.3）创建用户线程
	thd_inference=thread_create("inference", (void *)thread_inference, 0, (1024*1024 * 20), 13, 20); 
	thd_secprg=thread_create("secprg", (void *)thread_secprg, 0, (1024*1024 * 5), 14, 20); 
	thd_unframe=thread_create("unframe", (void *)thread_unframe, 0, (1024*1024 * 5), 14, 20); 
	thd_imgpre=thread_create("imgpre", (void *)thread_imgpre, 0, (1024*1024 * 5), 12, 20); 

	//（2.4）启动用户线程
    thread_startup(thd_unframe);
    thread_startup(thd_inference);
    thread_startup(thd_secprg);
    thread_startup(thd_imgpre);
    
    //（2.5）阻塞本线程
    thread_block();
    //【2】======操作系统部分（结尾）========================================
}  













