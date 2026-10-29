//=====================================================================
//文件名称：model_preprocess.c
//功能概要：模型驱动构件源文件
//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)
//版    本：2022-07-14  V2.0
//适用芯片：D1-H
//=====================================================================

//包含的头文件
#include "imgpre.h"

//=================内部调用函数声明=====================================

//=====================================================================
//函数名称:enhance_contrast_rgb565
//函数返回:无
//参数说明: originImage:二维数组 factor:对比度(3.0-8.0)
//功能概要:增强图像对比度
//=====================================================================
void imgpre_contrast(uint16_t h,uint16_t w,uint16_t img1[h][w],\
                      uint16_t img2[h][w],float alpha, float beta)
{
	for(int i=0; i<h; i++){
		for(int j=0; j<w; j++){
			uint16_t pixel = img1[i][j];
			// 提取RGB分量
			uint8_t r = (pixel >> 11) & 0x1F; // R占用高5位
			uint8_t g = (pixel >> 5) & 0x3F;  // G占用中间6位
			uint8_t b = pixel & 0x1F;         // B占用低5位
			// 转换到8位范围(0-255)
			r = (r << 3) | (r >> 2);
			g = (g << 2) | (g >> 4);
            b = (b << 3) | (b >> 2);
			// 应用对比度增强公式
			int r1 = (int)(r * alpha + beta);
            int g1 = (int)(g * alpha + beta);
            int b1 = (int)(b * alpha + beta); 
			// 限制范围到 [0, 255]
            r1 = (r1 > 255) ? 255 : (r1 < 0) ? 0 : r1;
            g1 = (g1 > 255) ? 255 : (g1 < 0) ? 0 : g1;
            b1 = (b1 > 255) ? 255 : (b1 < 0) ? 0 : b1;
			// 转换回 RGB565 格式
            r = r1 >> 3;
            g = g1 >> 2;
            b = b1 >> 3;
			// 重新组合成 16 位像素
			img2[i][j] = (r << 11) | (g << 5) | b;
		}
	}
}

// void imgpre_contrast(uint16_t h,uint16_t w,uint16_t img1[h][w],
//                       uint16_t img2[h][w],float factor)
// {
// 	for(int i=0; i<h; i++){
// 		for(int j=0; j<w; j++){
// 			uint16_t pixel = img1[i][j];
// 			// 提取RGB分量
// 			uint8_t r = (pixel >> 11) & 0x1F; // R占用高5位
// 			uint8_t g = (pixel >> 5) & 0x3F;  // G占用中间6位
// 			uint8_t b = pixel & 0x1F;         // B占用低5位
// 			// 转换到8位范围(0-255)
// 			r = (r << 3) | (r >> 2);
// 			g = (g << 2) | (g >> 4);
//             b = (b << 3) | (b >> 2);
// 			// 应用对比度增强公式
// 			int r1 = (int)((r - 128) * factor + 128);
//             int g1 = (int)((g - 128) * factor + 128);
//             int b1 = (int)((b - 128) * factor + 128); 
// 			// 限制范围到 [0, 255]
//             r1 = (r1 > 255) ? 255 : (r1 < 0) ? 0 : r1;
//             g1 = (g1 > 255) ? 255 : (g1 < 0) ? 0 : g1;
//             b1 = (b1 > 255) ? 255 : (b1 < 0) ? 0 : b1;
// 			// 转换回 RGB565 格式
//             r = r1 >> 3;
//             g = g1 >> 2;
//             b = b1 >> 3;
// 			// 重新组合成 16 位像素
// 			img2[i][j] = (r << 11) | (g << 5) | b;
// 		}
// 	}
// }


void img888pre_To3DArray(uint16_t h,uint16_t w,uint16_t chl,\
                          uint8_t img[chl][h][w],float output[chl][h][w])
{
	uint16_t i, j;
	uint8_t red, green, blue;
	for(i = 0; i < h; i++){
		for(j = 0; j < w; j++){
			red = img[0][i][j]; 
			green = img[1][i][j];
			blue = img[2][i][j];
			output[0][i][j] = (float)(red * (1.0 / 255));
			output[1][i][j] = (float)(green * (1.0 / 255));
			output[2][i][j] = (float)(blue * (1.0 / 255));
		}
	}
}


//----------------------以下为内部函数存放处----------------------------

//=====================================================================
//函数名称:cubic_weight
//函数返回:权重
//参数说明: x：像素位置
//功能概要:  Cubic Spline 插值函数
//=====================================================================
double cubic_weight(double x) {
    x = fabs(x);
    if (x <= 1) {
        return 1.5 * pow(x, 3) - 2.5 * pow(x, 2) + 1;
    } else if (x <= 2) {
        return -0.5 * pow(x, 3) + 2.5 * pow(x, 2) - 4 * x + 2;
    } else {
        return 0;
    }
}

//=====================================================================
//函数名称:decode_rgb
//函数返回:无
//参数说明: pixel：16-bit像素值 r：传回红色通道像素值分量 g：传回绿色通道像素值分量 b：传回蓝色通道像素值分量
//功能概要: 将 16-bit 整数的像素值解码为 RGB 分量
//=====================================================================
// 
void decode_rgb(uint16_t pixel, uint8_t *r, uint8_t *g, uint8_t *b) {
    *r = (pixel >> 11) & 0x1F;  // 5 bits for red
    *g = (pixel >> 5) & 0x3F;   // 6 bits for green
    *b = pixel & 0x1F;           // 5 bits for blue
}

//=====================================================================
//函数名称:encode_rgb
//函数返回:16bit像素值
//参数说明: r：红色通道像素值 g：绿色通道像素值 b：蓝色通道像素值
//功能概要: 将 RGB 分量编码为 16-bit 像素值
//=====================================================================
uint16_t encode_rgb(uint8_t r, uint8_t g, uint8_t b) {
    uint16_t pixel = 0;
    pixel |= (r & 0x1F) << 11;  // 5 bits for red
    pixel |= (g & 0x3F) << 5;   // 6 bits for green
    pixel |= (b & 0x1F);         // 5 bits for blue
    return pixel;
}