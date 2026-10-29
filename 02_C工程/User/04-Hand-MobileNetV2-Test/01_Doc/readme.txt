
UART_User串口中断
TIMER_User_Handler中断
thread_unframe
预处理
推理
二次编程





从推理模版到验证程序

1. 删除摄像头相关操作
推理模版程序运行流程为：初始化->摄像头采集图像->图像采集完毕发送采集完毕事件->解析图像并显示在LCD屏幕上->进行图像预处理（调整对比度、归一化）->图片推理得出结果->二次编程。
因为此处要进行的任务是验证部署模型的准确性，主要通过获取的上位机发送的原始图片进行图片预测，所以不需要摄像头操作，以下为删除操作的详细步骤：
步骤1：导入电子资源。通过金葫芦IDE打开电子资源中的【EORS-D1-H-LiteOS-Template】文件夹，可以看到07文件夹下存在头文件和数个源文件。
步骤2：打开thread_auto.c文件，删除摄像头初始化代码。删除摄像头初始化代码及使能摄像头中断代码：
        mflag=cam_init();        //摄像头初始化代码
        cam_enable_int();        //使能摄像头帧中断
步骤3：打开thread_imgget.c文件，删除摄像头初始化代码。删除摄像头初始化代码及使能摄像头中断代码：
        tFlag=cam_init();        //摄像头初始化代码
        cam_enable_int();       //使能摄像头帧中断
至此，已经全部删除摄像头操作相关代码，验证程序不需要摄像头参与，因此删除并不影响验证程序运行。
2. 添加缓冲区及相关变量
验证程序的核心思路是通过串口接收上位机发送的图像数据，图像数据发送的格式为r g b格式，一次发送的数据为一幅图像，因此要添加大小为【帧头+数据+校验和】的缓冲区。
缓冲区变量的大小是【宽*高*通道数+帧头+校验和】个数的字节。具体大小为150*160*3 + 2 + 2 = 72004个字节。在includes.h头文件中添加缓冲区变量以及接收字节数记录变量：
  G_VAR_PREFIX vuint32_t  g_byteNumber;        //接收字节数
G_VAR_PREFIX volatile uint8_t g_dataReceived[IMG_H * IMG_W * NUM_CHANNEL + 2 + 2]; 
3. 修改串口及定时器中断处理函数
串口中断的核心思想为：当串口开始接收一张图片时，接收一定是连续的。因此，程序中用定时器来验证接收是否结束：定时器触发间隔为20ms，使用一个静态变量来记录本次定时器触发时串口接收的字节数，若是下次触发定时器中断时接收数据的长度没有改变，则认为本次图片接收结束。以下为修改中断处理函数的详细操作步骤：
步骤1：删除回发字节的代码。此处串口中断被用于其他的功能，因此无用代码要删除。
    if (flag)                       //有数据
    {
        uart_send1(UART_User,ch);  //回发接收到的字节
    }
步骤2：添加缓冲区接收数据的代码。使用上一步定义的缓冲区接收数据，接收数据后将字节的长度加一，若程序处于图像处理状态则退出。
   if (g_img_pro_flag == 1) goto UART_User_Handler_exit;   //不用放入接收缓冲区,退出
	g_dataReceived[g_byteNumber] = ch;                 // 放入接收缓冲区  
	g_byteNumber++;    
步骤三：修改定时器中断，添加记录接收字节数代码。
	static uint32_t oldbyteNumber = 0;
步骤四：添加验证中断是否结束的代码。若是中断已经结束，则g_byteNumber和 oldbyteNumber相等。
	 if (g_byteNumber != oldbyteNumber)
    {
        oldbyteNumber = g_byteNumber;       //更新oldbyteNumber
    }
    else 
    {
		// oldbyteNumber==0 则g_byteNumber==0 ，说明接收还没有开始，不做处理
		if (oldbyteNumber != 0)
		{
			oldbyteNumber = 0;
			event_send(g_EventWord,RECEIVE_EVENT);			
		}
    }	
4. 添加接收线程
定时器中断判断接收成功以后，会给接受线程发送事件，接收线程负责帧校验和数据解析的任务。
步骤1：添加接收线程和接收事件。在07文件夹下新建thread_receive.c文件，在其中新建名为thread_receive的函数，并将函数头添加到includes文件中，在头文件中添加接收事件。
void thread_receive(void)；      //接收线程函数头
#define RECEIVE_EVENT      (1<<5)       //宏定义“接收事件”
步骤2：在自启动线程中添加线程变量并启动接收线程。打开thread_auto.c文件，在其中添加以下代码：
thread_t thd_receive;           //线程变量
// 创建接收线程
thd_receive=thread_create("thd_receive", (void *)thread_receive, 0, (1024*1024 * 5), 14, 20); 
// 启动接收线程
thread_startup(thd_receive);
步骤3：编写接收线程。接受线程首先负责帧头的校验工作，帧头校验无误则会进行CRC校验，两者均无问题会进行数据解析，将数据解析为衣服完整的图像，并向图像获取线程发送事件进行同步。以上任意环节出现问题则会退出接收线程并将相关变量复位。
void thread_receive(void)
{
    uint32_t tEventState; // 事件返回参数使用

    while (1)
    {
        // （2.1）进入“接收事件”RECEIVE_EVENT的等待状态
        printf("金葫芦提示：接收线程【thread_receive】进入【接收事件】等待状态...\r\n");
        event_recv(g_EventWord, RECEIVE_EVENT,
                   EVENT_FLAG_OR | EVENT_FLAG_CLEAR, WAITING_FOREVER, &tEventState);
        // (2.2)解析帧头，帧头不是0XAA55 报错,由于上位机是小端格式发送，因此此处先判断低字节
        if (g_dataReceived[0] != 0x55 && g_dataReceived[1] != 0xAA)
        {
            printf("帧头校验失败，接收数据错误\n");
            g_byteNumber = 0;    // 清接收字节数g_byteNumber
            g_img_pro_flag == 0; // 可以接收新的图片
            goto thread_receive_1;
        }

        // （2.3）以小端模式读取校验和
        uint16_t checksum = g_dataReceived[sizeof(g_dataReceived) - 2];
        checksum |= g_dataReceived[sizeof(g_dataReceived) - 1] << 8;
        // （2.4）根据接收到的数据计算校验和
        uint16_t caculatedCheckSum = crc16_modbus(g_dataReceived, sizeof(g_dataReceived) - 2);

        // （2.5）判断校验和是否正确，不正确退出此次循环
        if (checksum != caculatedCheckSum)
        {
            printf("校验和校验失败，接收数据错误\n");
            g_byteNumber = 0;    // 清接收字节数g_byteNumber
            g_img_pro_flag == 0; // 可以接收新的图片
            goto thread_receive_1;
        }

        // （2.6）校验和校验正确，说明数据接收无误数据，根据接收到的数据组合图像
        for (int row = 0; row < IMG_H; row++)
        {
            for (int col = 0; col < IMG_W; col++)
            {
                uint16_t r = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col];
                uint16_t g = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col + 1];
                uint16_t b = g_dataReceived[2 + NUM_CHANNEL * IMG_W * row + NUM_CHANNEL * col + 2];

                r = (r & 0xF8) << 8;
                g = (g & 0xFC) << 3;
                b = (b & 0xF8) >> 3;

                uint16_t rgb565 = r | g | b;

                g_image1[row][col] = rgb565;
            }
        }

        printf("图像传输校验完成，触发【CAM读取事件】\n");
        g_byteNumber = 0;
        g_img_pro_flag = 1;
        event_send(g_EventWord, CAM_GET_EVENT);
    thread_receive_1:
        __asm("nop");
    }
}
步骤4：编写CRC校验函数。在thread_receive.c文件中添加CRC校验函数。
//=====================================================================
// 函数名称：crc16_modbus
// 功能概要：将数据进行16位的CRC校验，返回校验后的结果值
// 参数说明：ptr:需要校验的数据缓存区
//      len:需要检验的数据长度
// 函数返回：计算得到的校验值?
//=====================================================================
uint16_t crc16_modbus(uint8_t *data, uint32_t length)
{
    uint16_t crc = 0xFFFF;
    for (uint32_t i = 0; i < length; i++)
    {
        crc ^= (uint16_t)data[i];
        for (uint8_t j = 0; j < 8; j++)
        {
            uint8_t lsb = crc & 0x0001;
            crc >>= 1;
            if (lsb)
            {
                crc ^= 0xA001;
            }
        }
    }
    return crc;
}

至此，验证程序已经编写结束，可以通过validate_model_python上位机程序发送图片进行模型的验证。
