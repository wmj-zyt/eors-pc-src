#ifndef __FLASH_H
#define __FLASH_H

#include "mcu.h"

//========================================================
//Nor Flash 相关信息 (W25X40CL)
//一次最多可以编程 256 个字节,每个页面 256 字节,2048 个可编程页
//分别具有128个可擦除4K扇区、16个可擦除32KB块和8个可擦除64KB块
//=========================================================
#define NorReadStatusReg		      (0x05) 
#define NorWriteStatusReg		      (0x01) 
#define NorReadData			          (0x03) 
#define NorFastReadData		          (0x0B) 
#define NorFastReadDual		          (0x3B) 
#define NorPageProgram		          (0x02) 
#define NorBlockErase1			      (0x52)    //32K
#define NorBlockErase2			      (0xD8)    //64K
#define NorSectorErase		          (0x20) 
#define NorChipErase			      (0xC7) 
#define NorPowerDown			      (0xB9) 
#define NorDeviceID			          (0xAB) 
 
/* WIP(busy)标志，FLASH内部正在写入 */
#define NorWIP_Flag                   (0x01)
#define NorDummy_Byte                (0xFF)

#define NorSPI_FLASH_PageSize       (0x100)      //256字节
#define NorSPI_FLASH_SECTOR_SIZE    (0x1000)     //1024*4字节
#define NorSPI_FLASH_BULK1_SIZE     (0x8000)     //1024*32字节
#define NorSPI_FLASH_BULK2_SIZE     (0x10000)    //1024*64字节

//========================================================
//spi nand Flash 相关信息 (MX35LF2GE4AD)
//Page size: (2048+64) byte 
//Block size: (128K+4K) byte
//=========================================================
//spi nand flash命令
#define NandRDID			        (0x9f)
#define NandGET_FEATURE             (0x0f)
#define NandSET_FEATURE             (0x1f)
#define NandREAD_PAGE_TO_CACHE	    (0x13)
#define NandREAD_PAGE_FROM_CACHE	(0x03)
#define NandBLOCK_ERASE			    (0xd8)
#define NandPROGRAM_LOAD			(0x02)
#define NandPROGRAM_EXEC			(0x10)
#define NandOPCODE_RESET		    (0xff)
#define NandDummy                   (0x00) 
#define NandFEATURE_PROTECT         (0xa0)
#define NandFEATURE_CONFIG          (0xb0)
#define NandFEATURE_STATUS          (0xc0)
#define NAND_PAGE_BITS	(11)
#define NAND_PAGE_MASK	((1 << NAND_PAGE_BITS) - 1)
#define NAND_PAGE_SIZE	(1 << NAND_PAGE_BITS)

#define WriteEnable		        (0x06) 
#define WriteDisable		    (0x04)
//=====================================================================
//函数名称：flash_init
//功能说明：SPI0模块四线SPI功能初始化,PC2:CLK,PC3:CS,PC4:MOSI,PC5:MISO
//函数参数：无
//函数返回：无
//=====================================================================
void flash_init(void);

//=====================================================================
//函数名称：flash_writeEnable
//功能说明：写使能 
//函数参数：无
//函数返回：无
//=====================================================================
void flash_writeEnable(void);

//=====================================================================
//函数名称：flash_read_physical
//功能说明：从闪存读取数据块
//函数参数： pBuffer:指向缓冲区的指针
//         ReadAddr:要读取Flash的内部地址
//         NumByteToRead: 读取闪存的字节数
//函数返回：无
//=====================================================================
void flash_read_physical(uint8_t *pBuffer,uint32_t ReadAddr,uint16_t NumByteToRead);

//=====================================================================
//函数名称：flash_write_physical
//功能说明：通过SPI接口将数据块写入闪存
//函数参数： pBuffer:指向缓冲区的指针
//         WriteAddr:要写入Flash的内部地址
//         NumByteToWrite: 写入闪存的字节数
//函数返回：无
//=====================================================================
uint8_t flash_write_physical(uint32_t WriteAddr,uint16_t NumByteToWrite,uint8_t* pBuffer);

//======================================================================
//函数名称：flash_read_logic
//函数返回：无
//参数说明：dest：读出数据存放处（传地址，目的是带出所读数据，RAM区）
//       sect：扇区号（范围取决于实际芯片，例如 STM32L433:0~127,每扇区2KB）
//       offset:扇区内部偏移地址（0~2024，要求为0,4,8,12，......）
//       N：读字节数目（4~2048,要求为4,8,12,......）//
//功能概要：读取flash存储器的sect扇区的 offset处开始的N字节，到RAM区dest处
//=======================================================================
void flash_read_logic(uint8_t *dest,uint16_t sect,uint16_t offset,uint16_t N);

//======================================================================
//函数名称：flash_write
//函数返回：函数执行状态：0=正常；1=异常。
//参数说明：sect：扇区号（范围取决于实际芯片，例如 STM32L433:0~127,每扇区2KB）
//        offset:写入扇区内部偏移地址（0~2044，要求为0,4,8,12，......）
//        N：写入字节数目（4~2048,要求为4,8,12,......）
//        buf：源数据缓冲区首地址
//功能概要：将buf开始的N字节写入到flash存储器的sect扇区的 offset处
//=======================================================================
uint8_t flash_write(uint16_t sect,uint16_t offset,uint16_t N,uint8_t *buf);

//======================================================================
//函数名称：flash_erase
//函数返回：函数执行执行状态：0=正常；1=异常。
//参数说明：sect：目标扇区号;
//功能概要：擦除flash存储器的sect扇区
//======================================================================
uint8_t flash_erase(uint16_t sect);

//=====================================================================
//函数名称：flash_nand_setfeature
//功能说明：设置Nand Feature寄存器的值
//函数参数：FeaAddr：Feature寄存器的地址；value：待设置的值
//函数返回：无
//=====================================================================
void flash_nand_setfeature(uint8_t FeaAddr,uint8_t value);

//=====================================================================
//函数名称：flash_nand_getfeature
//功能说明：获取Feature寄存器的值
//函数参数：FeaAddr：Feature寄存器的地址
//函数返回：指定Feature寄存器的值
//=====================================================================
uint8_t flash_nand_getfeature(uint8_t FeaAddr);

//=====================================================================
//函数名称：flash_nand_reset
//功能说明：spi nand flash复位
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nand_reset(void);

//=====================================================================
//函数名称：flash_nand_unlock
//功能说明：解除Nand写保护
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nand_unlock(void);




#endif
