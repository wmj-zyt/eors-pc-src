#include <uart.h>

//内部函数声明
uint8_t uart_is_uartNo(uint8_t uartNo);

//======================================================================
//函数名称：uart_init
//功能概要：初始化uart模块
//参数说明：uartNo:串口号：UART_1、UART_2、UART_3
//          baud:波特率：300、600、1200、2400、4800、9600、19200、115200...
//函数返回：无
//======================================================================
void uart_init(uint8_t uartNo, uint32_t baud_rate)
{
    virtual_addr_t addr; 
    uint32_t val;
    uint8_t LDivisor,HDivisor;
    virtual_addr_t UART_BASE;
    //判断传入串口号参数是否有误,有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return;
	}
    switch(uartNo)
    {
        case 0:  //uart0, tx:PB8,rx:PB9
            /* Open the clock gate for uart0 ,Deassert uart0 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 0)|(0x1<<16);
	        write32(addr, val);

            /* Config GPIOB8 and GPIOB9 to tx and rx */
	        addr = 0x02000034;
	        val = read32(addr);
	        val &= ~(0xf<<0);
	        val |= (0x6<<0);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 4);
	        val |= (0x6 << 4);
	        write32(addr, val);
            UART_BASE=UART0_BASE;
            break;
        case 1: //uart1, tx:PD21,rx:PD22
            /* Open the clock gate for uart1 ,Deassert uart1 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 1)|(0x1<<17);
	        write32(addr, val);

            /* Config GPIOD21 and GPIOD22 to tx and rx */
	        addr = 0x02000098;
	        val = read32(addr);
	        val &= ~(0xf<<20);
	        val |= (0x4<<20);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 24);
	        val |= (0x4 << 24);
	        write32(addr, val);
            UART_BASE=UART1_BASE;
            break;
        case 2: //uart2, tx:PB0,rx:PB1
            /* Open the clock gate for uart2 ,Deassert uart2 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 2)|(0x1<<18);
	        write32(addr, val);

            /* Config GPIOB0 and GPIOB1 to tx and rx */
	        addr = 0x02000030;
	        val = read32(addr);
	        val &= ~(0xf<<0);
	        val |= (0x7<<0);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 4);
	        val |= (0x7 << 4);
	        write32(addr, val);
            UART_BASE=UART2_BASE;
            break;
        case 3: //uart3, tx:PD10,rx:PD11
            /* Open the clock gate for uart3 ,Deassert uart3 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 3)|(0x1<<19);
	        write32(addr, val);

            /* Config GPIOD10 and GPIOD11 to tx and rx */
	        addr = 0x02000094;
	        val = read32(addr);
	        val &= ~(0xf<<8);
	        val |= (0x5<<8);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 12);
	        val |= (0x5 << 12);
	        write32(addr, val);
            UART_BASE=UART3_BASE;
            break;
        case 4:  //uart4, tx:PB2,rx:PB3
            /* Open the clock gate for uart4 ,Deassert uart4 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 4)|(0x1<<20);
	        write32(addr, val);

            /* Config GPIOB2 and GPIOB3 to tx and rx */
	        addr = 0x02000030;
	        val = read32(addr);
	        val &= ~(0xf<<8);
	        val |= (0x7<<8);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 12);
	        val |= (0x7 << 12);
	        write32(addr, val);
            UART_BASE=UART4_BASE;
            break;
        case 5: //uart5, tx:PG4,rx:PG5
            /* Open the clock gate for uart5 ,Deassert uart5 reset*/
	        addr = 0x0200190c;
	        val = read32(addr);
	        val |= (0x1 << 5)|(0x1<<21);
	        write32(addr, val);

            /* Config GPIOG4 and GPIOG5 to tx and rx */
	        addr = 0x02000120;
	        val = read32(addr);
	        val &= ~(0xf<<16);
	        val |= (0x3<<16);
	        write32(addr, val);

	        val = read32(addr);
	        val &= ~(0xf << 20);
	        val |= (0x3 << 20);
	        write32(addr, val);
            UART_BASE=UART5_BASE;
            break;
    }
    /* Set UART mode */
    addr = UART_BASE;
    val = read32(addr+UART_MCR);
    val &= ~(0x3<<6);
    write32(addr+UART_MCR,val);
    /* FIFO enable */
    val = read32(addr+UART_FCR);
    val |= (0x1<<0);
    write32(addr+UART_FCR,val);
    /* Disable TX transfer */
    val = read32(addr+UART_HALT);
    val |= (0x1<<0);
    write32(addr+UART_HALT,val);
    /* Set baud */
    val = read32(addr+UART_LCR);
    val |= (0x1 << 7);
    write32(addr+UART_LCR,val);
    LDivisor=1500000/baud_rate;
    HDivisor=(1500000/baud_rate)>>8;
    write32(addr+UART_DLL,LDivisor);
    write32(addr+UART_DLH,HDivisor);
    val = read32(addr+UART_LCR);
    val &= ~(0x1 << 7);
    write32(addr+UART_LCR,val);
    /* Set Parity disabled,1 stop bit,8 data bits  */
    val = read32(addr + UART_LCR);
    val &= ~0x1f;
    val |= (0x3 << 0) | (0x0 << 2) | (0x0 << 3);
    write32(addr + UART_LCR, val);
    /* Enable TX transfer */
    val = read32(addr+UART_HALT);
    val &= ~(0x1<<0);
    write32(addr+UART_HALT,val);
}

//======================================================================
//函数名称：uart_send1
//参数说明：uartNo: 串口号:UART_1、UART_2、UART_3
//          ch:要发送的字节
//函数返回：函数执行状态：1=发送成功；0=发送失败。
//功能概要：串行发送1个字节
//======================================================================
uint8_t uart_send1(uint8_t uartNo, uint8_t ch)
{
    virtual_addr_t addr; 
    uint32_t t;
    //判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return 0;
	}
    switch(uartNo)
    {
        case 0:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART0_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
        case 1:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART1_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
        case 2:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART2_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
        case 3:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART3_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
        case 4:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART4_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
        case 5:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART5_BASE;
                if(read32(addr+UART_USR) & (0x1<<1))
                {
                    write32(addr + UART_THR, ch);
                    break;
                }
            }
            if(t>=0xFBBB)
                return 0;
            else
                return 1;
            break;
    }
    return 0;
}

//======================================================================
//函数名称：uart_sendN
//参数说明：uartNo: 串口号:UART_1、UART_2、UART_3
//         buff: 发送缓冲区
//         len:发送长度
//函数返回： 函数执行状态：1=发送成功；0=发送失败
//功能概要：串行 接收n个字节
//======================================================================
uint8_t uart_sendN(uint8_t uartNo ,uint32_t len ,uint8_t* buff)
{
    uint32_t i;

    //判断传入串口号参数是否有误，有误直接退出
    if(!uart_is_uartNo(uartNo))
    {
        return 0;
    }

    for (i = 0; i < len; i++)
    {
        if (!uart_send1(uartNo, buff[i])) //发送一个字节数据，失败则跳出循环
        {
            break;
        }
    }
    if(i<len)
        return 0;    //发送出错
    else
        return 1;    //发送出错
}

//======================================================================
//函数名称：uart_send_string
//参数说明：uartNo:UART模块号:UART_1、UART_2、UART_3
//          buff:要发送的字符串的首地址
//函数返回： 函数执行状态：1=发送成功；0=发送失败
//功能概要：从指定UART端口发送一个以'\0'结束的字符串
//======================================================================
uint8_t uart_send_string(uint8_t uartNo, uint8_t* buff)
{
    uint16_t i = 0;
    uint8_t *buff_ptr = (uint8_t *)buff;     //定义指针指向要发送字符串首地址

    //判断传入串口号参数是否有误，有误直接退出
    if(!uart_is_uartNo(uartNo))
    {
        return 0;
    }

    for(i = 0; buff_ptr[i] != '\0'; i++)   //遍历字符串里的字符
    {
        if (!uart_send1(uartNo,buff_ptr[i]))//发送指针对应的字符
            return 0;  //发送失败,返回
    }
    return 1;          //发送成功
}

//======================================================================
//函数名称：uart_re1
//参数说明：uartNo: 串口号:UART_1、UART_2、UART_3
//        *fp:接收成功标志的指针:*fp=1:接收成功；*fp=0:接收失败
//函数返回：接收返回字节
//功能概要：串行接收1个字节
//======================================================================
uint8_t uart_re1(uint8_t uartNo,uint8_t *fp)
{
    uint32_t t;
    uint8_t  dat;
    virtual_addr_t addr; 
	//判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		*fp=0;
		return 0;
	}
    switch(uartNo)
    {
        case 0:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART0_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break; 
        case 1:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART1_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break;
        case 2:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART2_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break;
        case 3:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART3_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break;
        case 4:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART4_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break;
        case 5:
            for(t=0;t<0xFBBB;t++)  //查询指定次数
            {
                addr=UART5_BASE;
                if(read32(addr+UART_USR) & (0x1<<3))
                {
                    dat=read32(addr+UART_RBR);
                    *fp = 1;
                    break;
                }
            }
            if(t>=0xFBBB)
            {
                dat = 0xFF;
                *fp = 0;
            }
            break;
    }
    return dat;
}


//======================================================================
//函数名称：uart_reN
//参数说明：uartNo: 串口号:UART_1、UART_2、UART_3
//          buff: 接收缓冲区
//          len:接收长度
//函数返回：函数执行状态 1=接收成功;0=接收失败
//功能概要：串行 接收n个字节,放入buff中
//======================================================================
uint8_t uart_reN(uint8_t uartNo ,uint16_t len ,uint8_t* buff)
{
    uint16_t i;
	uint8_t flag = 0;

	//判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return 0;
	}

	//判断是否能接受数据
	for (i = 0; i < len && flag==1; i++)
	{
		buff[i] = uart_re1(uartNo, &flag); //接受数据
	}
	if (i < len)
		return 0; //接收失败
	else
		return 1; //接收成功
}

//======================================================================
//函数名称：uart_enable_re_int
//参数说明：uartNo: 串口号:UART_1、UART_2、UART_3
//函数返回：无
//功能概要：开串口接收中断
//======================================================================
void uart_enable_re_int(uint8_t uartNo)
{
    virtual_addr_t addr; 
    uint32_t val;
    //判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return;
	}
    switch(uartNo)
    {
        case 0:
            addr=UART0_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART0);
            break;
        case 1:
            addr=UART1_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART1);
            break;
        case 2:
            addr=UART2_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART2);
            break;
        case 3:
            addr=UART3_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART3);
            break;
        case 4:
            addr=UART4_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART4);
            break;
        case 5:
            addr=UART5_BASE;
            val=read32(addr+UART_IER);
            val |= (0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_EnableIRQ(D1_IRQ_UART5);
            break;
    }
}

//======================================================================
//函数名称：uart_disable_re_int
//参数说明：uartNo: 串口号 :UART_1、UART_2、UART_3
//函数返回：无
//功能概要：关串口接收中断
//======================================================================
void uart_disable_re_int(uint8_t uartNo)
{
    virtual_addr_t addr; 
    uint32_t val;
    //判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return;
	}
    switch(uartNo)
    {
        case 0:
            addr=UART0_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART0);
            break;
        case 1:
            addr=UART1_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART1);
            break;
        case 2:
            addr=UART2_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART2);
            break;
        case 3:
            addr=UART3_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART3);
            break;
        case 4:
            addr=UART4_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART4);
            break;
        case 5:
            addr=UART5_BASE;
            val=read32(addr+UART_IER);
            val &= ~(0x1<<0);
            write32(addr+UART_IER,val);  //Enable Received Data Available Interrupt 
            PLIC_MIE_DisableIRQ(D1_IRQ_UART5);
            break;
    }
}

//======================================================================
//函数名称：uart_get_re_int
//参数说明：uartNo: 串口号 :UART_1、UART_2、UART_3
//函数返回：接收中断标志 1=有接收中断;0=无接收中断
//功能概要：获取串口接收中断标志
//======================================================================
uint8_t uart_get_re_int(uint8_t uartNo)
{
    virtual_addr_t addr; 
    uint32_t val;
    //判断传入串口号参数是否有误，有误直接退出
	if(!uart_is_uartNo(uartNo))
	{
		return 0;
	}
    switch(uartNo)
    {
        case 0:
            addr=UART0_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
        case 1:
            addr=UART1_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
        case 2:
            addr=UART2_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
        case 3:
            addr=UART3_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
        case 4:
            addr=UART4_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
        case 5:
            addr=UART5_BASE;
            val=read32(addr+UART_IIR);
            if((val & 0x4)==0x4)
                return 1;
            else
                return 0;
            break;
    }
    return 0;
}


//----------------------以下为内部函数存放处--------------------------------------
//=====================================================================
//函数名称：uart_is_uartNo
//函数返回：1:串口号在合理范围内，0：串口号不合理
//参数说明：串口号uartNo  :UART_1、UART_2、UART_3
//功能概要：为程序健壮性而判断uartNo是否在串口数字范围内
//=====================================================================
uint8_t uart_is_uartNo(uint8_t uartNo)
{
    if(uartNo < UART_0 || uartNo > UART_5)
        return 0;
    else
        return 1;
}
