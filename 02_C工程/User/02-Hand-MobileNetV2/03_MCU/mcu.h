//======================================================================
//文件名称：mcu.h（mcu头文件）
//框架提供：苏州大学嵌入式系统与物联网研究所（sumcu.suda.edu.cn）
//更新记录：20181201-20200627
//======================================================================
#ifndef MPU_H     //防止重复定义（MCU_H 开头）
#define MPU_H

//（1）【变动】包含芯片头文件
#include "cpu.h"
#include "interr.h"


//（2）【变动】MCU基本信息相关宏常数
#define MCU_TYPE              "AHL-D1-H-V2.0 "    //MCU型号（19字节）f
#define BIOS_TYPE             "20220519 "       //BIOS版本号（9字节）
#define MCU_SECTORSIZE        2048              //扇区大小（B）
#define MCU_SECTOR_NUM        131072               //MCU扇区总数（默认）
#define MCU_STACKTOP          0x50000000        //栈顶地址（RAM最高地址）
#define MCU_FLASH_ADDR_START  0x00000000        //MCU的FLASH起始地址
#define MCU_FLASH_ADDR_LENGTH 0x10000000        //MCU的FLASH长度（256MB）
#define MCU_RAM_ADDR_START    0x40000000	    //MCU的RAM起始地址
#define MCU_RAM_ADDR_LENGTH   0x10000000	    //MCU的RAM长度（512M）

#endif    //防止重复定义（MCU_H 结尾）
