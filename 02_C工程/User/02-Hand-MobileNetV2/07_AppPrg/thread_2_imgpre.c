#include "includes.h"

void sendFrame(uint32_t length, uint8_t *data);
uint16_t crc16(uint8_t *data, uint32_t length);

//======================================================================
// 线程函数：thread_imgpre
// 功能概要：图像预处理
// 内部调用：
//======================================================================
void thread_imgpre(void)
{
    // 【1】======启动部分（开头）==========================================
    uint32_t tEventState; // 事件返回参数使用

    g_sendImage_pre = 1; // 标记

    // 【1】======启动部分（结尾）==========================================

    // 【2】======线程主循环（开始）========================================
    while (1)
    {
        // （2.1）进入“图像预处理事件”等待状态
        event_recv(g_EventWord, PRETREAT_EVENT,
                   EVENT_FLAG_OR | EVENT_FLAG_CLEAR, WAITING_FOREVER, &tEventState);
        // （2.2）“图像预处理事件”触发后，运行下述语句
        if (g_img_pro_flag == 0)
            goto thread_imgpre_1; // 若图像标志=0
                                  // （2.3）g_img_pro_flag=1，可以进行工作，发送图像到PC机，用户可以手动验证
        if (g_sendImage_pre == 1)
        {
            g_sendImage_pre = 0;
            memcpy(g_image2, g_image1, CAMIMG_H * CAMIMG_W * 2);
            for (int row = 0; row < IMG_H; row++)
            {
                for (int col = 0; col < IMG_W; col++)
                {
                    uint16_t pixel = g_image2[row][col];

                    // 提取RGB565分量
                    uint8_t r5 = (pixel >> 11) & 0x1F; // 5位红色
                    uint8_t g6 = (pixel >> 5) & 0x3F;  // 6位绿色
                    uint8_t b5 = pixel & 0x1F;         // 5位蓝色

                    // 转换为8位RGB（精确计算）
                    uint8_t r8 = r5 * 255 / 31;
                    uint8_t g8 = g6 * 255 / 63;
                    uint8_t b8 = b5 * 255 / 31;

                    g_image3[0][row][col] = r8;
                    g_image3[1][row][col] = g8;
                    g_image3[2][row][col] = b8;
                }
            }

            sendFrame(CAMIMG_H * CAMIMG_W * 3, (uint8_t *)g_image3);
            // （2.4）g_img_pro_flag=1，可以进行工作，调整对比度，LCD显示图像
            printf("图像预处理线程【thread_imgpre】：调整对比度...\0");
            //            imgpre_contrast(CAMIMG_H, CAMIMG_W, g_image1, g_image2, 1, 20);
            //            LCD_DrawPixel(36, 48, CAMIMG_W, CAMIMG_H, g_image2);
            // （2.5）转换成三维数组并正则化
            printf("转换成三维数组并正则化...\0");
            img888pre_To3DArray(CAMIMG_H, CAMIMG_W, NUM_CHANNEL, g_image3, g_modelInputImage);
            // （2.6）触发“推理事件”
            printf("触发“推理事件”\r\n");
            event_send(g_EventWord, REASONING_EVENT);
        }

    thread_imgpre_1:
        __asm("nop");
    }
    // 【2】======线程主循环（结尾）========================================
}

//=====================================================================
// 函数名称：crc16
// 功能概要：将数据进行16位的CRC校验，返回校验后的结果值
// 参数说明：ptr:需要校验的数据缓存区，len:需要检验的数据长度
// 函数返回：计算得到的校验值
//=====================================================================
uint16_t crc16(uint8_t *data, uint32_t length)
{
    // 【1】声明临时变量
    uint32_t i, j;
    uint16_t crc;
    uint8_t lsb;
    // 【2】初始化临时变量
    crc = 0xFFFF;
    // 【3】计算CRC校验值
    for (i = 0; i < length; i++)
    {
        // 将数据与CRC值进行异或运算
        crc ^= (uint16_t)data[i];
        for (j = 0; j < 8; j++)
        { // 将CRC值右移一位，若最低位为1，则与多项式A001进行异或运算
            lsb = crc & 0x0001;
            crc >>= 1;
            if (lsb)
                crc ^= 0xA001;
        }
    }
    return crc;
}

//=====================================================================
// 函数名称：sendFrame
// 函数返回： 无
// 参数说明： length：待发送数据的长度；data：待发送数据缓冲区。
// 功能概要：通过emuart发送指定长度的字节数组。
// 更新记录：20180602，wb；
//=====================================================================
void sendFrame(uint32_t length, uint8_t *data)
{
    uint16_t crc = crc16(data, length); // CRC计算不变
    // 1. 发送帧头（2字节）
    uart_send1(UART_User, 0x55);
    uart_send1(UART_User, 0xAA);

    // 2. 发送长度（4字节，大端序）
    uart_send1(UART_User, (length >> 24) & 0xFF); // 最高字节
    uart_send1(UART_User, (length >> 16) & 0xFF);
    uart_send1(UART_User, (length >> 8) & 0xFF);
    uart_send1(UART_User, length & 0xFF); // 最低字节

    // 3. 发送数据
    uart_sendN(UART_User, length, data);

    // 4. 发送CRC（2字节）
    uart_send1(UART_User, crc >> 8);
    uart_send1(UART_User, crc & 0xFF);
}
