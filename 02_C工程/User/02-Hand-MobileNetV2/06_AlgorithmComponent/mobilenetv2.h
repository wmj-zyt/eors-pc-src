//=====================================================================
//文件名称：model_ops.h
//功能概要：模型驱动构件源文件
//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)
//版    本：2022-07-14  V1.0
//适用芯片：D1
//=====================================================================
#ifndef MODEL_OPS_H
#define MODEL_OPS_H

#include <math.h>
#include <string.h>

#define max(a, b) (((a) > (b)) ? (a) : (b))

//=====================================================================
// 函数名称:GETLENGTH
// 函数返回:数组长度
// 参数说明:array:输入数组
// 功能概要:计算数组元素个数
//=====================================================================
#define GETLENGTH(array) (sizeof(array) / sizeof(*(array)))

//=====================================================================
// 函数名称:GETCOUNT
// 函数返回:float数组元素个数
// 参数说明:array:输入数组
// 功能概要:计算float类型的数组个数
//=====================================================================
#define GETCOUNT(array) (sizeof(array) / sizeof(float))

//=====================================================================
// 函数名称:FOREACH
// 函数返回:无
// 参数说明:   i:临时计数变量
//        count:总循环次数
// 功能概要:进行for循环
//=====================================================================
#define FOREACH(i, count) for (int i = 0; i < count; ++i)

//=====================================================================
// 函数名称:Data_Padding
// 函数返回:无
// 参数说明:input:输入层元素数组指针，afterPadding:填充后元素数组指针,p:填充所需元素
// 功能概要:填充输入层
//=====================================================================
#define Data_Padding(input, afterPadding, pad_top, pad_right, pad_bottom, pad_left)                                                       \
	{                                                                                                                                     \
		FOREACH(h, GETLENGTH(afterPadding))                                                                                               \
		FOREACH(w, GETLENGTH(*afterPadding))                                                                                              \
		{                                                                                                                                 \
			if (w < pad_left || w >= (GETLENGTH(*afterPadding) - pad_right) || h < pad_top || h >= (GETLENGTH(afterPadding) - pad_bottom)) \
				afterPadding[h][w] = 0;                                                                                                   \
			else                                                                                                                          \
				afterPadding[h][w] = input[h - pad_top][w - pad_left];                                                                    \
		}                                                                                                                                 \
	}

//=====================================================================
// 函数名称:CONVOLUTE_VALID
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//		  output:输出层元素数组首地址指针
//        weight:输入层与输出层之间权重数组指针
//        s:步长
// 功能概要:进行权重的赋值传播
//=====================================================================
#define CONVOLUTE_VALID(input, output1, weight, s)                                 \
	{                                                                              \
		for (int o0 = 0; o0 < GETLENGTH(output1); ++o0)                            \
			for (int o1 = 0; o1 < GETLENGTH(*output1); ++o1)                       \
				FOREACH(w0, GETLENGTH(weight))                                     \
					FOREACH(w1, GETLENGTH(*(weight)))                                          \
						(output1)[o0][o1] += (input)[o0 * s + w0][o1 * s + w1] * (weight)[w0][w1]; \
	}

//=====================================================================
// 函数名称:DEPTHWISE_CONVOLUTE_VALID
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//		  output:输出层元素数组首地址指针
//        weight:输入层与输出层之间权重数组指针
//        s:步长
// 功能概要:进行深度可分离卷积操作(使用赋值而非累加)
//=====================================================================
#define DEPTHWISE_CONVOLUTE_VALID(input, output1, weight, s)                       \
	{                                                                              \
		for (int o0 = 0; o0 < GETLENGTH(output1); ++o0) {                          \
			for (int o1 = 0; o1 < GETLENGTH(*output1); ++o1) {                     \
				float sum = 0;                                                     \
				FOREACH(w0, GETLENGTH(weight)) {                                   \
					FOREACH(w1, GETLENGTH(*(weight))) {                            \
						sum += (input)[o0 * s + w0][o1 * s + w1] * (weight)[w0][w1];   \
					}                                                              \
				}                                                              \
				(output1)[o0][o1] = sum;                                           \
			}                                                              \
		}                                                                  \
	}

//=====================================================================
// 函数名称:Conv2D
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//		   output:输出层元素数组首地址指针
//         kernel:输入层与输出层之间权值数组指针
//         bias:输入层与输出层之间偏置数组指针
//         strides:步长
//         padding:填充
// 功能概要:进行卷积操作，填充输入，随后做卷积操作
//=====================================================================
#define CONV2D(input, output, kernel, bias, strides, padding)                                                           \
	{                                                                                                                   \
		int pad_top = 0, pad_bottom = 0, pad_left = 0, pad_right = 0;                                                \
		int pad_along_height = 0, pad_along_width = 0;    \
		if(strcmp(padding, "valid") == 0) {                                                           	                \
			pad_top = pad_bottom = pad_left = pad_right = 0;                                          		            \
		} else if(strcmp(padding, "same") == 0) {                                                    		            \
			pad_along_height = max((GETLENGTH(*output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(*input), 0); \
			pad_along_width = max((GETLENGTH(**output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(**input), 0);  \
			pad_top = pad_along_height / 2;                                                                             \
			pad_bottom = pad_along_height - pad_top;                                                                    \
			pad_left = pad_along_width / 2;                                                                             \
			pad_right = pad_along_width - pad_left;                                                                     \
		}                                                                                                               \
		float padded[GETLENGTH(input)][(GETLENGTH(*input) + pad_along_height)][(GETLENGTH(**input) + pad_along_width)]; \
		FOREACH(i, GETLENGTH(input))                                                                                    \
			Data_Padding(input[i], padded[i], pad_top, pad_right, pad_bottom, pad_left);                                   \
		FOREACH(x, GETLENGTH(kernel))                                                                                   \
			FOREACH(y, GETLENGTH(*kernel))                                                                                  \
				CONVOLUTE_VALID(padded[x], output[y], kernel[x][y], strides);                                                  \
		FOREACH(j, GETLENGTH(output))                                                                                  \
			FOREACH(i, GETCOUNT(output[j]))                                                                                 \
				((float *)output[j])[i] = ((float *)output[j])[i] + bias[j];                                                    \
	}

//=====================================================================
// 函数名称:DEPTHWISE_CONV2D
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//		  output:输出层元素数组首地址指针
//        kernel:输入层与输出层之间权值数组指针
//          bias:输入层与输出层之间偏置数组指针
//        strides:步长
// 功能概要:进行卷积操作，填充输入，随后坐卷积操作
//=====================================================================
#define DEPTHWISE_CONV2D(input, output, kernel, bias, strides)                                                          \
	{                                                                                                                   \
		int pad_along_height = max((GETLENGTH(*output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(*input), 0);    \
		int pad_along_width = max((GETLENGTH(**output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(**input), 0);     \
		int pad_top = pad_along_height / 2;                                                                             \
		int pad_bottom = pad_along_height - pad_top;                                                                    \
		int pad_left = pad_along_width / 2;                                                                             \
		int pad_right = pad_along_width - pad_left;                                                                     \
		float padding[GETLENGTH(input)][(GETLENGTH(*input) + pad_along_height)][(GETLENGTH(**input) + pad_along_width)]; \
		FOREACH(i, GETLENGTH(input))                                                                                    \
			Data_Padding(input[i], padding[i], pad_top, pad_right, pad_bottom, pad_left);                               \
		FOREACH(x, GETLENGTH(kernel))                                                                                   \
			DEPTHWISE_CONVOLUTE_VALID(padding[x], output[x], kernel[x][0], strides);                                                  \
		FOREACH(j, GETLENGTH(output))                                                                                   \
			FOREACH(i, GETCOUNT(output[j]))                                                                                 \
				((float *)output[j])[i] = ((float *)output[j])[i] + bias[j];                                                    \
	}

//=====================================================================
// 函数名称:BATCH_NORMALIZATION
// 函数返回:无
// 参数说明:input:输入层元素数组指针，output:输出元素数组指针
// 数据：eps：增加到方差中的小浮动，以避免被零整除
//     momentum：移动到平均值和移动方差的动量
//     bnParam  0-gamma  1-beta 2-move_mean 3 -move_var
// 功能概要:批量归一化处理
//=====================================================================
#define BATCH_NORMALIZATION(input, bnParam)                                                          \
	{                                                                                                \
		float eps = 0.001;                                                                           \
		float beta[GETLENGTH(*bnParam)];                                                             \
		float gamma[GETLENGTH(*bnParam)];                                                            \
		float move_mean[GETLENGTH(*bnParam)];                                                        \
		float move_var[GETLENGTH(*bnParam)];                                                         \
		float x_normed[GETLENGTH(input)][GETLENGTH(*input)][GETLENGTH(**input)];                     \
		FOREACH(w, GETLENGTH(*bnParam))                                                              \
		{                                                                                            \
			(beta)[w] = (bnParam)[1][w];                                                             \
			(gamma)[w] = (bnParam)[0][w];                                                            \
			(move_mean)[w] = (bnParam)[2][w];                                                        \
			(move_var)[w] = (bnParam)[3][w];                                                         \
		}                                                                                            \
		FOREACH(i, GETLENGTH(input))                                                                 \
			FOREACH(j, GETLENGTH(*input))                                                                \
				FOREACH(k, GETLENGTH(**input))                                                               \
				{                                                                                            \
					(x_normed)[i][j][k] = ((input)[i][j][k] - (move_mean)[i]) / (sqrt((move_var)[i] + eps)); \
					(input)[i][j][k] = gamma[i] * (x_normed)[i][j][k] + (beta)[i];                           \
				}                                                                                            \
	}

//=====================================================================
// 函数名称:ACTIVATION
// 函数返回:无
// 参数说明:input:输入层元素数组指针
//         Active_Fun：激活函数
// 功能概要:激活函数
//=====================================================================
#define ACTIVATION(input, Active_Fun)                                                \
	{                                                                                \
		FOREACH(j, GETLENGTH(input))                                                 \
			FOREACH(i, GETCOUNT(input[j]))                                               \
				((float *)input[j])[i] = Active_Fun(((float *)input[j])[i]);                 \
	}

//=====================================================================
// 函数名称:SOFTMAX
// 函数返回:无
// 参数说明:input:输入层元素数组指针
// 功能概要:softmax激活函数
//=====================================================================
#define SOFTMAX(input)                                                                 \
	{                                                                                   \
		float exparr[GETLENGTH(input)];                                                 \
		float expsum = 0;                                                               \
		FOREACH(i, GETLENGTH(input))                                                   \
		{                                                                               \
			exparr[i] = (float)exp((input)[i][0][0]);                                   \
			expsum += exparr[i];                                                         \
		}                                                                               \
		FOREACH(i, GETLENGTH(input))                                                   \
			(input)[i][0][0] = exparr[i] / expsum;                                           \
	}

//=====================================================================
// 函数名称:GLOBALAVERAGEPOOLING
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//		   output:输出层元素数组首地址指针
// 功能概要:全局平均池化 对最后一层卷积的特征图，每个通道求整个特征图的均值
//=====================================================================
#define GLOBALAVERAGEPOOLING(input, output)                              \
	{                                                                    \
		FOREACH(i, GETLENGTH(input))                                     \
		{                                                                \
			float temp = 0;                                              \
			FOREACH(j, GETLENGTH(*input))                                 \
				FOREACH(k, GETLENGTH(**input))                              \
					temp += (input)[i][j][k];                            \
			(output)[i] = temp / ((GETLENGTH(*input)) * (GETLENGTH(**input))); \
		}                                                                \
	}

//=====================================================================
// 函数名称:ADD
// 函数返回:无
// 参数说明:input1:输入层元素数组首地址指针
//		   input2:输出层元素数组首地址指针
//         output:输出层元素数组首地址指针
// 功能概要:残差连接
//=====================================================================
#define ADD(input1, input2, output)                                     \
	{                                                                   \
		FOREACH(i, GETLENGTH(input1))                                   \
			FOREACH(j, GETLENGTH(*input1))                                  \
				FOREACH(k, GETLENGTH(**input1))                                 \
					(output)[i][j][k] = (input1)[i][j][k] + (input2)[i][j][k];      \
	}

//=====================================================================
// 函数名称:RESHAPE
// 函数返回:无
// 参数说明:input:输入层元素数组首地址指针
//         output:输出层元素数组首地址指针
// 功能概要:变换维度
//=====================================================================
#define RESHAPE(input, output)                                         \
	{                                                                 \
		memcpy(output, input, GETCOUNT(input) * sizeof(float));         \
	}

//=====================================================================
// 函数名称:relu6
// 函数返回:激活值
// 参数说明:x:待激活值
// 功能概要:将输出值限制在(0,6)之间
//=====================================================================
float relu6(float x);

//=====================================================================
// 函数名称:softmax
// 函数返回:无
// 参数说明:input:输入数组指针, dim:数组维度
// 功能概要:Softmax激活函数
//=====================================================================
void softmax(float *input, int dim);

#endif /* MODEL_OPS_H */
//===================================================================== 
//文件名称：mobilenetv2.h 
//功能概要：模型驱动构件头文件 
//版    本：V3.0 
//使用芯片：D1-H 
//构件生成时间：2026年07月09日 17:44:14
//===================================================================== 
#ifndef MODEL_H 
#define MODEL_H 

#define SortNum 0

#define SORT0 ""
#define SORT1 ""
#define SORT2 ""
#define SORT3 ""
#define SORT4 ""
#define SORT5 ""
#define SORT6 ""
#define SORT7 ""
#define SORT8 ""
#define SORT9 ""

#define RESIZED_IMAGE_HEIGHT 150
#define RESIZED_IMAGE_WIDTH 160

const float conv2d_kernel[3][6][3][3];  //卷积层1卷积核的权重
const float conv2d_bias[6];  //卷积层1卷积核的偏置
const float batch_normalization_params[4][6];  //BN归一层1参数
const float conv2d_1_kernel[6][18][1][1];  //卷积层2卷积核的权重
const float conv2d_1_bias[18];  //卷积层2卷积核的偏置
const float batch_normalization_1_params[4][18];  //BN归一层2参数
const float depthwise_conv2d_depthwise_kernel[18][1][3][3];  //深度卷积层1卷积核的权重
const float depthwise_conv2d_bias[18];  //深度卷积层1卷积核的偏置
const float batch_normalization_2_params[4][18];  //BN归一层3参数
const float conv2d_2_kernel[18][8][1][1];  //卷积层3卷积核的权重
const float conv2d_2_bias[8];  //卷积层3卷积核的偏置
const float batch_normalization_3_params[4][8];  //BN归一层4参数
const float conv2d_3_kernel[8][24][1][1];  //卷积层4卷积核的权重
const float conv2d_3_bias[24];  //卷积层4卷积核的偏置
const float batch_normalization_4_params[4][24];  //BN归一层5参数
const float depthwise_conv2d_1_depthwise_kernel[24][1][3][3];  //深度卷积层2卷积核的权重
const float depthwise_conv2d_1_bias[24];  //深度卷积层2卷积核的偏置
const float batch_normalization_5_params[4][24];  //BN归一层6参数
const float conv2d_4_kernel[24][8][1][1];  //卷积层5卷积核的权重
const float conv2d_4_bias[8];  //卷积层5卷积核的偏置
const float batch_normalization_6_params[4][8];  //BN归一层7参数
const float conv2d_5_kernel[8][10][3][3];  //卷积层6卷积核的权重
const float conv2d_5_bias[10];  //卷积层6卷积核的偏置
const float batch_normalization_7_params[4][10];  //BN归一层8参数
const float conv2d_6_kernel[10][14][3][3];  //卷积层7卷积核的权重
const float conv2d_6_bias[14];  //卷积层7卷积核的偏置
const float batch_normalization_8_params[4][14];  //BN归一层9参数
const float conv2d_7_kernel[14][16][1][1];  //卷积层8卷积核的权重
const float conv2d_7_bias[16];  //卷积层8卷积核的偏置
const float batch_normalization_9_params[4][16];  //BN归一层10参数
const float conv2d_8_kernel[16][10][1][1];  //卷积层9卷积核的权重
const float conv2d_8_bias[10];  //卷积层9卷积核的偏置
//=====================================================================
//文件名称：mobilenetv2.h
//功能概要：模型驱动构件头文件
//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)
//版    本：2022-07-14  V1.0
//适用芯片：D1
//构件生成时间：2026年07月09日 17:44:14
//=====================================================================

//=====================================================================
//函数名称:Model_PredictImage
//函数返回:无
//参数说明:result:传出参数，存储推理结果
//功能概要:模型推理函数
//=====================================================================
void Model_PredictImage(float *result);

#endif /* MODEL_H */ 
