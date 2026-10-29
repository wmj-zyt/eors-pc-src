//=====================================================================
//文件名称：ov7670.c
//功能概要：ov7670摄像头底层驱动构件文件
//版    本：2020-08-09
//使用芯片：STM32L433xx
//=====================================================================

//包含头文件
#include "cam.h"

//=================内部调用函数声明=====================================
void Delay_us(uint32_t us);
void reg_init();
void reg_write(uint8_t regID, uint8_t regDat);
void reg_read(uint8_t regID, uint8_t *regDat);
uint8_t SCCB_RD_Reg(uint8_t reg);
uint8_t SCCB_WR_Reg(uint8_t reg,uint8_t data);
void config_window(uint16_t x,uint16_t y,uint16_t w, uint16_t h);

//=====================================================================
//函数名称：cam_init
//函数返回：0：配置成功
//         1：失败
//         2：读取到数据但是不正确，重新初始化一次
//参数说明：无
//功能概要：cam初始化相关配置
//=====================================================================
uint8_t cam_init()
{
	uint8_t state;
	//初始化引脚
	gpio_init(cam_FIFO_RCK,1,0);
	gpio_init(cam_VSYNC, 0, 1);			//初始化帧中断读取引脚
	//初始化图像数据接收8个引脚
	gpio_init(cam_DATA_IO_0, 0, 1);
	gpio_init(cam_DATA_IO_1, 0, 1);
	gpio_init(cam_DATA_IO_2, 0, 1);
	gpio_init(cam_DATA_IO_3, 0, 1);
	gpio_init(cam_DATA_IO_4, 0, 1);
	gpio_init(cam_DATA_IO_5, 0, 1);
	gpio_init(cam_DATA_IO_6, 0, 1);  
	gpio_init(cam_DATA_IO_7, 0, 1);
	//初始化摄像头输出使能脚
	gpio_init(cam_FIFO_OE,1,0);
	Delay_us(50);
	//初始化SCCB通信协议
	gpio_init(SCLK,1,1);
	gpio_init(SDIO,1,1);
	Delay_us(1);
	reg_write(0x12, 0X80);	//读取0X12寄存器
	Delay_us(50);
	//初始化ov7670寄存器
	reg_init();
	Delay_us(50);
	//设置摄像头输出的窗口格式为320*240
	config_window(12,174,240,320);	
	reg_read(0x79, &state);
	//判断是否初始化成功
	if(state==0x26)
	{
		return 0;					//成功
	}
	else if(state==0xff)
	{
		return 1; 					//读取不到数据 硬件接线问题
	}
	else
	{
		return 2;					//读取到数据但是不正确 重新初始化一次
	}
}

//======================================================================
//程序名称：cam_enabledata
//函数功能：摄像头中断服务例程调用二次则有图像数据可取
//函数返回：1：有图像可读
//======================================================================
uint8_t cam_enabledata()
{
   static uint8_t  cnt=1;
   if (cnt == 1)
	{
	    //写指针复位
		gpio_init(cam_FIFO_WRST,1,0); //FIFO读使能复位口电平输出
        Delay_us(1);
		gpio_init(cam_FIFO_WRST,1,1); //FIFO读使能复位口电平输出
        Delay_us(1);
		gpio_init(cam_FIFO_WR,1,1);//FIFO写使能口电平输出 禁止写入FIFO
        cnt=0;
	}
    else if (cnt == 0)
    {
		gpio_init(cam_FIFO_WR,1,0);//FIFO写使能口电平输出 写入FIFO
		Delay_us(1);
		gpio_init(cam_FIFO_WRST,1,1); //FIFO读使能复位口电平输出
		Delay_us(1);
		gpio_init(cam_FIFO_WRST,1,1); //FIFO读使能复位口电平输出
		cnt=1;
    }
	return cnt;	
}

//=====================================================================
//函数名称：cam_getimg
//函数返回：无
//参数说明：w=图片宽度<240,h=图片高度<320,*point图像存放地址
//功能概要：获得指定大小(w*h)的RGB图像
//=====================================================================
void cam_getimg(uint16_t w,uint16_t h,uint16_t point[h][w])
{
	//【1】初始化相关变量
	register uint16_t j,i;
 	register uint16_t color=0;
 	uint32_t count=0;
 	//【2】得到FIFO缓冲区缓冲结束信号
	//(2.1)停止ov7670输出图像
	gpio_init(cam_FIFO_OE,1,0);//FIFO输出使能电平输出
	//(2.2)开始复位读指针
	gpio_init(cam_FIFO_RRST,1,0);//FIFO写使能复位电平输出
	gpio_init(cam_FIFO_RCK,1,0);//FIFO时钟口电平输出
	gpio_init(cam_FIFO_RCK,1,1);//FIFO时钟口电平输出
	gpio_init(cam_FIFO_RCK,1,0);//FIFO时钟口电平输出
	gpio_init(cam_FIFO_RRST,1,1);//FIFO写使能复位电平输出,复位读指针结束
	gpio_init(cam_FIFO_RCK,1,1);//FIFO时钟口电平输出
	//【3】读取FIFO缓冲区的像素数据并显示
	for(i=0;i<240;i++)
	{			
		for(j=0;j<320;j++)
		{						    
			PF_DAT &= ~(0x1 << 0);                  //时钟口置低电平
			if(i>=120-h/2 && i< 120-h/2+h && j>=160-w/2 && j< 160-w/2+w)
			{
				//(3.1)首先读取RGB像素点的高八位
				color=(PD_DAT & 0xFF);
			    PF_DAT |= (0x1 << 0);               //时钟口置高电平
				//(3.2)像素点左移8位读取低八位数据
				color <<= 8;
				__asm("nop");
				//(3.3)读取RGB像素点的低八位并合成16位RGB数据
				PF_DAT &= ~(0x1 << 0);              //时钟口置低电平
				__asm("nop");
				//读取到完整的16位彩色像素数据
				color |= (PD_DAT & 0xFF);				    					
				//point[count++]=color; 
				 point[count/w][count%w]=color;
				 count++;
			}
			else
			{
				PF_DAT |= (0x1 << 0);     //时钟口置高电平                 		
				PF_DAT &= ~(0x1 << 0);    //时钟口置低电平
			}
			PF_DAT |= (0x1 << 0);         //时钟口置高电平  
		}
	}
	//【4】重新复位ov7670输出使能
	gpio_init(cam_FIFO_OE,1,1);   //FIFO输出使能电平输出
	gpio_init(cam_FIFO_RCK,1,0);  //FIFO时钟口电平输出
	gpio_init(cam_FIFO_RCK,1,1);  //FIFO时钟口电平输出
}

//=====================================================================
//函数名称：cam_enable_int
//函数返回：无
//参数说明：无
//功能概要：使能摄像头帧中断
//=====================================================================
void cam_enable_int()
{
   gpio_enable_int(cam_VSYNC,FALLING_EDGE);
}  

//=====================================================================
//函数名称：cam_disable_int
//函数返回：无
//参数说明：无
//功能概要：禁止摄像头帧中断
//=====================================================================
void cam_disable_int()
{
    gpio_disable_int(cam_VSYNC);
} 

//=====================================================================
//函数名称：cam_clear_int
//函数返回：无
//参数说明：无
//功能概要：清除摄像头帧中断标志
//=====================================================================
void cam_clear_int()
{
	gpio_clear_int(cam_VSYNC); 
}

//=====================================================================
//函数名称：cam_get_int
//函数返回：CAM帧中断（1或0）1表示引脚有CAM中断，0表示引脚没有CAM中断。
//参数说明：无
//功能概要：摄像头每采集一幅图像，产生本中断
//=====================================================================
uint8_t cam_get_int()
{
    return gpio_get_int(cam_VSYNC);
}


//----------------------以下为内部函数存放处----------------------------


//=====================================================================
//函数名称：cam_gpio_init
//函数返回：无
//参数说明：无
//功能概要：初始化ov7670使用的gpio引脚
//=====================================================================
void cam_gpio_init()
{	
	//初始化控制脚
	gpio_init(cam_FIFO_RCK,1,0);
	gpio_init(cam_VSYNC, 0, 1);			//初始化帧中断读取引脚
	
	//初始化图像数据接收8个引脚
	gpio_init(cam_DATA_IO_0, 0, 1);
	gpio_init(cam_DATA_IO_1, 0, 1);
	gpio_init(cam_DATA_IO_2, 0, 1);
	gpio_init(cam_DATA_IO_3, 0, 1);
	gpio_init(cam_DATA_IO_4, 0, 1);
	gpio_init(cam_DATA_IO_5, 0, 1);
	gpio_init(cam_DATA_IO_6, 0, 1);  
	gpio_init(cam_DATA_IO_7, 0, 1);
		
	//初始化摄像头输出使能脚
	gpio_init(cam_FIFO_OE,1,0);
}

//=====================================================================
//函数名称：cam_config_window
//函数返回：无
//参数说明：x：设置图像开始读取的x坐标
//		    y：设置图像开始读取的y坐标
//			w：设置显示图像窗口的宽度
//			h：设置显示图像窗口的高度
//功能概要：设置ov7670传输后显示图像的窗口参数
//          (140,16,640,480)适合VGA格式输出的图像
//          (272,16,320,240)适合QVGA格式输出的图像
//=====================================================================
void config_window(uint16_t x,uint16_t y,uint16_t w, uint16_t h)
{
	uint16_t endx;						//图像结束点的x坐标
	uint16_t endy;						//图像结束点的y坐标
	uint8_t temp_reg1, temp_reg2;

	//设置图像显示结束点的横纵坐标
	endx=(x+w*2);
	endy=(y+h*2);
	
	//参数判断
	if(endy>784) endy-=784;

	//修改图像输出的开始与结束像素点
    reg_read(0x03, &temp_reg1 );
	temp_reg1 &= 0xf0;
	temp_reg1|=((endx&0X03)<<2)|(x&0X03);
	reg_write(0X03,temp_reg1);
	reg_write(0X19,x>>2);
	reg_write(0X1A,endx>>2);

	reg_read(0x32, &temp_reg2 );
	temp_reg2 &= 0xc0;
	temp_reg2|=((endy&0x7)<<3)|(y&0x7);
	reg_write(0x17, y>>3 );
	reg_write(0x18, endy>>3);
}

//=====================================================================
//函数名称：reg_write
//函数返回：无
//参数说明：regID：寄存器地址
//			regDat：写入数值
//功能概要：更改ov7670指定地址寄存器参数
//=====================================================================
 void reg_write(uint8_t regID, uint8_t regDat)
{
	SCCB_WR_Reg(regID,regDat);
}

//=====================================================================
//函数名称：reg_read
//函数返回：无
//参数说明：regID：寄存器地址
//			regDat：写入数值
//功能概要：读取ov7670指定地址寄存器参数
//=====================================================================
 void reg_read(uint8_t regID, uint8_t *regDat)
{
	*regDat=SCCB_RD_Reg(regID);
}

//=====================================================================
//函数名称：reg_init
//函数返回：无
//参数说明：
//功能概要：参考官方手册配置ov7670寄存器
//=====================================================================
void reg_init()
{
	reg_write(0x3a, 0x04);
	reg_write(0x40, 0xd0);			//565
	reg_write(0x12, 0x14);			//QVGA,RGB输出
	//输出窗口设置
	reg_write(0x32, 0x80);
	reg_write(0x17, 0x16);
	reg_write(0x18, 0x04);
	reg_write(0x19, 0x02);
	reg_write(0x1a, 0x7b);
	reg_write(0x03, 0x06);			//帧竖直方向控制
	
	reg_write(0x0c, 0x00);
	reg_write(0x15, 0x00);
	reg_write(0x3e, 0x00);
	reg_write(0x70, 0x3a);
	reg_write(0x71, 0x35);
	reg_write(0x72, 0x11);
	reg_write(0x73, 0x00);

	reg_write(0xa2, 0x02);
	reg_write(0x11, 0x81);           //时钟分频设置，0，不分频
	reg_write(0x7a, 0x20);
	reg_write(0x7b, 0x1c);
	reg_write(0x7c, 0x28);

	reg_write(0x7d, 0x3c);
	reg_write(0x7e, 0x55);
	reg_write(0x7f, 0x68);
	reg_write(0x80, 0x76);
	reg_write(0x81, 0x80);

	reg_write(0x82, 0x88);
	reg_write(0x83, 0x8f);
	reg_write(0x84, 0x96);
	reg_write(0x85, 0xa3);
	reg_write(0x86, 0xaf);

	reg_write(0x87, 0xc4);
	reg_write(0x88, 0xd7);
	reg_write(0x89, 0xe8);
	reg_write(0x13, 0xe0);
	reg_write(0x00, 0x00);

	reg_write(0x10, 0x00);
	reg_write(0x0d, 0x30);            //全窗口， 位[5:4]: 01 半窗口，10 1/4窗口，11 1/4窗口
	reg_write(0x14, 0x28);
	reg_write(0xa5, 0x05);
	reg_write(0xab, 0x07);

	reg_write(0x24, 0x75);
	reg_write(0x25, 0x63);
	reg_write(0x26, 0xA5);
	reg_write(0x9f, 0x78);
	reg_write(0xa0, 0x68);

	reg_write(0xa1, 0x03);			//0x0b,
	reg_write(0xa6, 0xdf);			//0xd8,
	reg_write(0xa7, 0xdf);			//0xd8,
	reg_write(0xa8, 0xf0);
	reg_write(0xa9, 0x90);

	reg_write(0xaa, 0x94);
	reg_write(0x13, 0xe5);
	reg_write(0x0e, 0x61);
	reg_write(0x0f, 0x4b);
	reg_write(0x16, 0x02);

//	reg_write(0x1e, 0x37);			//图像输出镜像控制.0x07
//	reg_write(0x21, 0x02);
//	reg_write(0x22, 0x91);
//	reg_write(0x29, 0x07);
//	reg_write(0x33, 0x0b);

	reg_write(0x35, 0x0b);
	reg_write(0x37, 0x1d);
	reg_write(0x38, 0x71);
	reg_write(0x39, 0x2a);
	reg_write(0x3c, 0x78);

	reg_write(0x4d, 0x40);
	reg_write(0x4e, 0x20);
	reg_write(0x69, 0x00);
	reg_write(0x6b, 0x40); /////
	reg_write(0x74, 0x19);
	reg_write(0x8d, 0x4f);

	reg_write(0x8e, 0x00);
	reg_write(0x8f, 0x00);
	reg_write(0x90, 0x00);
	reg_write(0x91, 0x00);
	reg_write(0x92, 0x00);

	reg_write(0x96, 0x00);
	reg_write(0x9a, 0x80);
	reg_write(0xb0, 0x84);
	reg_write(0xb1, 0x0c);
	reg_write(0xb2, 0x0e);

	reg_write(0xb3, 0x82);
	reg_write(0xb8, 0x0a);
	reg_write(0x43, 0x14);
	reg_write(0x44, 0xf0);
	reg_write(0x45, 0x34);

	reg_write(0x46, 0x58);
	reg_write(0x47, 0x28);
	reg_write(0x48, 0x3a);
	reg_write(0x59, 0x88);
	reg_write(0x5a, 0x88);

	reg_write(0x5b, 0x44);
	reg_write(0x5c, 0x67);
	reg_write(0x5d, 0x49);
	reg_write(0x5e, 0x0e);
	reg_write(0x64, 0x04);
	reg_write(0x65, 0x20);

	reg_write(0x66, 0x05);
	reg_write(0x94, 0x04);
	reg_write(0x95, 0x08);
	reg_write(0x6c, 0x0a);
	reg_write(0x6d, 0x55);

	reg_write(0x4f, 0x80);
	reg_write(0x50, 0x80);
	reg_write(0x51, 0x00);
	reg_write(0x52, 0x22);
	reg_write(0x53, 0x5e);
	reg_write(0x54, 0x80);

	reg_write(0x09, 0x03);           //驱动能力最大

	reg_write(0x6e, 0x11);
	reg_write(0x6f, 0x9f);
	reg_write(0x55, 0x40);			//亮度控制  30
	reg_write(0x56, 0x40);			//对比度 0x40
	reg_write(0x57, 0x40);

	reg_write(0x6a, 0x40);
	reg_write(0x01, 0x40);
	reg_write(0x02, 0x40);
	reg_write(0x13, 0xe7);
	reg_write(0x15, 0x00);

	reg_write(0x58, 0x9e);

	reg_write(0x41, 0x08);
	reg_write(0x3f, 0x00);
	reg_write(0x75, 0x05);
	reg_write(0x76, 0xe1);
	reg_write(0x4c, 0x00);
	reg_write(0x77, 0x01);
	reg_write(0x3d, 0xc2);
	reg_write(0x4b, 0x09);
	reg_write(0xc9, 0x60);
	reg_write(0x41, 0x38);

	reg_write(0x34, 0x11);
	reg_write(0x3b, 0x02);

	reg_write(0xa4, 0x89);
	reg_write(0x96, 0x00);
	reg_write(0x97, 0x30);
	reg_write(0x98, 0x20);
	reg_write(0x99, 0x30);
	reg_write(0x9a, 0x84);
	reg_write(0x9b, 0x29);
	reg_write(0x9c, 0x03);
	reg_write(0x9d, 0x4c);
	reg_write(0x9e, 0x3f);
	reg_write(0x78, 0x04);

	reg_write(0x79, 0x01);
	reg_write(0xc8, 0xf0);
	reg_write(0x79, 0x0f);
	reg_write(0xc8, 0x00);
	reg_write(0x79, 0x10);
	reg_write(0xc8, 0x7e);
	reg_write(0x79, 0x0a);
	reg_write(0xc8, 0x80);
	reg_write(0x79, 0x0b);
	reg_write(0xc8, 0x01);
	reg_write(0x79, 0x0c);
	reg_write(0xc8, 0x0f);
	reg_write(0x79, 0x0d);
	reg_write(0xc8, 0x20);
	reg_write(0x79, 0x09);
	reg_write(0xc8, 0x80);
	reg_write(0x79, 0x02);
	reg_write(0xc8, 0xc0);
	reg_write(0x79, 0x03);
	reg_write(0xc8, 0x40);
	reg_write(0x79, 0x05);
	reg_write(0xc8, 0x30);
	reg_write(0x79, 0x26);
	reg_write(0x09, 0x00);
}


//---------以下为串行摄像机控制总线协议(SCCB)底层驱动构件文件--------------
//=====================================================================
//函数名称：SCCB_Start
//函数返回：无
//参数说明：无
//功能概要：开启SCCB
//=====================================================================
void SCCB_Start(void)
{
	gpio_set(SDIO,1);			//SDIO保持高电平
	gpio_set(SCLK,1);			//SCLK保持高电平
	Delay_us(50);
	gpio_set(SDIO,0);			//SDIO拉低
	Delay_us(50);
	gpio_set(SCLK,0);			//SCLK拉低
}

//=====================================================================
//函数名称：SCCB_Stop
//函数返回：无
//参数说明：无
//功能概要：停止SCCB
//=====================================================================
void SCCB_Stop(void)
{
	gpio_set(SDIO,0);	
	Delay_us(50);
	gpio_set(SCLK,1);
	Delay_us(50);
	gpio_set(SDIO,1);	
	Delay_us(50);
}
//=====================================================================
//函数名称：SCCB_WR_Byte
//函数返回：0，成功；1：失败
//参数说明：单个数据字节
//功能概要：通过SCCB写一个字节
//=====================================================================
uint8_t SCCB_WR_Byte(uint8_t dat)
{
	uint8_t j,res;	
	for(j=0;j<8;j++)
	{
		if(dat&0x80) gpio_set(SDIO,1);	
		else gpio_set(SDIO,0);
		dat<<=1;
		Delay_us(50);
		gpio_set(SCLK,1);	
		Delay_us(50);
		gpio_set(SCLK,0);
	}	

	gpio_init(SDIO, 0, 1);		//将GPIO设置为输入模式
	gpio_pull(SDIO,1);

	//gpio_init(SDIO,0,0);		
	Delay_us(50);
	gpio_set(SCLK,1);
	Delay_us(50);
	if(gpio_get(SDIO)) res=1;
	else res=0;         
	gpio_set(SCLK,0);  
	gpio_init(SDIO,1,1);
	return res;  
}
//=====================================================================
//函数名称：SCCB_RD_Byte
//函数返回：读到的字节
//参数说明：无
//功能概要：通过SCCB读一个字节
//=====================================================================
uint8_t SCCB_RD_Byte(void)
{
	uint8_t temp=0,j;    
	//gpio_init(SDIO,0,0);	
	gpio_init(SDIO, 0, 1);		//将GPIO设置为输入模式
	gpio_pull(SDIO,1);
	
	Delay_us(50);
	for(j=8;j>0;j--) 	
	{		     	  
		Delay_us(50);
		gpio_set(SCLK,1);
		temp=temp<<1;
		if(gpio_get(SDIO)) temp++;   
		Delay_us(50);
		gpio_set(SCLK,0);
	}	
	gpio_init(SDIO,1,1);			  
	return temp;
} 	

//=====================================================================
//函数名称：SCCB_WR_Reg
//函数返回：0，成功；1：失败
//参数说明：reg:寄存器，data：数值
//功能概要：写一个寄存器
//=====================================================================
uint8_t SCCB_WR_Reg(uint8_t reg,uint8_t data)
{
	uint8_t res=0;
	SCCB_Start(); 					
	if(SCCB_WR_Byte(SCCB_ID)) res=1;	 
	Delay_us(100);
  	if(SCCB_WR_Byte(reg)) res=1;	  
	Delay_us(100);
  	if(SCCB_WR_Byte(data)) res=1; 	 
  	SCCB_Stop();	  
  	return	res;
}

//=====================================================================
//函数名称：SCCB_RD_Reg
//函数返回：0，成功；1：失败
//参数说明：reg:寄存器
//功能概要：读寄存器
//=====================================================================
uint8_t SCCB_RD_Reg(uint8_t reg)
{
	uint8_t val=0;
	SCCB_Start(); 				
	SCCB_WR_Byte(SCCB_ID);		
	Delay_us(100);	 
  	SCCB_WR_Byte(reg);		  
	Delay_us(100);	  
	SCCB_Stop();   
	Delay_us(100);	   
	SCCB_Start();
	SCCB_WR_Byte(SCCB_ID|0X01);  
	Delay_us(100);
  	val=SCCB_RD_Byte();
	Delay_us(50);
	gpio_set(SDIO,1);	
	gpio_set(SCLK,1);	
	Delay_us(50);
	gpio_set(SCLK,0);	
	Delay_us(50);
	gpio_set(SDIO,0);		
	Delay_us(50);
  	SCCB_Stop();
  	return val;
}

void Delay_us(uint32_t us)
{
	uint32_t i;
	for(i = 0; i < 10*us; i++)
	{
		 __asm ("NOP") ;
	}
}
