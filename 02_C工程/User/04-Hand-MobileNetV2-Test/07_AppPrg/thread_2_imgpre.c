#include "includes.h"


extern uint16_t crc16(uint8_t *data, uint32_t length);
void sendFrame(uint32_t length, uint8_t *data);


//======================================================================
//线程函数：thread_imgpre
//功能概要：图像预处理
//内部调用：
//======================================================================
void thread_imgpre(void)
{
    //【1】======启动部分（开头）==========================================
    uint32_t tEventState;     //事件返回参数使用
	//【1】======启动部分（结尾）==========================================
	
    //【2】======线程主循环（开始）========================================
    while (1)
    {
       //（2.1）进入“图像预处理事件”等待状态
       event_recv(g_EventWord,PRETREAT_EVENT,\
                   EVENT_FLAG_OR|EVENT_FLAG_CLEAR,WAITING_FOREVER,&tEventState);
        
    //    delay_ms(1000*15);
       //（2.2）“图像预处理事件”触发后，运行下述语句   
       printf("图像预处理线程【thread_imgpre】：调整对比度...\0");
    //    imgpre_contrast(CAMIMG_H,CAMIMG_W,g_image1,g_image2,1.0);   //调整对比度
    //    LCD_DrawPixel(36,48,CAMIMG_W,CAMIMG_H,g_image2);            //LCD显示图像
       //（2.3）转换成三维数组并正则化
   	   printf("转换成三维数组并正则化...\0");
       sendFrame(CAMIMG_H*CAMIMG_W*3,g_image3);

	//    imgpre_To3DArray(CAMIMG_H,CAMIMG_W,NUM_CHANNEL,g_image1, g_modelInputImage);
        img888pre_To3DArray(CAMIMG_H,CAMIMG_W,NUM_CHANNEL,g_image3, g_modelInputImage);
       //（2.4）触发“推理事件”
       printf("触发“推理事件”\r\n");
       event_send(g_EventWord,REASONING_EVENT);
       __asm("nop");
    }
    //【2】======线程主循环（结尾）========================================
}


//=====================================================================
//函数名称：sendFrame
//函数返回： 无
//参数说明： length：待发送数据的长度；data：待发送数据缓冲区。
//功能概要：通过emuart发送指定长度的字节数组。
//更新记录：20180602，wb；
//=====================================================================
void  sendFrame(uint32_t length, uint8_t *data) {
    uint16_t crc = crc16(data, length);  // CRC计算不变
    // 1. 发送帧头（2字节）
    uart_send1(UART_User, 0x55);
    uart_send1(UART_User, 0xAA);
    
    // 2. 发送长度（4字节，大端序）
    uart_send1(UART_User, (length >> 24) & 0xFF);  // 最高字节
    uart_send1(UART_User, (length >> 16) & 0xFF);
    uart_send1(UART_User, (length >> 8) & 0xFF);
    uart_send1(UART_User, length & 0xFF);          // 最低字节
    
    // 3. 发送数据
    uart_sendN(UART_User, length, data);
    
    // 4. 发送CRC（2字节）
    uart_send1(UART_User, crc >> 8);
    uart_send1(UART_User, crc & 0xFF);
}
