#include <interr.h>
#include "printf.h"
/* 中断服务函数表 */
static sys_irq_handle_t irqTable[NUMBER_OF_INT_VECTORS];

/*
 * @description	: 中断初始化函数
 * @param		: 无
 * @return 		: 无
 */
void int_init(void)
{
    PLIC_Init();              //初始化 PLIC
    system_irqtable_init();	  //初始化中断表
}


/*
 * @description	: 初始化中断服务函数表 
 * @param		: 无
 * @return 		: 无
 */
void system_irqtable_init(void)
{
	unsigned int i = 0;
	
	/* 先将所有的中断服务函数设置为默认值 */
	for(i = 0; i < NUMBER_OF_INT_VECTORS; i++)
	{
		system_register_irqhandler((IRQn_Type)i,default_irqhandler, NULL);
	} 
}

/*
 * @description			: 给指定的中断号注册中断服务函数 
 * @param - irq			: 要注册的中断号
 * @param - handler		: 要注册的中断处理函数
 * @param - usrParam	: 中断服务处理函数参数
 * @return 				: 无
 */
void system_register_irqhandler(IRQn_Type irq, system_irq_handler_t handler, void *userParam) 
{
	irqTable[irq].irqHandler = handler;
  	irqTable[irq].userParam = userParam;
}

/*
 * @description			: C语言中断服务函数，irq汇编中断服务函数会
 						  调用此函数，此函数通过在中断服务列表中查
 						  找指定中断号所对应的中断处理函数并执行。
 * @param - giccIar		: 中断号
 * @return 				: 无
 */
void system_irqhandler(void) 
{
   uint32_t IRQID=read32(PLIC_MCLAIM);
   /* 检查中断号是否符合要求 */
   if ((IRQID <0) || (IRQID >= NUMBER_OF_INT_VECTORS))
   {
	 	return;
   }
   /* 根据传递进来的中断号，在irqTable中调用确定的中断服务函数*/
   irqTable[IRQID].irqHandler(IRQID, irqTable[IRQID].userParam);
   write32(PLIC_MCLAIM, IRQID);
}



/*
 * @description			: 默认中断服务函数
 * @param - giccIar		: 中断号
 * @param - usrParam	: 中断服务处理函数参数
 * @return 				: 无
 */
void default_irqhandler(unsigned int giccIar, void *userParam) 
{
	while(1) 
  	{
   	}
}

/*******************************************************************************
* Function Name  : PLIC_SetPriority
* Description    : Set Interrupt Priority
* Input          : IRQn: Interrupt Numbers
*                  priority: bit4-bit0: priority
* Return         : None
*******************************************************************************/
void  PLIC_SetPriority(IRQn_Type IRQn, uint8_t priority)
{
	virtual_addr_t addr;
	addr=PLIC_PRIO(IRQn);
	write32(addr, priority);
}

/*******************************************************************************
* Function Name  : PLIC_MIE_DisableIRQ
* Description    : Machine Disable Interrupt
* Input          : IRQn: Interrupt Numbers
* Return         : None
*******************************************************************************/
void PLIC_MIE_DisableIRQ(IRQn_Type IRQn)
{
	uint32_t val;
    val = read32(PLIC_MIE(IRQn >> 5));
    val &= ~(1 << (IRQn & 0x1f));
	write32(PLIC_MIE(IRQn >> 5), val);
}

/*******************************************************************************
* Function Name  : PLIC_MIE_EnableIRQ
* Description    : Enable Interrupt
* Input          : IRQn: Interrupt Numbers
* Return         : None
*******************************************************************************/
void PLIC_MIE_EnableIRQ(IRQn_Type IRQn)
{
	uint32_t val;
    val = read32(PLIC_MIE(IRQn >> 5));
    val |= (1 << (IRQn & 0x1f));
	write32(PLIC_MIE(IRQn >> 5), val);
}

/*******************************************************************************
* Function Name  : PLIC_SetPendingIRQ
* Description    : Set Interrupt Pending
* Input          : IRQn: Interrupt Numbers
* Return         : None
*******************************************************************************/
void PLIC_SetPendingIRQ(IRQn_Type IRQn)
{
	uint32_t val;
    val = read32(PLIC_IP(IRQn >> 5));
    val |= (1 << (IRQn & 0x1f));
	write32(PLIC_IP(IRQn >> 5), val);
}


/*******************************************************************************
* Function Name  : PLIC_Init
* Description    : PLIC INIT
* Input          : None
* Return         : None
*******************************************************************************/
void PLIC_Init(void)
{
    uint32_t val;
    int i;
    /*
	 * Disable all interrupts
	 */
    for(i=0;i<NUMBER_OF_INT_VECTORS;i++)
    {
        val = read32(PLIC_MIE(i >> 5));
        val &= ~(1 << (i & 0x1f));
		write32(PLIC_MIE(i >> 5), val);
    }
    /*
	 * Set all source priorities to one
	 */
    for(i = 1; i < NUMBER_OF_INT_VECTORS; i++)
	{
		write32(PLIC_PRIO(i), 1);
	}
    /*
	 * Clear pending bits
	 */
	for(i = 0; i < NUMBER_OF_INT_VECTORS; i++)
	{
		write32(PLIC_MCLAIM, i);
	}
}

/*******************************************************************************
* Function Name  : SYS_ResetExecute
* Description    : 执行系统软件复位
* Input          : None
* Return         : None
*******************************************************************************/
void Sys_ResetExecute(void)
{
    WDOG_SOFT_RST = 0x16aa0001;
}

