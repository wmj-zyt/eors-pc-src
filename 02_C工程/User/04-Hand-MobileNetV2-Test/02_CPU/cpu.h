//======================================================================
//文件名称：cpu.h（cpu头文件）
//制作单位：SD-Arm(sumcu.suda.edu.cn)
//更新记录：20210709
//======================================================================
#ifndef CPU_H     //防止重复定义（CPU_H 开头）
#define CPU_H

//（1）【变动】包含所有芯片头文件，因CPU不同而异
#include "interr.h"
#include "d1.h"
#include "riscv64.h"
#include "stdint.h"
#include "io.h"
//（2）【变动】复位相关
// 按键复位
// #define IS_PIN_RESET_OCCURED     
                          
// // 上电复位                                
// #define IS_POWERON_RESET        
// 写1清引脚复位标志位 
// #define CLEAR_PIN_RESET_FLAG     

//（3）【固定】中断宏定义,若是ARM架构，则根据芯片手册自行定义开关中断语句；
//【20221021】若为RISC-V架构由硬件自己管理开关中断故宏定义为空
#define ENABLE_INTERRUPTS             //开机器模式总中断
#define DISABLE_INTERRUPTS            //关机器模式总中断
//#define ENABLE_INTERRUPTS        ({ __asm("li t0, 0x8"); __asm("csrs mstatus, t0"); })     //开机器模式总中断
//#define DISABLE_INTERRUPTS       ({ __asm("li t0, 0x8"); __asm("csrc mstatus, t0"); })     //关机器模式总中断
//（4）【固定】不优化类型别名宏定义
typedef volatile uint8_t      vuint8_t;   // 不优化无符号8位数，字节
typedef volatile uint16_t     vuint16_t;  // 不优化无符号16位数，字
typedef volatile uint32_t     vuint32_t;  // 不优化无符号32位数，长字

//（5）【固定】位操作宏函数（置位、清位、获得寄存器一位的状态）
#define BSET(bit,Register)  ((Register)|= (1<<(bit)))    //置寄存器的一位
#define BCLR(bit,Register)  ((Register) &= ~(1<<(bit)))  //清寄存器的一位
#define BGET(bit,Register)  (((Register) >> (bit)) & 1)  //获得寄存器一位的状态

#endif    //防止重复定义（CPU_H 结尾）