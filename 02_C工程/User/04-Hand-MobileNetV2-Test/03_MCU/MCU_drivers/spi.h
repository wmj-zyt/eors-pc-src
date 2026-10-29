#ifndef _NORFLASH_H
#define _NORFLASH_H

#include "mcu.h"
#define SPI_0  0
#define SPI_1  1

#define SPI_MASTER  1
#define SPI_SLAVE   0

//=====================================================================
//函数名称：spi_init
//功能说明：spi初始化
//函数参数：No：模块号
//       MSTR：SPI主从机选择，1：主机，0：从机
//       BaudRate：波特率，单位：bps
//       CPOL：极性
//       CPHA：相位
//函数返回：无
//=====================================================================
void spi_init(uint8_t No,uint8_t MSTR,uint16_t BaudRate,\
		uint8_t CPOL,uint8_t CPHA);
		
//=====================================================================
//函数名称：spi_send1.
//功能说明：SPI发送一字节数据。
//函数参数：No：模块号
//       data： 需要发送的一字节数据。
//函数返回：0：发送失败；1：发送成功。
//=====================================================================
uint8_t spi_send1(uint8_t No,uint8_t data);




#endif