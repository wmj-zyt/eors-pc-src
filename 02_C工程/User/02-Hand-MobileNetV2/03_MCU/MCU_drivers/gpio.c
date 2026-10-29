
#include "gpio.h"

//内部函数声明
void gpio_get_port_pin(uint16_t port_pin,uint8_t* port,uint8_t* pin);

//=====================================================================
//函数名称：gpio_init
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//         dir：引脚方向（0=输入，1=输出,可用引脚方向宏定义）
//         state：端口引脚初始状态（0=低电平，1=高电平）
//功能概要：初始化指定端口引脚作为GPIO引脚功能，并定义为输入或输出，若是输出，
//         还指定初始状态是低电平或高电平
//=====================================================================
void gpio_init(uint16_t port_pin, uint8_t dir, uint8_t state)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
    case 1: //portB
         if(dir == 1)  //定义为输出引脚
         {
            if(pin<=7)
            {
            	PB_CFG0 &= ~(0xF << (pin * 4));
            	PB_CFG0 |= (0x1 << (pin * 4));
            }
            else
            {
            	PB_CFG1 &= ~(0xF << ((pin-8) * 4));
            	PB_CFG1 |= (0x1 << ((pin-8) * 4));
            }
            gpio_set(port_pin,state);
         }
         else
         {
            if(pin<=7)
                PB_CFG0 &= ~(0xF<<(pin * 4));
            else
                PB_CFG1 &= ~(0xF<<((pin-8) * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    case 2:  //portC
         if(dir == 1)  //定义为输出引脚
         {
         	PC_CFG0 &= ~(0xF << (pin * 4));
            PC_CFG0 |= (0x1 << (pin * 4));
            gpio_set(port_pin,state);
         }
         else
         {
            PC_CFG0 &= ~(0xF<<(pin * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    case 3:  //portD
         if(dir == 1)  //定义为输出引脚
         {
            if(pin<=7)
            {
            	PD_CFG0 &= ~(0xF << (pin * 4));
            	PD_CFG0 |= (0x1 << (pin * 4));
            }
            else if(pin>=8 && pin<=15)
            {
            	PD_CFG1 &= ~(0xF << ((pin-8) * 4));
            	PD_CFG1 |= (0x1 << ((pin-8) * 4));
            }
            else
            {
            	PD_CFG2 &= ~(0xF << ((pin-16) * 4));
            	PD_CFG2 |= (0x1 << ((pin-16) * 4));
            }
            gpio_set(port_pin,state);
         }
         else
         {
            if(pin<=7)
                PD_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PD_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PD_CFG2 &= ~(0xF<<((pin-16) * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    case 4:  //portE
         if(dir == 1)  //定义为输出引脚
         {
            if(pin<=7)
            {
            	PE_CFG0 &= ~(0xF << (pin * 4));
            	PE_CFG0 |= (0x1 << (pin * 4));
            }
            else if(pin>=8 && pin<=15)
            {
            	PE_CFG1 &= ~(0xF << ((pin-8) * 4));
            	PE_CFG1 |= (0x1 << ((pin-8) * 4));
            }
            else
            {
            	PE_CFG2 &= ~(0xF << ((pin-16) * 4));
            	PE_CFG2 |= (0x1 << ((pin-16) * 4));
            }
            gpio_set(port_pin,state);
         }
         else
         {
            if(pin<=7)
                PE_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PE_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PE_CFG2 &= ~(0xF<<((pin-16) * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    case 5:  //portF
         if(dir == 1)  //定义为输出引脚
         {
         	PF_CFG0 &= ~(0xF << (pin * 4));
            PF_CFG0 |= (0x1 << (pin * 4));
            gpio_set(port_pin,state);
         }
         else
         {
            PF_CFG0 &= ~(0xF<<(pin * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    case 6:  //portG
         if(dir == 1)  //定义为输出引脚
         {
            if(pin<=7)
            {
            	PG_CFG0 &= ~(0xF << (pin * 4));
            	PG_CFG0 |= (0x1 << (pin * 4));
            }
            else if(pin>=8 && pin<=15)
            {
            	PG_CFG1 &= ~(0xF << ((pin-8) * 4));
            	PG_CFG1 |= (0x1 << ((pin-8) * 4));
            }
            else
            {
            	PG_CFG2 &= ~(0xF << ((pin-16) * 4));
            	PG_CFG2 |= (0x1 << ((pin-16) * 4));
            }
            gpio_set(port_pin,state);
         }
         else
         {
            if(pin<=7)
                PG_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PG_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PG_CFG2 &= ~(0xF<<((pin-16) * 4));
            //gpio_pull(port_pin,1);
         }
         break;
    }
}

//=====================================================================
//函数名称：gpio_set
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//          state：希望设置的端口引脚状态（0=低电平，1=高电平）
//功能概要：当指定端口引脚被定义为GPIO功能且为输出时，本函数设定引脚状态
//=====================================================================
void gpio_set(uint16_t port_pin, uint8_t state)
{
   uint8_t port,pin;    //声明端口port、引脚pin变量
   //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
   gpio_get_port_pin(port_pin,&port,&pin);
   switch (port)
   {
    case 1:
        if(state==1)
            PB_DAT |= (1<<pin);
        else
            PB_DAT &=~(1<<pin);
        break;
    case 2:
        if(state==1)
            PC_DAT |= (1<<pin);
        else
            PC_DAT &=~(1<<pin);
        break;
    case 3:
        if(state==1)
        {
        	//PD_DAT &= ~(0x1<<pin);
            PD_DAT |= (0x1<<pin);
        }
        else
        { 
            PD_DAT &=~(0x1<<pin);
        }
        break;
    case 4:
        if(state==1)
            PE_DAT |= (1<<pin);
        else
            PE_DAT &=~(1<<pin);
        break;
    case 5:
        if(state==1)
            PF_DAT |= (1<<pin);
        else
            PF_DAT &=~(1<<pin);
        break;
    case 6:
        if(state==1)
            PG_DAT |= (1<<pin);
        else
            PG_DAT &=~(1<<pin);
        break;
   }

}
//=====================================================================
//函数名称：gpio_get
//函数返回：指定端口引脚的状态（1或0）
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数获取指定引脚状态
//=====================================================================
uint8_t gpio_get(uint16_t port_pin)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    uint32_t temp;      //临时存放寄存器里的值
    uint8_t value=0;
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
    case 1:
        temp=PB_DAT;
        if((temp & (1<<pin))>>pin==1)
            value=1;
        else
            value=0;
        break; 
    case 2:
        temp=PC_DAT;
        if((temp & (1<<pin))>>pin==1)
            value=1;
        else
            value=0;
        break; 
    case 3:
        temp=PD_DAT;
        if(((temp & (1 << pin)) >> pin)==1)
            value=1;
        else
            value=0;
        break; 
    case 4:
        temp=PE_DAT;
        if((temp & (1<<pin))>>pin==1)
            value=1;
        else
            value=0;
        break; 
    case 5:
        temp=PF_DAT;
        if((temp & (1<<pin))>>pin==1)
            value=1;
        else
            value=0;
        break; 
    case 6: 
        temp=PG_DAT;
        if((temp & (1<<pin))>>pin==1)
            value=1;
        else
            value=0;
        break; 
    }
    return value;
}

//=====================================================================
//函数名称：gpio_reverse
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输出时，本函数反转引脚状态
//=====================================================================
void gpio_reverse(uint16_t port_pin)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    uint32_t temp;       //临时存放寄存器里的值
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
        case 1:
            temp=PB_DAT;
            if((temp & (1<<pin))>>pin==1)
                PB_DAT &=~(1<<pin);
            else
                PB_DAT |=(1<<pin);
            break;
        case 2:
            temp=PC_DAT;
            if((temp & (1<<pin))>>pin==1)
                PC_DAT &=~(1<<pin);
            else
                PC_DAT |=(1<<pin);
            break;
        case 3:
            temp=PD_DAT;
            if((temp & (1<<pin))>>pin==1)
                PD_DAT &=~(1<<pin);
            else
                PD_DAT |=(1<<pin);
            break;
        case 4:
            temp=PE_DAT;
            if((temp & (1<<pin))>>pin==1)
                PE_DAT &=~(1<<pin);
            else
                PE_DAT |=(1<<pin);
            break;
        case 5:
            temp=PF_DAT;
            if((temp & (1<<pin))>>pin==1)
                PF_DAT &=~(1<<pin);
            else
                PF_DAT |=(1<<pin);
            break;
        case 6:
            temp=PG_DAT;
            if((temp & (1<<pin))>>pin==1)
                PG_DAT &=~(1<<pin);
            else
                PG_DAT |=(1<<pin);
            break;
    }
}

//=====================================================================
//函数名称：gpio_pull
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//       pullselect：下拉/上拉（PULL_DOWN=下拉，PULL_UP=上拉）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数设置引脚下拉/上拉
//=====================================================================
void gpio_pull(uint16_t port_pin, uint8_t pullselect)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);

    switch(port)
    {
        case 1:
            if(pullselect==1)
                PB_PULL0 |=(1<<(2*pin));
            else
                PB_PULL0 |=(2<<(2*pin));
            break;
        case 2:
            if(pullselect==1)
                PC_PULL0 |=(1<<(2*pin));
            else
                PC_PULL0 |=(2<<(2*pin));
            break;
        case 3:
            if(pullselect==1)
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PD_PULL1 |=(1<<(2*pin));
                }
                else
                    PD_PULL0 |=(1<<(2*pin));
            }
            else
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PD_PULL1 |=(2<<(2*pin));
                }
                else
                    PD_PULL0 |=(2<<(2*pin));
            }
            break;
        case 4:
            if(pullselect==1)
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PE_PULL1 |=(1<<(2*pin));
                }
                else
                    PE_PULL0 |=(1<<(2*pin));
            }
            else
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PE_PULL1 |=(2<<(2*pin));
                }
                else
                    PE_PULL0 |=(2<<(2*pin));
            }
            break;
        case 5:
            if(pullselect==1)
                PF_PULL0 |=(1<<(2*pin));
            else
                PF_PULL0 |=(2<<(2*pin));
            break;
        case 6:
            if(pullselect==1)
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PG_PULL1 |=(1<<(2*pin));
                }
                else
                    PG_PULL0 |=(1<<(2*pin));
            }
            else
            {
                if(pin>=16)
                {
                    pin=pin-16;
                    PG_PULL1 |=(2<<(2*pin));
                }
                else
                    PG_PULL0 |=(2<<(2*pin));
            }
            break;
    }
}

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
void gpio_enable_int(uint16_t port_pin,uint8_t irqtype)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
        case 1:
        if(pin<=7)
        {	
        	PB_CFG0 &= ~(0xF<<(pin * 4));
            PB_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        }
        else
        {
        	PB_CFG1 &= ~(0xF<<((pin-8) * 4));
            PB_CFG1 |= (0xE<<((pin-8) * 4));  //复用成ENIT功能
        }
        switch(irqtype)
        {
            case 1:  //上升沿触发
            if(pin<=7)
                PB_EINT_CFG0 &= ~(0xF<<(pin * 4));
            else
                PB_EINT_CFG1 &= ~(0xF<<((pin-8) * 4));
            break;
            case 2:  //下降沿触发
            if(pin<=7)
                PB_EINT_CFG0 |= (0x1<<(pin * 4));
            else
                PB_EINT_CFG1 |= (0x1<<((pin-8) * 4));
            break;
            case 3:  //双边沿触发
            if(pin<=7)
                PB_EINT_CFG0 |= (0x4<<(pin * 4));
            else
                PB_EINT_CFG1 |= (0x4<<((pin-8) * 4));
            break;
            case 4:
            if(pin<=7)
                PB_EINT_CFG0 |= (0x2<<(pin * 4));
            else
                PB_EINT_CFG1 |= (0x2<<((pin-8) * 4));
            break;
            case 5:
            if(pin<=7)
                PB_EINT_CFG0 |= (0x3<<(pin * 4));
            else
                PB_EINT_CFG1 |= (0x3<<((pin-8) * 4));
            break;
        }
        PB_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOB_NS);
        break;
        case 2:
        PC_CFG0 &= ~(0xF<<(pin * 4));
        PC_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        switch(irqtype)
        {
            case 1:  //上升沿触发
            PC_EINT_CFG0  &= ~(0xF<<(pin * 4));
            break;
            case 2:  //下降沿触发
            PC_EINT_CFG0 |= (0x1<<(pin * 4));
            break;
            case 3:  //双边沿触发
            PC_EINT_CFG0 |= (0x4<<(pin * 4));
            break;
            case 4:
            PC_EINT_CFG0 |= (0x2<<(pin * 4));
            break;
            case 5:
            PC_EINT_CFG0 |= (0x3<<(pin * 4));
            break;
        }
        PC_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOC_NS);
        break;
        case 3:
        if(pin<=7)
        {	
        	PD_CFG0 &= ~(0xF<<(pin * 4));
            PD_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        }
        else if(pin>=8 && pin<=15)
        {
        	PD_CFG1 &= ~(0xF<<((pin-8) * 4));
            PD_CFG1 |= (0xE<<((pin-8) * 4));  //复用成ENIT功能
        }
        else
        {
        	PD_CFG2 &= ~(0xF<<((pin-16) * 4));
            PD_CFG2 |= (0xE<<((pin-16) * 4));  //复用成ENIT功能
        }
        switch(irqtype)
        {
            case 1:  //上升沿触发
            if(pin<=7)
                PD_EINT_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PD_EINT_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PD_EINT_CFG2 &= ~(0xF<<((pin-16) * 4));
            break;
            case 2:  //下降沿触发
            if(pin<=7)
                PD_EINT_CFG0 |= (0x1<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PD_EINT_CFG1 |= (0x1<<((pin-8) * 4));
            else
                PD_EINT_CFG2 |= (0x1<<((pin-16) * 4));
            break;
            case 3:  //双边沿触发
            if(pin<=7)
                PD_EINT_CFG0 |= (0x4<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PD_EINT_CFG1 |= (0x4<<((pin-8) * 4));
            else   
                PD_EINT_CFG2 |= (0x4<<((pin-16) * 4));
            break;
            case 4:
            if(pin<=7)
                PD_EINT_CFG0 |= (0x2<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PD_EINT_CFG1 |= (0x2<<((pin-8) * 4));
            else
                PD_EINT_CFG2 |= (0x2<<((pin-16) * 4));
            break;
            case 5:
            if(pin<=7)
                PD_EINT_CFG0 |= (0x3<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PD_EINT_CFG1 |= (0x3<<((pin-8) * 4));
            else
                PD_EINT_CFG2 |= (0x3<<((pin-16) * 4));
            break;
        }
        PD_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOD_NS);
        break;
        case 4:
        if(pin<=7)
        {	
        	PE_CFG0 &= ~(0xF<<(pin * 4));
            PE_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        }
        else if(pin>=8&&pin<=15)
        {
        	PE_CFG1 &= ~(0xF<<((pin-8) * 4));
            PE_CFG1 |= (0xE<<((pin-8) * 4));  //复用成ENIT功能
        }
        else
        {
        	PE_CFG2 &= ~(0xF<<((pin-16) * 4));
            PE_CFG2 |= (0xE<<((pin-16) * 4));  //复用成ENIT功能
        }
        switch(irqtype)
        {
            case 1:  //上升沿触发
            if(pin<=7)
                PE_EINT_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PE_EINT_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PE_EINT_CFG2 &= ~(0xF<<((pin-16) * 4));
            break;
            case 2:  //下降沿触发
            if(pin<=7)
                PE_EINT_CFG0 |= (0x1<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PE_EINT_CFG1 |= (0x1<<((pin-8) * 4));
            else
                PE_EINT_CFG2 |= (0x1<<((pin-16) * 4));
            break;
            case 3:  //双边沿触发
            if(pin<=7)
                PE_EINT_CFG0 |= (0x4<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PE_EINT_CFG1 |= (0x4<<((pin-8) * 4));
            else   
                PE_EINT_CFG2 |= (0x4<<((pin-16) * 4));
            break;
            case 4:
            if(pin<=7)
                PE_EINT_CFG0 |= (0x2<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PE_EINT_CFG1 |= (0x2<<((pin-8) * 4));
            else
                PE_EINT_CFG2 |= (0x2<<((pin-16) * 4));
            break;
            case 5:
            if(pin<=7)
                PE_EINT_CFG0 |= (0x3<<(pin * 4));
            else if(pin>=8 && pin<=15)
                PE_EINT_CFG1 |= (0x3<<((pin-8) * 4));
            else
                PE_EINT_CFG2 |= (0x3<<((pin-16) * 4));
            break;
        }
        PE_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOE_NS);
        break;
        PF_CFG0 &= ~(0xF<<(pin * 4));
        PF_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        case 5:
        switch(irqtype)
        {
            case 1:  //上升沿触发
            PF_EINT_CFG0 &= ~(0xF<<(pin * 4));
            break;
            case 2:  //下降沿触发
            PF_EINT_CFG0 |= (0x1<<(pin * 4));
            break;
            case 3:  //双边沿触发
            PF_EINT_CFG0 |= (0x4<<(pin * 4));
            break;
            case 4:
            PF_EINT_CFG0 |= (0x2<<(pin * 4));
            break;
            case 5:
            PF_EINT_CFG0 |= (0x3<<(pin * 4));
            break;
        }
        PF_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOF_NS);
        break;
        case 6:
        if(pin<=7)
        {	
        	PG_CFG0 &= ~(0xF<<(pin * 4));
            PG_CFG0 |= (0xE<<(pin * 4));  //复用成ENIT功能
        }
        else if(pin>=8&&pin<=15)
        {
        	PG_CFG1 &= ~(0xF<<((pin-8) * 4));
            PG_CFG1 |= (0xE<<((pin-8) * 4));  //复用成ENIT功能
        }
        else
        {
        	PG_CFG2 &= ~(0xF<<((pin-16) * 4));
            PG_CFG2 |= (0xE<<((pin-16) * 4));  //复用成ENIT功能
        }
        switch(irqtype)
        {
            case 1:  //上升沿触发
            if(pin<=7)
                PG_EINT_CFG0 &= ~(0xF<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PG_EINT_CFG1 &= ~(0xF<<((pin-8) * 4));
            else
                PG_EINT_CFG2 &= ~(0xF<<((pin-16) * 4));
            break;
            case 2:  //下降沿触发
            if(pin<=7)
                PG_EINT_CFG0 |= (0x1<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PG_EINT_CFG1 |= (0x1<<((pin-8) * 4));
            else
                PG_EINT_CFG2 |= (0x1<<((pin-16) * 4));
            break;
            case 3:  //双边沿触发
            if(pin<=7)
                PG_EINT_CFG0 |= (0x4<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PG_EINT_CFG1 |= (0x4<<((pin-8) * 4));
            else   
                PG_EINT_CFG2 |= (0x4<<((pin-16) * 4));
            break;
            case 4:
            if(pin<=7)
                PG_EINT_CFG0 |= (0x2<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PG_EINT_CFG1 |= (0x2<<((pin-8) * 4));
            else
                PG_EINT_CFG2 |= (0x2<<((pin-16) * 4));
            break;
            case 5:
            if(pin<=7)
                PG_EINT_CFG0 |= (0x3<<(pin * 4));
            else if(pin>=8&&pin<=15)
                PG_EINT_CFG1 |= (0x3<<((pin-8) * 4));
            else
                PG_EINT_CFG2 |= (0x3<<((pin-16) * 4));
            break;
        }
        PG_EINT_CTL |= (0x1 << pin); //中断使能
        PLIC_MIE_EnableIRQ(D1_IRQ_GPIOG_NS);
        break;
    }

}

//=====================================================================
//函数名称：gpio_disable_int
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时，本函数关闭引脚中断
//=====================================================================
void gpio_disable_int(uint16_t port_pin)
{
	uint8_t port,pin;    //声明端口port、引脚pin变量
	//根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
	gpio_get_port_pin(port_pin,&port,&pin);
	switch(port)
	{
		case 1:
			PB_EINT_CTL &= ~(0x1 << pin); //中断除能
        	PLIC_MIE_DisableIRQ(D1_IRQ_GPIOB_NS);
			break;
		case 2:
			PC_EINT_CTL &= ~(0x1 << pin); //中断除能
        	PLIC_MIE_DisableIRQ(D1_IRQ_GPIOC_NS);
			break;
		case 3:
			PD_EINT_CTL &= ~(0x1 << pin); //中断除能
        	PLIC_MIE_DisableIRQ(D1_IRQ_GPIOD_NS);
			break;
		case 4:
			PE_EINT_CTL &= ~(0x1 << pin); //中断除能
        	//PLIC_MIE_DisableIRQ(D1_IRQ_GPIOE_NS);
			break;
		case 5:
			PF_EINT_CTL &= ~(0x1 << pin); //中断除能
        	PLIC_MIE_DisableIRQ(D1_IRQ_GPIOF_NS);
			break;
		case 6:
			PG_EINT_CTL &= ~(0x1 << pin); //中断除能
        	PLIC_MIE_DisableIRQ(D1_IRQ_GPIOG_NS);
			break;
	}
}


//=====================================================================
//函数名称：gpio_get_int
//函数返回：引脚GPIO中断标志（1或0）1表示引脚有GPIO中断，0表示引脚没有GPIO中断。
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时,获取中断标志。
//=====================================================================
uint8_t gpio_get_int(uint16_t port_pin)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    uint8_t value=0;
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
        case 1:
            if((PB_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
        case 2:
            if((PC_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
        case 3:
            if((PD_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
        case 4:
            if((PE_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
        case 5:
            if((PF_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
        case 6:
            if((PG_EINT_STATUS &(0x1<<pin))==(0x1<<pin))
                value=1;
            else value=0;
            break;
    }
    return value;
}

//=====================================================================
//函数名称：gpio_clear_int
//函数返回：无
//参数说明：port_pin：(端口号)|(引脚号)（如：(PTB_NUM)|(9) 表示为B口9号脚）
//功能概要：当指定端口引脚被定义为GPIO功能且为输入时,清除中断标志。
//=====================================================================
void gpio_clear_int(uint16_t port_pin)
{
    uint8_t port,pin;    //声明端口port、引脚pin变量
    //根据带入参数port_pin，解析出端口与引脚分别赋给port,pin
    gpio_get_port_pin(port_pin,&port,&pin);
    switch(port)
    {
        case 1:
            PB_EINT_STATUS |= (0x1<<pin);
            break;
        case 2:
            PC_EINT_STATUS |= (0x1<<pin);
            break;
        case 3:
            PD_EINT_STATUS |= (0x1<<pin);
            break;
        case 4:
            PE_EINT_STATUS |= (0x1<<pin);
            break;
        case 5:
            PF_EINT_STATUS |= (0x1<<pin);
            break;
        case 6:
            PG_EINT_STATUS |= (0x1<<pin);
            break;
    }
}


//----------------------以下为内部函数存放处-----------------
//=====================================================================
//函数名称：gpio_get_port_pin
//函数返回：无
//参数说明：port_pin：端口号|引脚号（如：(PTB_NUM)|(9) 表示为B口9号脚）
//       port：端口号（传指带出参数）
//       pin:引脚号（0~15，实际取值由芯片的物理引脚决定）（传指带出参数）
//功能概要：将传进参数port_pin进行解析，得出具体端口号与引脚号，分别赋值给port与pin,返回。
//       （例：(PTB_NUM)|(9)解析为PORTB与9，并将其分别赋值给port与pin）。
//=====================================================================
void gpio_get_port_pin(uint16_t port_pin,uint8_t* port,uint8_t* pin)
{
    *port = (port_pin>>8);
    *pin = port_pin;
}