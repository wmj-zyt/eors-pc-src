//=====================================================================
//文件名称：model_preprocess.h
//功能概要：模型驱动构件源文件
//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)
//版    本：2022-07-14  V2.0
//适用芯片：D1
//=====================================================================
#ifndef IMGPRE_H
#define IMGPRE_H

#include "user.h"
#include "math.h"

void imgpre_contrast(uint16_t h,uint16_t w,uint16_t img1[h][w],\
                      uint16_t img2[h][w],float alpha, float beta);

void img888pre_To3DArray(uint16_t h,uint16_t w,uint16_t chl,\
                          uint8_t img[chl][h][w],float output[chl][h][w]);


#endif    
