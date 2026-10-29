#ifndef  GPIO_H       //防止重复定义（_GPIO_H  开头)
#define  GPIO_H

#include "mcu.h"

// 端口号地址偏移量宏定义
#define PTB_NUM    (1<<8)
#define PTC_NUM    (2<<8)
#define PTD_NUM    (3<<8)
#define PTE_NUM    (4<<8)
#define PTF_NUM    (5<<8)
#define PTG_NUM    (6<<8)
// GPIO引脚方向宏定义
#define GPIO_INPUT  (0)      //GPIO输入
#define GPIO_OUTPUT (1)      //GPIO输出
// GPIO引脚拉高低状态宏定义
#define PULL_UP    (1)   //拉高
#define PULL_DOWN  (0)   //拉低
// GPIO引脚中断类型宏定义
#define RISING_EDGE  (1)     //上升沿触发
#define FALLING_EDGE (2)     //下降沿触发
#define DOUBLE_EDGE  (3)     //双边沿触发
#define High_Level   (4)
#define Low_Level    (5)
// GPIO输出速率宏定义
#define LOW_SPEED       (0x00u)  //低速
#define MSDIUM_SPEED    (0x01u)  //中速
#define HIGH_SPEED      (0x02u)  //高速
#define VERY_HIGH_SPEED (0x03u)  //超高速


#define USE_BIOS_GPIO    (0) 
#if (USE_BIOS_GPIO==0)

//=====================================================================
//函数名称：gpio_init
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//         dir：引脚方向（0=输入，1=输出,可用引脚方向宏定义）
//         state：端口引脚初始状态（0=低电平，1=高电平）
//功能概要：初始化指定端口引脚作为GPIO引脚功能，并定义为输入或输出，若是输出，
//         还指定初始状态是低电平或高电平
//=====================================================================
void gpio_init(uint16_t port_pin, uint8_t dir, uint8_t state);
//=====================================================================
//函数名称：gpio_set
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//          state：希望设置的端口引脚状态（0=低电平，1=高电平）
//功能概要：当指定端口引脚被定义为GPIO功能且为输出时，本函数设定引脚状态
//=====================================================================
void gpio_set(uint16_t port_pin, uint8_t state);
//=====================================================================
//函数名称：gpio_get
//函数返回：指定端口引脚的状态（1或0）
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数获取指定引脚状态
//=====================================================================
uint8_t gpio_get(uint16_t port_pin);
//=====================================================================
//函数名称：gpio_reverse
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输出时，本函数反转引脚状态
//=====================================================================
void gpio_reverse(uint16_t port_pin);
//=====================================================================
//函数名称：gpio_pull
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//       pullselect：下拉/上拉（PULL_DOWN=下拉，PULL_UP=上拉）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数设置引脚下拉/上拉
//=====================================================================
void gpio_pull(uint16_t port_pin, uint8_t pullselect);
//=====================================================================
//函数名称：gpio_enable_int
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//          irqtype：引脚中断类型，由宏定义给出，再次列举如下：
//                  RISING_EDGE  9      //上升沿触发
//                  FALLING_EDGE 10     //下降沿触发
//                  LowLevel   11       //低电平触发
//                  HighLevel  12       //高电平触发
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数开启引脚中断，并
//          设置中断触发条件。
//=====================================================================
void gpio_enable_int(uint16_t port_pin,uint8_t irqtype);
//=====================================================================
//函数名称：gpio_get_int
//函数返回：引脚GPIO中断标志（1或0）1表示引脚有GPIO中断，0表示引脚没有GPIO中断。
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时,获取中断标志。
//=====================================================================
uint8_t gpio_get_int(uint16_t port_pin);
//=====================================================================
//函数名称：gpio_disable_int
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数关闭引脚中断
//=====================================================================
void gpio_disable_int(uint16_t port_pin);

//=====================================================================
//函数名称：gpio_clear_int
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时,清除中断标志。
//=====================================================================
void gpio_clear_int(uint16_t port_pin);

#elif (USE_BIOS_GPIO==1)
#define gpio_init1 ((void (*)(uint16_t port_pin, uint8_t dir, uint8_t state))(component_fun[33]))
#define gpio_set1 ((void (*)(uint16_t port_pin, uint8_t state))(component_fun[34]))
#define gpio_get1 ((uint8_t (*)(uint16_t port_pin))(component_fun[35]))
#define gpio_reverse1 ((void (*)(uint16_t port_pin))(component_fun[36]))
#define gpio_pull1 ((void (*)(uint16_t port_pin, uint8_t pullselect))(component_fun[37]))
#define gpio_enable_int1 ((void (*)(uint16_t port_pin,uint8_t irqtype))(component_fun[38]))
#define gpio_get_int1 ((uint8_t (*)(uint16_t port_pin))(component_fun[39]))
#define gpio_clear_int1 ((void (*)(uint16_t port_pin))(component_fun[40]))

#endif


#endif

