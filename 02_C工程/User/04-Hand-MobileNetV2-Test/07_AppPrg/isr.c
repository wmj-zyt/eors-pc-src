//=====================================================================
// 文件名称：isr.c（中断处理程序源文件）
// 框架提供：苏大嵌入式（sumcu.suda.edu.cn）
// 更新记录：20240817-20250301
// 功能描述：提供中断处理程序编程框架
// 移植规则：【固定】本工程07_AppPrg整个文件夹具备芯片无关性，差异体现在
//           05_UserBoard文件夹的User.h中
//=====================================================================
#include "includes.h"

//本文件使用的内部函数声明
void SecAdd1(uint8_t *p);

//======================================================================
//ISR名称：UART_User_Handler
//触发条件：UART_User串口收到一个字节触发
//程序功能：收到的一个字节后，根据全局变量g_img_pro_flag是否为0（表示可以
//         接收新的数据），将收到的一个字节放入全局数组g_dataReceived，
//         下标为：全局变量g_byteNumber，然后g_byteNumber+1
//特别说明：进入本程序后，可使用uart_get_re_int函数可再进行中断标志判断
//          （1-有UART接收中断，0-没有UART接收中断）
//修改日期：250916，WYH
//======================================================================``
void UART_User_Handler(void)
{
    //【1】关中断
    DISABLE_INTERRUPTS;
    //【2】声明临时变量
    uint8_t flag,ch;
    //【3】判断是否为本中断触发
    if (!uart_get_re_int(UART_User)) goto UART_User_Handler_exit;
    //【4】确认是本中断触发，读取接到的字节赋给变量ch，flag是收到数据标志
    ch=uart_re1(UART_User,&flag);   //调用接收一个字节的函数，清接收中断位
    //【5】根据flag判断是否真正收到一个字节的数据
    if (!flag)  goto UART_User_Handler_exit;  //无数据，退出
    //【6】已经收到一个字节，根据g_img_pro_flag标志，决定是否将该字节放入接收缓冲区
    if (g_img_pro_flag == 1) goto UART_User_Handler_exit;   //不用放入接收缓冲区,退出
	g_dataReceived[g_byteNumber] = ch;                      // 放入接收缓冲区  
	g_byteNumber++;                                         // 接收字节数+1
    //【7】开中断
UART_User_Handler_exit:
    ENABLE_INTERRUPTS;
}

//=====================================================================
//中断服务例程名称：TIMER_User_Handler（TPM1定时器中断处理程序）
//触发条件：20ms时间到
//功能概要：
//          （1）每20ms中断触发本程序一次；
//          （2）达到一秒时，调用秒+1程序，计算“时、分、秒”，
//               放入全局字节型数组g_Time，顺序是时分秒
//          （3）对接收的字节数进行判断，在不为0的条件下，若没有变化，
//               说明接收一帧完成，发送接收事件发送“接收事件”RECEIVE_EVENT，
//               触发接收线程运行
//特别说明：
//          （1）使用全局变量字节型数组gTime[3]，分别存储“时、分、秒”
//          （2）注意其中静态变量的使用
//=====================================================================
void TIMER_User_Handler(void)
{
	//【1】关中断
    DISABLE_INTERRUPTS;
    //【2】声明一个静态变量（20ms计数器）
	static uint8_t TimerCount = 0;       //静态变量（20ms计数器）需要初值
	static uint32_t oldbyteNumber = 0;   //已经接收字节数
	//【3】判断是否为本中断触发
	if(!timer_get_int(TIMER_User)) goto TIMER_User_Handler_exit;
	//【4】确认是本中断触发，TimerCount+1，判断是否调用秒+1程序
	TimerCount++;           //静态变量（20ms计数器）
	if (TimerCount >= 50)
	{
	   TimerCount = 0;     //静态变量（20ms计数器）清0
	   SecAdd1((uint8_t *)g_Time);    //时、分、秒累加
	   gpio_reverse(LIGHT_BLUE);      //蓝灯作为运行指示灯
	}
	//【5】因为20ms进入本中断一次，如果间隔了20ms，收到新的字节，
	//    即g_byteNumber不等于进入本中断时数值，说明一帧接收没有完成，
	//    反之，说明接收一帧完成（两帧之间时间大于20ms）
	//若为0，说明接收还没有开始，不做处理
	if  (g_byteNumber == 0) goto TIMER_User_Handler_exit;
	//g_byteNumber不为0
	if (g_byteNumber != oldbyteNumber)     //新旧不等，说明接收的字节数增加
       oldbyteNumber = g_byteNumber;       //更新oldbyteNumber
    else                                   //新旧相等，
    {
			oldbyteNumber = 0;         //清oldbyteNumber
			g_byteNumber = 0;          //清“接收数据帧字节数”变量g_byteNumber
			g_img_pro_flag = 1;        //“图像处理标志”=1，表示正在处理图像，暂不接收数据
			event_send(g_EventWord,RECEIVE_EVENT);	//发送“接收事件”RECEIVE_EVENT	
    }
	//【5】清时钟溢出标志位，开总中断
TIMER_User_Handler_exit:
    timer_clear_int(TIMER_User);    //清时钟溢出标志位
	ENABLE_INTERRUPTS;                //开总中断
}


//本文件使用的内部函数

//===========================================================================
//函数名称：SecAdd1
//函数返回：无
//参数说明：*p:为指向一个时分秒数组p[3]，p[2],秒；p[1],分，p[0],时
//功能概要：秒单元+1，并处理时分单元（00:00:00-23:59:59)
//===========================================================================
void SecAdd1(uint8_t *p)
{
	//【1】秒+1
	*(p+2)+=1;   
	//【2】未到60秒，退出；到则清秒，分+1
	if(*(p+2)<60) goto SecAdd1_exit;    //使用goto向后跳，减少{}嵌套
	*(p+2)=0;                           //到60秒，清秒，分+1
	*(p+1)+=1;     
	//【3】未到60分，退出；到则清分，时+1
	if(*(p+1)<60) goto SecAdd1_exit;   
	*(p+1)=0;                          //到60分，清分，时+1
	*p+=1;     
	//【4】未到24时，退出；到则清时
	if(*p<24)  goto SecAdd1_exit;   
	*p=0;    //清时
SecAdd1_exit:
    __asm("nop");
}



/*
 【可复用性说明】
 本文件中的中断处理函数调用的均是相关设备封装好的具体构件，在更换芯片
 时，只需保证设备的构件接口一致，即可保证本文件的相关中断处理函数不做任何
 更改，从而达到芯片无关性的要求。
 */
