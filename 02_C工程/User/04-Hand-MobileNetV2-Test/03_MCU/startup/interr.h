#ifndef __IN_H__
#define __IN_H__

#include "cpu.h"
#include "stddef.h"
#include "stdint.h"
#define WDOG_SOFT_RST  *((volatile unsigned int *)0x020500A8)

#define PLIC_PRIO(x)		(0x10000000 + (x) * 4)
#define PLIC_IP(x)			(0x10001000 + (x) * 4)
#define PLIC_MIE(x)			(0x10002000 + (x) * 4)
#define PLIC_SIE(x)			(0x10002080 + (x) * 4)
#define PLIC_CTRL			(0x101ffffc)
#define PLIC_MTH			(0x10200000)
#define PLIC_MCLAIM			(0x10200004)
#define PLIC_STH			(0x10201000)
#define PLIC_SCLAIM			(0x10201004)

#define NUMBER_OF_INT_VECTORS (256)

#ifdef __cplusplus
extern "C" {
#endif
typedef enum IRQn
{
 D1_IRQ_UART0			=18,
 D1_IRQ_UART1			=19,
 D1_IRQ_UART2			=20,
 D1_IRQ_UART3			=21,
 D1_IRQ_UART4			=22,
 D1_IRQ_UART5			=23,
 D1_IRQ_TWI0		    =25,
 D1_IRQ_TWI1		    =26,
 D1_IRQ_TWI2		    =27,
 D1_IRQ_TWI3			=28,
 D1_IRQ_SPI0			=31,
 D1_IRQ_SPI1			=32,
 D1_IRQ_PWM				=34,
 D1_IRQ_IR_TX			=35,
 D1_IRQ_LEDC			=36,
 D1_IRQ_OWA				=39,
 D1_IRQ_DMIC			=40,
 D1_IRQ_AUDIO_CODEC		=41,
 D1_IRQ_I2S0			=42,
 D1_IRQ_I2S1			=43,
 D1_IRQ_I2S2			=44,
 D1_IRQ_USB0_DEVICE		=45,
 D1_IRQ_USB0_EHCI		=46,
 D1_IRQ_USB0_OHCI		=47,
 D1_IRQ_USB1_EHCI		=49,
 D1_IRQ_USB1_OHCI		=50,
 D1_IRQ_SMHC0			=56,
 D1_IRQ_SMHC1			=57,
 D1_IRQ_SMHC2			=58,
 D1_IRQ_MSI				=59,
 D1_IRQ_EMAC			=62,
 D1_IRQ_ECCU_FERR		=64,
 D1_IRQ_AHB_TIMEOUT		=65,
 D1_IRQ_DMAC_NS			=66,
 D1_IRQ_CE_NS			=68,
 D1_IRQ_SPINLOCK		=70,
 D1_IRQ_HSTIME0			=71,
 D1_IRQ_HSTIME1			=72,
 D1_IRQ_GPADC			=73,
 D1_IRQ_THS				=74,
 D1_IRQ_TIMER0			=75,
 D1_IRQ_TIMER1			=76,
 D1_IRQ_LRADC			=77,
 D1_IRQ_TPADC			=78,
 D1_IRQ_WATCHDOG		=79,
 D1_IRQ_IOMMU			=80,
 D1_IRQ_VE				=82,
 D1_IRQ_GPIOB_NS		=85,
 D1_IRQ_GPIOC_NS		=87,
 D1_IRQ_GPIOD_NS		=89,
 D1_IRQ_GPIOE_NS		=91,
 D1_IRQ_GPIOF_NS		=93,
 D1_IRQ_GPIOG_NS	    =95,
 D1_IRQ_DE				=103,
 D1_IRQ_DI				=104,
 D1_IRQ_G2D				=105,
 D1_IRQ_LCD				=106,
 D1_IRQ_TV				=107,
 D1_IRQ_DSI				=108,
 D1_IRQ_HDMI			=109,
 D1_IRQ_TVE				=110,
 D1_IRQ_CSI_DMA0		=111,
 D1_IRQ_CSI_DMA1		=112,
 D1_IRQ_CSI_PARSER0		=116,
 D1_IRQ_CSI_TOP_PKT		=122,
 D1_IRQ_TVD				=123,
 D1_IRQ_DSP_DFE			=136,
 D1_IRQ_DSP_PFE			=137,
 D1_IRQ_DSP_WDG			=138,
 D1_IRQ_DSP_MBOX_RISCV_W  =140,
 D1_IRQ_DSP_TZMA	      =141,
 D1_IRQ_DMAC_IRQ_DSP_NS	  =142,
 D1_IRQ_RISCV_MBOX_RISCV  =144,
 D1_IRQ_RISCV_MBOX_DSP	=145,
 D1_IRQ_RISCV_WDG		=147,
 D1_IRQ_IRRX			=167,
 D1_IRQ_C0_CTI0			=176,
 D1_IRQ_C0_CTI1			=177,
 D1_IRQ_C0_COMMTX0		=180,
 D1_IRQ_C0_COMMTX1		=181,
 D1_IRQ_C0_COMMRX0		=184,
 D1_IRQ_C0_COMMRX1		=185,
 D1_IRQ_C0_PMU0			=188,
 D1_IRQ_C0_PMU1			=189,
 D1_IRQ_C0_AXI_ERROR	=192,
 D1_IRQ_AXI_WR_IRQ		=194,
 D1_IRQ_AXI_RD_IRQ		=195,
 D1_IRQ_DBGWRUPREQ_OUT0	=196,
 D1_IRQ_DBGWRUPREQ_OUT1	=197

}IRQn_Type;
#ifdef __cplusplus
}
#endif



/* 中断服务函数形式 */ 
typedef void (*system_irq_handler_t) (unsigned int giccIar, void *param);


/* 中断服务函数结构体*/
typedef struct _sys_irq_handle
{
    system_irq_handler_t irqHandler; /* 中断服务函数 */
    void *userParam;                 /* 中断服务函数参数 */
} sys_irq_handle_t;



/* 函数声明 */
void int_init(void);
void system_irqtable_init(void);
void system_register_irqhandler(IRQn_Type irq, system_irq_handler_t handler, void *userParam);
void system_irqhandler(void);
void default_irqhandler(unsigned int giccIar, void *userParam);
void PLIC_Init(void);
void PLIC_SetPriority(IRQn_Type IRQn, uint8_t priority);
void PLIC_MIE_DisableIRQ(IRQn_Type IRQn);
void PLIC_MIE_EnableIRQ(IRQn_Type IRQn);
void PLIC_SetPendingIRQ(IRQn_Type IRQn);
void Sys_ResetExecute(void);

#endif