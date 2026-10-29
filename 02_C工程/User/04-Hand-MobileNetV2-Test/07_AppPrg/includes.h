///=====================================================================
// 文件名称：includes.h文件
// 框架提供：苏大嵌入式（sumcu.suda.edu.cn）
// 版本更新：20230915
// 移植规则：【固定】
//=====================================================================

#ifndef  INCLUDES_H     //防止重复定义（INCLUDES_H 开头）
#define  INCLUDES_H

//----------------------------------------------------------------------
//（1）包含用到的构件
#include "user.h"
#include "NumToStr.h"
#include "imgpre.h"
#include "mobilenetv2.h"

//----------------------------------------------------------------------
//（2）全局使用的宏常数。
#define NUM_CHANNEL  3

#define CRC_OK_EVENT       (1<<1)       //宏定义“CAM读取事件”
#define PRETREAT_EVENT     (1<<2)       //宏定义“图像预处理事件”
#define REASONING_EVENT    (1<<3)       //宏定义“推理事件”
#define SECPRG_EVENT       (1<<4)       //宏定义“二次编程事件”
#define RECEIVE_EVENT      (1<<5)       //宏定义“接收事件”

#define IMG_H  CAMIMG_H          //图像高
#define IMG_W  CAMIMG_W          //图像宽

//----------------------------------------------------------------------
//（3）自定义数据类型
// 字宏定义
//----------------------------------------------------------------------

//（4）声明全局变量。命名规范见注2。
//【不动】宏定义全局变量前缀G_VAR_PREFIX。实现原理见注3。
#ifdef GLOBLE_VAR              //GLOBLE_VAR在main.c文件中有宏定义
  #define G_VAR_PREFIX         //前缀G_VAR_PREFIX定义为空
#else                          //GLOBLE_VAR在非main.c文件中无定义
  #define G_VAR_PREFIX extern  //前缀G_VAR_PREFIX定义为"extern"
#endif
//（在此增加全局变量）
G_VAR_PREFIX vuint8_t  g_Time[3];        //时间数组
G_VAR_PREFIX vuint8_t  g_TimerCount;
G_VAR_PREFIX uint16_t  g_image1[IMG_H][IMG_W];    //图像数组1
G_VAR_PREFIX uint16_t  g_image2[IMG_H][IMG_W];    //图像数组1

G_VAR_PREFIX uint8_t   g_image3[3][IMG_H][IMG_W];    //图像数组1


G_VAR_PREFIX vuint8_t  g_img_pro_flag;
G_VAR_PREFIX vuint32_t  g_byteNumber;

G_VAR_PREFIX sem_t g_semCapture;    // 获取图像信号量
G_VAR_PREFIX sem_t g_semInference;  // 推理信号量
G_VAR_PREFIX event_t g_getImg;      // 完整接收一帧图片事件
G_VAR_PREFIX float g_modelInputImage[NUM_CHANNEL][IMG_H][IMG_W]; // 模型输入图像
G_VAR_PREFIX uint8_t g_dataReceived[IMG_H * IMG_W * NUM_CHANNEL + 2 + 2]; // 模型输入图像
G_VAR_PREFIX   event_t    g_EventWord;         //声明事件字g_EventWord
G_VAR_PREFIX   char*      g_classification[SortNum];  //分类名称（字符串）数组
G_VAR_PREFIX   float      g_result[SortNum];          //分类值数组

//----------------------------------------------------------------------

// 线程函数声明
void thread_auto();
void thread_unframe();
void thread_inference();
void thread_secprg();
void thread_imgpre();

#endif                  //防止重复定义（INCLUDES_H 结尾）


/*
 知识要素：
 注1：全局使用的宏常数，使用全大写
 注2：全局变量命名一律以g开头，尽可能保证全工程内唯一性，并且一定要注明
      其含义，（声明时不准赋值）
 注3：全局变量一处声明多处使用处理方法代码段是为了解决全局变量重复声明
 的问题，宏GLOBLE_VAR仅在main.c中声明，所以只有在main.c中包含
 本头文件时才会声明全局变量，在其他文件中包含本文件时，编译时，就会自动加
 上前缀extern，表明是main函数中声明的全局变量，该文件中直接使用。
 */


