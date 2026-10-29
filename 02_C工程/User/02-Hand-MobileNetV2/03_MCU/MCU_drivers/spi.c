#include <spi.h>

//内部函数声明
void spi_cs_low(uint8_t No);
void spi_cs_high(uint8_t No);
static int sys_spi_transfer(void * txbuf, void * rxbuf, int len);
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
		uint8_t CPOL,uint8_t CPHA)
{
    virtual_addr_t addr;
	uint32_t val;
	if(No<SPI_0 || No>SPI_1) No=SPI_1;
	switch(No)
	{
		case SPI_1:
			/* Config PD10, PD11, PD12 and PD13 */
			addr = 0x02000094;
			val = read32(addr);
			val &= ~(0xf << 8);
			val |= (0x4 << 8);
			write32(addr, val);
	
			val = read32(addr);
			val &= ~(0xf << 12);
			val |= (0x4 << 12);
			write32(addr, val);

			val = read32(addr);
			val &= ~(0xf << 16);
			val |= (0x4 << 16);
			write32(addr, val);
	
			val = read32(addr);
			val &= ~(0xf << 20);
			val |= (0x4 << 20);
			write32(addr, val);
			
			/* Deassert spi1 reset */
			addr = 0x0200196c;
			val = read32(addr);
			val |= (1 << 17);
			write32(addr, val);
			
			
    		/* Open the spi1 gate */
			addr = 0x02001944;
			val = read32(addr);
			val |= (1 << 31);
			write32(addr, val);

			/* Open the spi1 bus gate */
			addr = 0x0200196c;
			val = read32(addr);
			val |= (1 << 1);
			write32(addr, val);
			
			/* Select pll-periph0 for spi0 clk */
			addr = 0x02001944;
			val = read32(addr);
			val &= ~(0x3 << 24);
			val |= 0x1 << 24;
			write32(addr, val);
			
			/* Set clock pre divide ratio, divided by 1 */
			addr = 0x02001944;
			val = read32(addr);
			val &= ~(0x3 << 8);
			val |= 0x0 << 8;
			write32(addr, val);

			/* Set clock divide ratio, divided by 12 */
			addr = 0x02001944;
			val = read32(addr);
			val &= ~(0xf << 0);
			val |= (12 - 1) << 0;
			write32(addr, val);
			
			/* Set spi clock rate control register, divided by 2 */
			addr = SPI_DBI_BASE;
			write32(addr + SPI_CCR, 0x1000);
			
			/* Enable spi0 and do a soft reset */
			val = read32(addr + SPI_GCR);
			val |= (1 << 31) | (1 << 7) | (1 << 0); //clear the SPI controller,
                                                       //Stop transmit data when RXFIFO full,SPI Module Enable
            val &=~(1<<3); //SPI Mode
            if(MSTR == 1)    //主机模式
            	val |= (1 << 1);
            else             //从机模式
            	val &= ~(1<<1);
            write32(addr + SPI_GCR, val);
	        while(read32(addr + SPI_GCR) & (1 << 31));  // wait clear the SPI controller complete
            
            val = read32(addr + SPI_TCR);
            val |= (1 << 6) | (1 << 2);  //Soft control SS
            val &= ~(0x3 << 0);
            if(CPOL == 1) //极性
            	val |= (1 << 1);
            else
            	val &= ~(1 << 1);
            if(CPHA == 1)  //相位
            	val |= (1 << 0);
            else
            	val &= ~(1 << 0);
            write32(addr + SPI_TCR, val);
			
			val = read32(addr + SPI_FCR);
			val |= (1 << 31) | (1 << 15);
			write32(addr + SPI_FCR, val);  //TXFIFO RXFIFO reset
			
			break;
	}
}

//=====================================================================
//函数名称：spi_send1.
//功能说明：SPI发送一字节数据。
//函数参数：No：模块号
//       data： 需要发送的一字节数据。
//函数返回：0：发送失败；1：发送成功。
//=====================================================================
uint8_t spi_send1(uint8_t No,uint8_t data)
{
	uint8_t *tx=&data;
	sys_spi_transfer(tx,NULL,1);
	return 1;
}

//----------------------以下为内部函数存放处-----------------
//=====================================================================
//SPI_FLASH_CS_LOW
//功能说明：SS_Low
//函数参数：无
//函数返回：无
//=====================================================================
void spi_cs_low(uint8_t No)
{
	virtual_addr_t addr = SPI_DBI_BASE;
	uint32_t val;
	switch(No)
	{
		case SPI_0:
			addr = SPI0_BASE;
			break;
		case SPI_1:
			addr = SPI_DBI_BASE;
			break;
	}
	val = read32(addr + SPI_TCR);
	val &= ~((0x3 << 4) | (0x1 << 7));
	val |= ((0 & 0x3) << 4) | (0x0 << 7);
	write32(addr + SPI_TCR, val);
}
//=====================================================================
//SPI_FLASH_CS_HIGH
//功能说明：SS_High
//函数参数：无
//函数返回：无
//=====================================================================
void spi_cs_high(uint8_t No)
{
	virtual_addr_t addr = SPI_DBI_BASE;
	uint32_t val;
	switch(No)
	{
		case SPI_0:
			addr = SPI0_BASE;
			break;
		case SPI_1:
			addr = SPI_DBI_BASE;
			break;
	}
	val = read32(addr + SPI_TCR);
	val &= ~((0x3 << 4) | (0x1 << 7));
	val |= ((0 & 0x3) << 4) | (0x1 << 7);
	write32(addr + SPI_TCR, val);
}


static void sys_spi_write_txbuf(uint8_t * buf, int len)
{
	virtual_addr_t addr = SPI_DBI_BASE;
	int i;

	write32(addr + SPI_MTC, len & 0xffffff);
	write32(addr + SPI_BCC, len & 0xffffff);
	if(buf)
	{
		for(i = 0; i < len; i++)
			write8(addr + SPI_TXD, *buf++);
	}
	else
	{
		for(i = 0; i < len; i++)
			write8(addr + SPI_TXD, 0xff);
	}
}


static int sys_spi_transfer(void * txbuf, void * rxbuf, int len)
{
	virtual_addr_t addr = SPI_DBI_BASE;
	int count = len;
	uint8_t * tx = txbuf;
	uint8_t * rx = rxbuf;
	uint8_t val;
	int n, i;

	while(count > 0)
	{
		n = (count <= 64) ? count : 64;
		write32(addr + SPI_MBC, n);
		sys_spi_write_txbuf(tx, n);
		write32(addr + SPI_TCR, read32(addr + SPI_TCR) | (1 << 31));

		while((read32(addr + SPI_FSR) & 0xff) < n);
		for(i = 0; i < n; i++)
		{
			val = read8(addr + SPI_RXD);
			if(rx)
				*rx++ = val;
		}

		if(tx)
			tx += n;
		count -= n;
	}
	return len;
}
