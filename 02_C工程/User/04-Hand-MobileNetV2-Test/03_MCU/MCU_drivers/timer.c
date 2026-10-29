#include "timer.h"
//============================================================================
//函数名称：timer_init
//函数返回：无
//参数说明： timer_No:时钟模块号  
//         time_ms:定时器中断的时间间隔，单位为毫秒。
//功能概要：时钟模块初始化
//============================================================================
void timer_init(uint8_t timer_No,uint32_t time_ms)
{
    switch(timer_No)
    {
        case 0:   //timer0
            TMR0_CTRL_REG &=~(0xFF<<0);  //reset
            TMR0_CTRL_REG &=~(0x1<<7);   //Periodic mode
            TMR0_CTRL_REG |=((0x6<<4)|(0x1<<2));    //64 pre-scale,OSC24M
            TMR0_INTV_VALUE_REG=(uint32_t)(375*time_ms);
            TMR0_CTRL_REG |=(0x1<<1);    //Reload
            TMR0_CTRL_REG |=(0x1<<0);    //start
            break;
        case 1:   //timer1
            TMR1_CTRL_REG &=~(0xFF<<0);  //reset
            TMR1_CTRL_REG &=~(0x1<<7);   //Periodic mode
            TMR1_CTRL_REG |=((0x6<<4)|(0x1<<2));    //64 pre-scale,OSC24M
            TMR1_CTRL_REG=(uint32_t)(375*time_ms);
            TMR1_CTRL_REG |=(0x1<<1);    //Reload
            TMR1_CTRL_REG |=(0x1<<0);    //start
            break;
    }
}

//============================================================================
//函数名称：timer_enable_int
//函数返回：无
//参数说明： timer_No:时钟模块号
//功能概要：时钟模块使能，开启时钟模块中断及定时器中断
//============================================================================
void timer_enable_int(uint8_t timer_No)
{
    switch(timer_No)
    {
        case 0:
            TMR_IRQ_EN_REG |=(0x1<<0);
            PLIC_MIE_EnableIRQ(D1_IRQ_TIMER0);
            break;
        case 1:
            TMR_IRQ_EN_REG |=(0x1<<1);
            PLIC_MIE_EnableIRQ(D1_IRQ_TIMER1);
            break;
    }
}

//============================================================================
//函数名称：timer_disable_int
//函数返回：无
//参数说明： timer_No:时钟模块号  
//功能概要：定时器中断除能
//============================================================================
void timer_disable_int(uint8_t timer_No)
{
    switch(timer_No)
    {
        case 0:
            TMR_IRQ_EN_REG &=~(0x1<<0);
            PLIC_MIE_DisableIRQ(D1_IRQ_TIMER0);
            break;
        case 1:
            TMR_IRQ_EN_REG &=~(0x1<<1);
            PLIC_MIE_DisableIRQ(D1_IRQ_TIMER1);
            break;
    }
}

//===================================================================
//函数名称：timer_get_int
//参数说明： timer_No:时钟模块号  
//功能概要：获取timer模块中断标志
//函数返回：中断标志 1=有对应模块中断产生;0=无对应模块中断产生
//===================================================================
uint8_t timer_get_int(uint8_t timer_No)
{
    switch(timer_No)
    {
        case 0:
            if((TMR_IRQ_STA_REG & 0x1)==0x1)
                return 1; 
            break;
        case 1:
            if((TMR_IRQ_STA_REG & 0x2)==0x2)
                return 1; 
            break;
    }
    return 0;
}

//============================================================================
//函数名称：timer_clear_int
//函数返回：无
//参数说明：timer_No:时钟模块号
//功能概要：定时器清除中断标志
//============================================================================
void timer_clear_int(uint8_t timer_No)
{
    switch(timer_No)
    {
        case 0:
            TMR_IRQ_STA_REG |= (0x1<<0);
            break;
        case 1:
            TMR_IRQ_STA_REG |= (0x1<<1);
            break;
    }
}
