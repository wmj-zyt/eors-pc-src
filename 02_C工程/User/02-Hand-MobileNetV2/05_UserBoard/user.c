///=====================================================================
//文件名称：user.c文件
//框架提供：苏州大学嵌入式系统与物联网研究所（sumcu.suda.edu.cn）
//更新记录：20220525
//移植规则：【固定】
//=====================================================================
#include "user.h"  //【CC-220102】

extern uint64_t handle_trap(uint64_t Mcause,uint64_t epc, uint64_t sp);

void defaultProgarm(void);

//=====================================================================
//函数名称：handle_trap
//功能说明：更具中断或异常的类型，执行不同的处理函数
//函数参数：Mcause:中断或异常的类型
//          epc：中断或异常返回地址
//函数返回：中断或异常返回地址
//=====================================================================
#define SW_Handler ((void (*)(uint64_t))(component_fun[28])) 
#define tick_tick ((void (*)(void))(component_fun[27]))
uint64_t handle_trap(uint64_t Mcause,uint64_t epc, uint64_t sp)
{
	if(Mcause & (1UL << 63))
	{
		unsigned long cause = Mcause & ~(1UL << 63);
		unsigned long pending = csr_read(mip) & (1 << cause);
		
		switch(cause)
		{
		case 0:		/* User software interrupt */
		case 1:		/* Supervisor software interrupt */
		case 2:		/* Hypervisor software interrupt */
		case 3:		/* Machine software interrupt */
			csr_clear(mip, pending);
			SW_Handler(sp);
			break;
		case 4:		/* User timer interrupt */
		case 5:		/* Supervisor timer interrupt */
		case 6:		/* Hypervisor timer interrupt */
		case 7:		/* Machine timer interrupt */
			csr_clear(mip, pending);
			tick_tick();
			break;
		case 8:		/* User external interrupt */
		case 9:		/* Supervisor external interrupt */
		case 10:	/* Hypervisor external interrupt */
		case 11:	/* Machine external interrupt */
			csr_clear(mip, pending);
			system_irqhandler();
			break;
		default:
			break;
		}
	}
	else
	{
		switch(Mcause)
		{
		case 0x0:	/* Misaligned fetch */
		case 0x1:	/* Fetch access */
		case 0x2:	/* Illegal instruction */
		case 0x3:	/* Breakpoint */
			defaultProgarm();
			break;
		case 0x4:	/* Misaligned load */
			defaultProgarm();
			break;
		case 0x5:	/* Load acces */
			defaultProgarm();
			break;
		case 0x6:	/* Misaligned store */
			defaultProgarm();
			break;
		case 0x7:	/* Store accesss */
		case 0x8:	/* User ecall */
		case 0x9:	/* Supervisor ecall */
		case 0xa:	/* Hypervisor ecall */
		case 0xb:	/* Machine ecall */
			defaultProgarm();
			break;
		default:
			defaultProgarm();
			break;
		}
	}
	return epc;
}


uint32_t __get_MEPC(void)
{
  uint32_t result;

  __asm volatile ( "csrr %0," "mepc" : "=r" (result) );
  return (result);
}
uint32_t __get_MCAUSE(void)
{
  uint32_t result;

  __asm volatile ( "csrr %0," "mcause" : "=r" (result) );
  return (result);
}
uint32_t __get_MTVAL(void)
{
  uint32_t result;

  __asm volatile ( "csrr %0," "mtval" : "=r" (result) );
  return (result);
}
void defaultProgarm(void)
{
  printf("mcause:%08x\r\n",__get_MCAUSE());
  printf("mepc:%08x\r\n",__get_MEPC());
  printf("mtval:%08x\r\n",__get_MTVAL());

  while (1)
  {

  }
}

//=====================================================================
//函数名称：register_irqhandler
//函数返回：无
//参数说明：无
//功能概要：注册中断服务函数
//=====================================================================
#define UART2_Handler  ((void (*)(void))(component_fun[26]))
void register_irqhandler(void)
{
    system_register_irqhandler(D1_IRQ_UART0,(system_irq_handler_t)UART0_Handler,NULL);
    system_register_irqhandler(D1_IRQ_UART2,(system_irq_handler_t)UART2_Handler,NULL);
    system_register_irqhandler(D1_IRQ_TIMER0,(system_irq_handler_t)TIMER0_Handler,NULL);
    system_register_irqhandler(D1_IRQ_GPIOE_NS,(system_irq_handler_t)D1_GPIOE_Handler,NULL);
 }

//=====================================================================
//函数名称：uart_relate
//函数返回：无
//参数说明：无
//功能概要：UART_Debug串口初始化与使能
//=====================================================================
void uart_relate(void)
{
	uart_init(UART_Debug, 1500000);     //UART_Debug串口初始化
	uart_enable_re_int(UART_Debug);    //UART_Debug串口使能
}
