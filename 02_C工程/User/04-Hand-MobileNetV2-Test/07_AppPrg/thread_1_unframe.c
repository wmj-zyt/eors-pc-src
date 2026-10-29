#include "includes.h"

//内部函数声明
uint16_t crc16(uint8_t *ptr, uint32_t len);

//======================================================================
// 线程函数：thread_unframe
// 功能概要：解帧获得一幅图像，放入全局数组g_image1
// 帧结构： 55AA 72000字节图片数据  两个字节CCR校验和
// 内部调用：crc16
//======================================================================
void thread_unframe(void)
{
    //【1】======启动部分（开始）======
    //（1.1）声明临时变量
    uint32_t tEventState;           //事件返回参数使用
    int i,j,k;                   
    uint16_t r,g,b,rgb565;          //图像颜色值变量

    //（1.2）初始化临时变量
    tEventState = 0;              
    i = 0;             
    j = 0;
    r = 0;             
    g = 0;
    b = 0;
    rgb565 = 0;
    //【1】======启动部分（结尾）========

    //【2】======线程主循环（开始）======
    while (1)
    {
        // （2.1）进入“接收事件”RECEIVE_EVENT的等待状态
        printf("金葫芦提示：解帧线程【thread_unframe】进入等待“接收事件”RECEIVE_EVENT状态...\r\n");
        LCD_ShowString(20, 218, BLUE, GRAY, (const char *)"Waiting image from PC ...");
        event_recv(g_EventWord, RECEIVE_EVENT,
                   EVENT_FLAG_OR | EVENT_FLAG_CLEAR, WAITING_FOREVER, &tEventState);
        //（2.2）至此，接收到一帧完整图像数据，进行解帧
        printf("             接收到一帧完整图像数据，进行解帧...\r\n");
        LCD_DrawSurface(20,218,230,310,GRAY);    //清除将要使用的LCD区域
        LCD_ShowString(20, 235, YELLOW, GRAY, (const char *)"Received one dataframe...");
        //判断是不是握手帧
        if ((g_dataReceived[0] == 0x24) && (g_dataReceived[1] == 0x21)){
            uart_send_string(UART_User,"yes,I am uart Test");
            g_img_pro_flag = 0;   //允许重新接收
            printf("             连接EORS成功\r\n");
            goto thread_unframe_exit2;
            
        }
        //      ① 解析帧头，帧头不是0xAA55 报错,由于上位机是小端格式发送，因此此处先判断低字节
        if ((g_dataReceived[0] != 0x55) || (g_dataReceived[1] != 0xAA)) goto thread_unframe_exit1;
        
        //      ② 以小端模式读取校验和（十六位）
        k=sizeof(g_dataReceived);         //字节数
        i = g_dataReceived[k-2] | (g_dataReceived[k-1] << 8);
        //      ③ 根据接收到的数据计算校验和
        j = crc16(g_dataReceived, k - 2);
        //      ④ 判断校验和是否正确，不正确退出此次循环
        if (i != j) goto thread_unframe_exit1;
        // （2.3）至此，校验和校验正确，说明数据接收无误数据，根据接收到的数据组合图像，放入g_image1数组
        //  接收数据格式为 帧头0xAA55 72000字节图片数据 两个字节CCR校验和,因此从下标2处开始接收数据,
        //  发送数据时，按照从上到下，从左到右的顺序发送数据，每个像素点被拆分成RGB （红绿蓝）三个字节
        //  从下标2开始，每三个字节为一组，分别表示RGB三个分量，因此需要将三个分量组合成RGB565格式
        for (int row = 0; row < IMG_H; row++)
        {
            for (int col = 0; col < IMG_W; col++)
            {
                // 从下标2开始解析RGB数据,每次一个像素点
                r = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col];
                g = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col + 1];
                b = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col + 2];

                g_image3[0][row][col]  = r;
                g_image3[1][row][col]  = g;
                g_image3[2][row][col]  = b;

                
                // 扩展数据到16位，以便组装为RGB565格式
                r = (r & 0xF8) << 8;
                g = (g & 0xFC) << 3;
                b = (b & 0xF8) >> 3;
                // 组合RGB565格式
                rgb565 = r | g | b;
                // 将RGB565格式的图像数据存入g_image1[row][col]
                g_image1[row][col] = rgb565;

            }
        }
        //（2.4）至此，解帧完成，g_image1数组为接收的图像数据，进行下一步工作
        printf("             嵌入式终端LCD上显示图像，终端将进行图像预处理...\r\n");
        LCD_DrawPixel(36,48,CAMIMG_W,CAMIMG_H,g_image1);  //LCD显示图像
        //（2.5）触发“图像预处理事件”   
        event_send(g_EventWord,PRETREAT_EVENT);
        goto thread_unframe_exit2;    //为了保证单出口
thread_unframe_exit1:
       printf("     解帧有误，重新接收...\n\r");
       LCD_DrawSurface(20,223,230,310,GRAY);    //清除将要使用的LCD区域
       g_img_pro_flag = 0;            //允许重新接收 
thread_unframe_exit2:       
       __asm("nop");
    }
}

//=====================================================================
// 函数名称：crc16
// 功能概要：将数据进行16位的CRC校验，返回校验后的结果值
// 参数说明：ptr:需要校验的数据缓存区，len:需要检验的数据长度
// 函数返回：计算得到的校验值
//=====================================================================
uint16_t crc16(uint8_t *data, uint32_t length)
{
    //【1】声明临时变量
    uint32_t i,j;
    uint16_t crc;
    uint8_t lsb;
    //【2】初始化临时变量
    crc = 0xFFFF;
    //【3】计算CRC校验值
    for (i = 0; i < length; i++)
    {
        // 将数据与CRC值进行异或运算
        crc ^= (uint16_t)data[i];
        for (j = 0; j < 8; j++)
        {                      // 将CRC值右移一位，若最低位为1，则与多项式A001进行异或运算
            lsb = crc & 0x0001;
            crc >>= 1;
            if (lsb)  crc ^= 0xA001;
        }
    }
    return crc;
}


