//======================================================================
//文件名称：user.h（user头文件）
//框架提供：苏大嵌入式（sumcu.suda.edu.cn）
//更新记录：20181201-20220525
//概要说明：（1）包含用到的头文件，为达到应用程序的可移植性，具体硬件要接
//              芯片哪个引脚，需要在这里宏定义，目的是实现对具体硬件对象
//              编程，而不是对芯片的引脚编程
//          （2）中断处理程序名字在此宏定义，以便isr.c可移植
//【20220516】优化结构，将GEC相关内容移到gec.h中；
//            通用接口头文件Os_United_API.h放置最前面
//======================================================================
#ifndef USER_H   //防止重复定义（USER_H 开头）
#define USER_H

//（1）文件包含
//【固定】包含通用接口文件和gec头文件
#include "Os_United_API.h"
#include "gec.h"
//【变动】根据使用的构件增减
#include "flash.h"
#include "gpio.h"
#include "uart.h"
#include "lcd.h"
#include "timer.h" 
#include "cam.h"

//（2）【变动】为了<07_AppPrg>可复用，main.c及isr.h中用到的宏常数在这里定义
#define MAIN_COUNT  (3000000)     //主函数使用的常数

//（3）【变动】指示灯端口及引脚定义—根据实际使用的引脚改动
//指示灯端口及引脚定义
#define  LIGHT_RED    (PTB_NUM|5)    //红灯
#define  LIGHT_GREEN  (PTB_NUM|12)   //绿灯
#define  LIGHT_BLUE   (PTB_NUM|4)    //蓝灯
//灯状态宏定义（灯亮、灯暗对应的物理电平由硬件接法决定）
#define  LIGHT_ON       0    //灯亮
#define  LIGHT_OFF      1    //灯暗
//【变动】UART可用模块定义
#define UART_Debug  UART_2             //BIOS使用的串口
#define UART_User   UART_0             //用户串口（黑-GND;白-TX;绿-RX）
//用户定时器
#define TIMER_User   Timer0    //用户定时器Timer0

//（4）【变动】中断服务函数宏定义
extern void UART_User_Handler(void);
#define UART0_Handler  UART_User_Handler

extern void TIMER_User_Handler(void);
#define TIMER0_Handler TIMER_User_Handler

extern void Cam_Handler(void);
#define D1_GPIOE_Handler  Cam_Handler

#endif    //防止重复定义（USER_H 结尾）
