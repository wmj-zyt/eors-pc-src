#include "flash.h"

//内部函数声明
void flash_cs_low(void);
void flash_cs_high(void);
uint8_t flash_sendbyte(uint8_t byte);
void flash_nor_wait(void);
void flash_nand_wait(void);
void flash_nor_pagewrite(uint8_t* pBuffer,uint32_t WriteAddr,uint16_t NumByteToWrite);
void flash_nor_physicalerase(uint32_t SectorAddr);
void flash_nand_physicalerase(uint32_t BlockAddr);
extern int get_boot_device(void);
//=====================================================================
//函数名称：flash_init
//功能说明：SPI0模块四线SPI功能初始化,PC2:CLK,PC3:CS,PC4:MOSI,PC5:MISO
//函数参数：无
//函数返回：无
//=====================================================================
void flash_init(void)
{
    virtual_addr_t addr;
	uint32_t val;

	/* Config GPIOC2, GPIOC3, GPIOC4 and GPIOC5 */
	addr = 0x02000060 + 0x00;
	val = read32(addr);
	val &= ~(0xf << ((2 & 0x7) << 2));
	val |= ((0x2 & 0xf) << ((2 & 0x7) << 2));
	write32(addr, val);

	val = read32(addr);
	val &= ~(0xf << ((3 & 0x7) << 2));
	val |= ((0x2 & 0xf) << ((3 & 0x7) << 2));
	write32(addr, val);

	val = read32(addr);
	val &= ~(0xf << ((4 & 0x7) << 2));
	val |= ((0x2 & 0xf) << ((4 & 0x7) << 2));
	write32(addr, val);

	val = read32(addr);
	val &= ~(0xf << ((5 & 0x7) << 2));
	val |= ((0x2 & 0xf) << ((5 & 0x7) << 2));
	write32(addr, val);

	/* Deassert spi0 reset */
	addr = 0x0200196c;
	val = read32(addr);
	val |= (1 << 16);
	write32(addr, val);

    /* Open the spi0 gate */
	addr = 0x02001940;
	val = read32(addr);
	val |= (1 << 31);
	write32(addr, val);

	/* Open the spi0 bus gate */
	addr = 0x0200196c;
	val = read32(addr);
	val |= (1 << 0);
	write32(addr, val);

	/* Select pll-periph0 for spi0 clk */
	addr = 0x02001940;
	val = read32(addr);
	val &= ~(0x3 << 24);
	val |= 0x1 << 24;
	write32(addr, val);

	/* Set clock pre divide ratio, divided by 1 */
	addr = 0x02001940;
	val = read32(addr);
	val &= ~(0x3 << 8);
	val |= 0x0 << 8;
	write32(addr, val);

	/* Set clock divide ratio, divided by 6 */
	addr = 0x02001940;
	val = read32(addr);
	val &= ~(0xf << 0);
	val |= (6 - 1) << 0;
	write32(addr, val);

	/* Set spi clock rate control register, divided by 2 */
	addr = SPI0_BASE;
	write32(addr + SPI_CCR, 0x1000);

    /* Enable spi0 and do a soft reset */
	val = read32(addr + SPI_GCR);
	val |= (1 << 31) | (1 << 7) | (1 << 1) | (1 << 0); 
                                                       
	write32(addr + SPI_GCR, val);
	while(read32(addr + SPI_GCR) & (1 << 31));  

	val = read32(addr + SPI_TCR);
	val &= ~(0x3 << 0);  
	val |= (1 << 6) | (1 << 2);
	write32(addr + SPI_TCR, val);  

	val = read32(addr + SPI_FCR);
	val |= (1 << 31) | (1 << 15);
	write32(addr + SPI_FCR, val); 
	/* Get device information */
	uint8_t device=get_boot_device();
	if(device==2)
		flash_nand_unlock();
}

//=====================================================================
//函数名称：flash_writeEnable
//功能说明：写使能 
//函数参数：无
//函数返回：无
//=====================================================================
void flash_writeEnable(void)
{
	flash_cs_low();
	flash_sendbyte(WriteEnable);
	flash_cs_high();
}

//=====================================================================
//函数名称：flash_read_physical
//功能说明：从闪存读取数据块
//函数参数： pBuffer:指向缓冲区的指针
//         ReadAddr:要读取Flash的内部地址
//         NumByteToRead: 读取闪存的字节数
//函数返回：无
//=====================================================================
void flash_read_physical(uint8_t *pBuffer,uint32_t ReadAddr,uint16_t NumByteToRead)
{
	uint8_t device=get_boot_device();
	uint32_t row,col;
	uint16_t n1,n2; 
	if(device==1) //spinor
	{
		flash_cs_low();
		flash_sendbyte(NorReadData);
		flash_sendbyte((ReadAddr&0xFF0000)>>16);
		flash_sendbyte((ReadAddr&0xFF00)>>8);
		flash_sendbyte(ReadAddr&0xFF);
		while(NumByteToRead--)
		{
			*pBuffer=flash_sendbyte(NorDummy_Byte);
			pBuffer++;
		}
		flash_cs_high();
	}
	else if(device==2) //spinand
	{
		while(NumByteToRead>0)
		{
			row = ReadAddr >> NAND_PAGE_BITS;  //行地址
			col = ReadAddr & NAND_PAGE_MASK;   //列地址
			n1 = NumByteToRead > (NAND_PAGE_SIZE - col) ? (NAND_PAGE_SIZE - col) : NumByteToRead;
			n2 = n1;
			flash_cs_low();
			flash_sendbyte(NandREAD_PAGE_TO_CACHE);
			flash_sendbyte((row&0xFF0000)>>16);
 	    	flash_sendbyte((row&0xFF00)>>8);
	    	flash_sendbyte(row&0xFF);
	    	flash_cs_high();
	    	flash_nand_wait();
	    	flash_cs_low();
	    	flash_sendbyte(NandREAD_PAGE_FROM_CACHE);
 	    	flash_sendbyte((col&0xFF00)>>8);
	    	flash_sendbyte(col&0xFF);
	   	 	flash_sendbyte(NandDummy);
	   		while(n1--)
	    	{
				*pBuffer=flash_sendbyte(NandDummy);
				pBuffer++;
	    	}
	    	flash_cs_high();
	    	flash_nand_wait();
	    	ReadAddr += n2;
			NumByteToRead -= n2;
		}
	}
}

//=====================================================================
//函数名称：flash_write_physical
//功能说明：通过SPI接口将数据块写入闪存
//函数参数： pBuffer:指向缓冲区的指针
//         WriteAddr:要写入Flash的内部地址
//         NumByteToWrite: 写入闪存的字节数
//函数返回：无
//=====================================================================
uint8_t flash_write_physical(uint32_t WriteAddr,uint16_t NumByteToWrite,uint8_t* pBuffer)
{
	uint8_t NumOfPage=0,NumOfSingle=0,Addr=0,count=0,temp=0;
	uint32_t row,col;
	uint16_t n1,n2; 
	uint8_t device=get_boot_device();
	if(device==1) //spinor
	{
    	Addr=WriteAddr % NorSPI_FLASH_PageSize;  //待写入页面的页内偏移
    	count=NorSPI_FLASH_PageSize-Addr;        //
   	 	NumOfPage=NumByteToWrite / NorSPI_FLASH_PageSize;  //需要写入的总页数
   	 	NumOfSingle=NumByteToWrite % NorSPI_FLASH_PageSize; //
    	if (Addr == 0) /* WriteAddr is SPI_FLASH_PageSize aligned  */
    	{
    		if (NumOfPage == 0) /* NumByteToWrite < SPI_FLASH_PageSize */
        	{
    			flash_nor_pagewrite(pBuffer, WriteAddr, NumByteToWrite);
        	}
        	else /* NumByteToWrite > SPI_FLASH_PageSize */
        	{
        		while (NumOfPage--)
        		{
            		flash_nor_pagewrite(pBuffer, WriteAddr, NorSPI_FLASH_PageSize);
            		WriteAddr +=  NorSPI_FLASH_PageSize;
           	    	pBuffer += NorSPI_FLASH_PageSize;
        		}
            	flash_nor_pagewrite(pBuffer, WriteAddr, NumOfSingle);
        	}
    	}
    	else /* WriteAddr is not SPI_FLASH_PageSize aligned  */
    	{
        	if (NumOfPage == 0) /* NumByteToWrite < SPI_FLASH_PageSize */
        	{
        		if (NumOfSingle > count) /* (NumByteToWrite + WriteAddr) > SPI_FLASH_PageSize */
     			{
        			temp = NumOfSingle - count;
        			flash_nor_pagewrite(pBuffer, WriteAddr, count);
        			WriteAddr +=  count;
        			pBuffer += count;
        			flash_nor_pagewrite(pBuffer, WriteAddr, temp);
            	}
            	else
            	{
        			flash_nor_pagewrite(pBuffer, WriteAddr, NumByteToWrite);
            	}
        	}
    		else /* NumByteToWrite > SPI_FLASH_PageSize */
    		{
        		NumByteToWrite -= count;
        		NumOfPage =  NumByteToWrite / NorSPI_FLASH_PageSize;
        		NumOfSingle = NumByteToWrite % NorSPI_FLASH_PageSize;
        		flash_nor_pagewrite(pBuffer, WriteAddr, count);
        		WriteAddr +=  count;
        		pBuffer += count;
        		while (NumOfPage--)
        		{
        			flash_nor_pagewrite(pBuffer, WriteAddr, NorSPI_FLASH_PageSize);
        			WriteAddr +=  NorSPI_FLASH_PageSize;
        			pBuffer += NorSPI_FLASH_PageSize;
        		}
      			if (NumOfSingle != 0)
      			{
        			flash_nor_pagewrite(pBuffer, WriteAddr, NumOfSingle);
        		}
    		}
   		}
   	}
   	else if(device==2) //spinand
   	{
		while(NumByteToWrite>0)
		{
			flash_writeEnable();
			row = WriteAddr >> NAND_PAGE_BITS;  //行地址
			col = WriteAddr & NAND_PAGE_MASK;   //列地址
			n1 = NumByteToWrite > (NAND_PAGE_SIZE - col) ? (NAND_PAGE_SIZE - col) : NumByteToWrite;
			n2 = n1;
			flash_cs_low();
			flash_sendbyte(NandPROGRAM_LOAD);
			flash_sendbyte((col&0xFF00)>>8);
	    	flash_sendbyte(col&0xFF);
	    	while(n1--)
	    	{
				flash_sendbyte(*pBuffer);
				pBuffer++;
	    	}
	    	flash_cs_high();
	    	flash_nand_wait();
	    	flash_cs_low();
	    	flash_sendbyte(NandPROGRAM_EXEC);
			flash_sendbyte((row&0xFF0000)>>16);
 	    	flash_sendbyte((row&0xFF00)>>8);
	    	flash_sendbyte(row&0xFF);
	   	 	flash_cs_high();
	    	flash_nand_wait();
	    	WriteAddr += n2;
			NumByteToWrite -= n2;
		}
   	}
	return 0;
}

//======================================================================
//函数名称：flash_read_logic
//函数返回：无
//参数说明：dest：读出数据存放处（传地址，目的是带出所读数据，RAM区）
//       sect：扇区号（范围取决于实际芯片，例如 STM32L433:0~127,每扇区2KB）
//       offset:扇区内部偏移地址（0~2024，要求为0,4,8,12，......）
//       N：读字节数目（4~2048,要求为4,8,12,......）//
//功能概要：读取flash存储器的sect扇区的 offset处开始的N字节，到RAM区dest处
//=======================================================================
void flash_read_logic(uint8_t *dest,uint16_t sect,uint16_t offset,uint16_t N)
{
	uint32_t ReadAddr=0;
	uint8_t device=get_boot_device();
	if(device==1) //spinor
		ReadAddr = sect * 0x1000 + offset;
	else if (device==2) //spinand
		ReadAddr = sect * 0x800 + offset;
	flash_read_physical(dest,ReadAddr,N);
}

//======================================================================
//函数名称：flash_write
//函数返回：函数执行状态：0=正常；1=异常。
//参数说明：sect：扇区号（范围取决于实际芯片，例如 STM32L433:0~127,每扇区2KB）
//        offset:写入扇区内部偏移地址（0~2044，要求为0,4,8,12，......）
//        N：写入字节数目（4~2048,要求为4,8,12,......）
//        buf：源数据缓冲区首地址
//功能概要：将buf开始的N字节写入到flash存储器的sect扇区的 offset处
//=======================================================================
uint8_t flash_write(uint16_t sect,uint16_t offset,uint16_t N,uint8_t *buf)
{
	uint32_t WriteAddr=0;
	uint8_t device=get_boot_device();
	if(device==1) //spinor
		WriteAddr = sect * 0x1000 + offset;
	else if (device==2) //spinand
		WriteAddr = sect * 0x800 + offset;
	flash_write_physical(WriteAddr,N,buf);
	return 0;
}

//======================================================================
//函数名称：flash_erase
//函数返回：函数执行执行状态：0=正常；1=异常。
//参数说明：sect：目标扇区号;
//功能概要：擦除flash存储器的sect扇区
//======================================================================
uint8_t flash_erase(uint16_t sect)
{
	uint8_t device=get_boot_device();
	uint32_t SectorAddr;
	if(device==1) //spinor
	{	
		SectorAddr = sect * 0x1000;
		flash_nor_physicalerase(SectorAddr);
	}
	else if(device==2) //spinand
	{
		SectorAddr = sect * 0x800;
		flash_nand_physicalerase(SectorAddr);
	}
	return 0;
}

//=====================================================================
//函数名称：flash_nand_setfeature
//功能说明：设置Nand Feature寄存器的值
//函数参数：FeaAddr：Feature寄存器的地址；value：待设置的值
//函数返回：无
//=====================================================================
void flash_nand_setfeature(uint8_t FeaAddr,uint8_t value)
{
	flash_cs_low();
	flash_sendbyte(NandSET_FEATURE);
	flash_sendbyte(FeaAddr);
	flash_sendbyte(value);
    flash_cs_high();
}

//=====================================================================
//函数名称：flash_nand_getfeature
//功能说明：获取Feature寄存器的值
//函数参数：FeaAddr：Feature寄存器的地址
//函数返回：指定Feature寄存器的值
//=====================================================================
uint8_t flash_nand_getfeature(uint8_t FeaAddr)
{
	uint8_t temp;
	flash_cs_low();
	flash_sendbyte(NandGET_FEATURE);
	flash_sendbyte(FeaAddr);
	temp=flash_sendbyte(NandDummy);
    flash_cs_high();
    return temp;
}

//=====================================================================
//函数名称：flash_nand_reset
//功能说明：spi nand flash复位
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nand_reset(void)
{
	flash_cs_low();
	flash_sendbyte(NandOPCODE_RESET);
	flash_cs_high();
}

//=====================================================================
//函数名称：flash_nand_unlock
//功能说明：解除Nand写保护
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nand_unlock(void)
{
	flash_nand_setfeature(NandFEATURE_PROTECT,0x00);
}

//----------------------以下为内部函数存放处-----------------
//=====================================================================
//函数名称：flash_cs_low
//功能说明：SS_Low
//函数参数：无
//函数返回：无
//=====================================================================
void flash_cs_low(void)
{
	virtual_addr_t addr = SPI0_BASE;
	uint32_t val;
	val = read32(addr + SPI_TCR);
	val &= ~((0x3 << 4) | (0x1 << 7));
	val |= ((0 & 0x3) << 4) | (0x0 << 7);
	write32(addr + SPI_TCR, val);
}
//=====================================================================
//函数名称：flash_cs_high
//功能说明：SS_High
//函数参数：无
//函数返回：无
//=====================================================================
void flash_cs_high(void)
{
	virtual_addr_t addr = 0x04025000;
	uint32_t val;

	val = read32(addr + SPI_TCR);
	val &= ~((0x3 << 4) | (0x1 << 7));
	val |= ((0 & 0x3) << 4) | (0x1 << 7);
	write32(addr + SPI_TCR, val);
}

//=====================================================================
//函数名称：flash_sendbyte
//功能说明：通过SPI接口发送一个字节并返回从SPI总线接收到的字节
//函数参数：
//函数返回：无
//=====================================================================
uint8_t flash_sendbyte(uint8_t byte)
{
	virtual_addr_t addr=SPI0_BASE;
	uint32_t val;
	val = read32(addr+SPI_FSR);
	while((val & (0xff<<16))>>16 != 0);  //wait TXFIFO empty
	/* Send Byte */
	write32(addr + SPI_MBC, 1);
	write32(addr + SPI_MTC, 1);
	write32(addr + SPI_BCC, 1);
	write8(addr + SPI_TXD, byte);
	write32(addr + SPI_TCR, read32(addr + SPI_TCR) | (1 << 31)); 
	while((read32(addr + SPI_FSR) & 0xff) < 1); 
	return (read8(addr + SPI_RXD));  // return Byte
}

//=====================================================================
//函数名称：flash_waitforwriteend
//功能说明：等待闪存写入结束
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nor_wait(void)
{
	uint8_t FLASH_Status = 0;
	flash_cs_low();
	flash_sendbyte(NorReadStatusReg);
	do
  	{
    	FLASH_Status=flash_sendbyte(NorDummy_Byte);
  	}while((FLASH_Status & NorWIP_Flag) ==1);
	flash_cs_high();
}

//=====================================================================
//函数名称：flash_nand_wait
//功能说明：等待SPI Nand Flash
//函数参数：无
//函数返回：无
//=====================================================================
void flash_nand_wait(void)
{
	uint8_t temp;
	do{
		flash_cs_low();
		flash_sendbyte(NandGET_FEATURE);
		flash_sendbyte(NandFEATURE_STATUS);
		temp=flash_sendbyte(NandDummy);
    	flash_cs_high();
	}while((temp & 0x1) == 0x1);
}

//=====================================================================
//函数名称：flash_nor_pagewrite
//功能说明：通过SPI接口将页写入闪存
//函数参数： pBuffer:指向缓冲区的指针
//         WriteAddr:要写入Flash的内部地址
//         NumByteToWrite: 写入闪存的字节数
//函数返回：无
//=====================================================================
void flash_nor_pagewrite(uint8_t* pBuffer,uint32_t WriteAddr,uint16_t NumByteToWrite)
{
	flash_writeEnable();
	flash_cs_low();
	//页编程指令
	flash_sendbyte(NorPageProgram);
	//发送高8位地址
	flash_sendbyte((WriteAddr&0xFF0000)>>16);
	//发送中8位地址
	flash_sendbyte((WriteAddr&0xFF00)>>8);
	//发送低8位地址
	flash_sendbyte(WriteAddr&0xFF);
	if(NumByteToWrite>NorSPI_FLASH_PageSize)
	{
		NumByteToWrite=NorSPI_FLASH_PageSize;
	}
	while(NumByteToWrite--)
	{
		flash_sendbyte(*pBuffer);
		pBuffer++;
	}
	flash_cs_high();
	flash_nor_wait();
}

//=====================================================================
//函数名称：flash_nor_physicalerase
//功能说明：从指定地址开始，擦除4KB
//函数参数：待擦除地址
//函数返回：无
//=====================================================================
void flash_nor_physicalerase(uint32_t SectorAddr)
{
	flash_writeEnable();
	flash_cs_low();
	flash_sendbyte(NorSectorErase);
	flash_sendbyte((SectorAddr & 0xFF0000)>>16);
	flash_sendbyte((SectorAddr & 0xFF00)>>8);
	flash_sendbyte(SectorAddr & 0xFF);
	flash_cs_high();
	flash_nor_wait();
}

//=====================================================================
//函数名称：flash_nand_physicalerase
//功能说明：擦除指定地址所在的块，一个块128KB
//函数参数：待擦除地址
//函数返回：无
//=====================================================================
void flash_nand_physicalerase(uint32_t BlockAddr)
{
	uint32_t row = BlockAddr >> NAND_PAGE_BITS; 
	flash_writeEnable();
	flash_cs_low();
	flash_sendbyte(NandBLOCK_ERASE);
	flash_sendbyte((row & 0xFF0000)>>16);
	flash_sendbyte((row & 0xFF00)>>8);
	flash_sendbyte(row & 0xFF);
	flash_cs_high();
	flash_nand_wait();
}