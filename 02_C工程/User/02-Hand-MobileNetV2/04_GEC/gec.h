//======================================================================
//文件名称：gec.h（GEC芯片引脚头文件）
//框架提供：苏州大学嵌入式系统与物联网研究所（sumcu.suda.edu.cn）
//更新记录：20181201-20220525
//【备注】：与芯片无关
//======================================================================
#ifndef GEC_H    //防止重复定义（开始）
#define GEC_H

#include "mcu.h"
#include "user.h"
#include "printf.h"
//【变动】系统复位函数宏定义
#define NVIC_SystemReset Sys_ResetExecute
//【变动】GEC基本信息==================================================
#define GEC_USER_SECTOR_START    (32768)   /*【0启动】2/2处，0-0启动，31-从BIOS启动*/
#define GEC_COMPONENT_LST_START  (138)   //构件库函数列表开始扇区号
// #define BIOS_UART_Debug_IRQn     (20)   //BIOS程序写入串口的中断号
//【变动】动态命令起始扇区、结束扇区
#define GEC_DYNAMIC_START        (136)                                     
#define GEC_DYNAMIC_END	         (137) 
//【固定】构件库函数指针和系统功能函数声明===========================================
extern void **  component_fun;

#endif  //防止重复定义（结尾）
