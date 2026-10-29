from keras.layers import (Input, Conv2D, BatchNormalization, GlobalAveragePooling2D, Dropout, Activation, Add, 
    Reshape, DepthwiseConv2D)
from keras import backend as K
from keras import Model


custom_objects = {}

custom_attrs = {
    'epochs': 40,
    'batch_size': 32,
    'learning_rate': 0.001
}

"""
函数名称：_conv_block
参数说明：inputs：输入 filters：输出维度 kernel：卷积核大小 strides：卷积核滑动步长
函数返回：输入数据经过卷积层、批标准化层和ReLU6激活函数处理后的张量
功能概要：通过卷积、批标准化和ReLU6激活层对输入数据进行特征提取和标准化处理
"""
def _conv_block(inputs, filters, kernel, strides):
    # 判断图像数据格式，返回对应的通道轴索引
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    # 使用Conv2D卷积层对输入数据进行卷积操作
    x = Conv2D(filters, kernel, padding='same', strides=strides)(inputs)
    # 使用BatchNormalization进行批标准化，规范化数据分布，加快收敛速度
    x = BatchNormalization(axis=channel_axis)(x)
    # 使用ReLU6激活函数，增加非线性
    return Activation('relu6')(x)


"""
函数名称：_bottleneck
参数说明：inputs:输入 filters:输出维度  kernel:卷积核  t:扩展因子  s:步长   r:是否使用残差  alpha:宽度系数
函数返回：输入数据经过瓶颈结构块处理后的张量
功能概要：实现瓶颈层的卷积块
"""
def _bottleneck(inputs, filters, kernel, t, alpha, s, r=False):
    # 判断图像数据格式，返回对应的通道轴索引
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    # 计算扩展后的通道数
    tchannel = inputs.shape[channel_axis] * t
    # 计算压缩后的通道数
    cchannel = int(filters * alpha)
    # 1x1卷积，用于扩展通道数
    x = _conv_block(inputs, tchannel, (1, 1), (1, 1))
    # 深度可分离卷积，用于提取空间特征
    x = DepthwiseConv2D(kernel, strides=(s, s), depth_multiplier=1, padding='same')(x)
    # 批标准化，规范化数据分布
    x = BatchNormalization(axis=channel_axis)(x)
    # ReLU6激活函数，增加非线性
    x = Activation('relu6')(x)
    # 1x1卷积，用于压缩通道数
    x = Conv2D(cchannel, kernel_size=(1, 1), strides=(1, 1), padding='same')(x)
    # 批标准化，规范化数据分布
    x = BatchNormalization(axis=channel_axis)(x)
    # 如果r为真，则进行残差连接
    if r:
        x = Add()([x, inputs])
    return x


"""
函数名称：_inverted_residual_block
参数说明：inputs:输入大小 filters:输出维度 kernel:卷积核大小 t:扩展因子 alpha:分辨率乘子,用于控制图像大小 strides:步长 n:层的重复次数
函数返回：输入数据经过倒残差块结构处理的张量
功能概要：实现倒残差块
"""
def _inverted_residual_block(inputs, filters, kernel, t, alpha, strides, n):
    # 调用瓶颈块
    x = _bottleneck(inputs, filters, kernel, t, alpha, strides)
    # 添加 n-1 个带有残差连接的瓶颈层
    for i in range(1, n):
        x = _bottleneck(x, filters, kernel, t, alpha, 1, True)
    return x


"""
函数名称：MobileNetv2
参数说明：input_shape:输入尺寸 k:物体种类数 alpha:宽度因子，最好为[0.35,0.5,0.75,1.0,1.3,1.4]
函数返回：MobileNetV2模型
功能概要：定义MobileNetV2模型结构
"""
def MobileNetv2(input_shape, k, alpha=1):
    # 定义输入层，形状为input_shape
    inputs = Input(shape=input_shape)
    # 第一个卷积块，输出通道数为6，卷积核大小为3x3，步幅为2x2
    x = _conv_block(inputs, 6, (3, 3), strides=(2, 2))
    # 倒残差块，输出通道数为8，卷积核大小为3x3，扩展因子t为3，步幅为2，包含2个瓶颈层
    x = _inverted_residual_block(x, 8, (3, 3), t=3, alpha=alpha, strides=2, n=2)
    # 第二个卷积块，输出通道数为10，卷积核大小为3x3，步幅为2x2
    x = _conv_block(x, 10, (3, 3), strides=(2, 2))
    # 第三个卷积块，输出通道数为14，卷积核大小为3x3，步幅为1x1
    x = _conv_block(x, 14, (3, 3), strides=(1, 1))
    # 第四个卷积块，输出通道数为16，卷积核大小为1x1，步幅为1x1
    x = _conv_block(x, 16, (1, 1), strides=(1, 1))
    # 全局平均池化层，将每个特征图转换为一个数值
    x = GlobalAveragePooling2D()(x)
    # 重塑张量形状为(1, 1, 16)
    x = Reshape((1, 1, 16))(x)
    # Dropout层，丢弃率为0.5，防止过拟合
    x = Dropout(0.4, name='Dropout')(x)
    # 卷积层，输出通道数为k，卷积核大小为1x1
    x = Conv2D(k, (1, 1), padding='same')(x)
    # Softmax激活函数，将输出转换为概率分布
    x = Activation('softmax')(x)
    # 重塑张量形状为(k,)
    output = Reshape((k,))(x)
    # 定义模型，输入为inputs，输出为output
    model = Model(inputs, output)
    # 返回模型
    return model


if __name__ == "__main__":
    pass