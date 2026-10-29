# -*- coding: utf-8 -*-
"""
函数名称：EfficientNetLite0
参数说明：input_shape:输入尺寸 k:物体种类数 width:宽度系数 depth:深度系数
函数返回：EfficientNet-Lite0 模型
功能概要：官方 EfficientNet-Lite0 骨干（无SE、ReLU6、深度可分离卷积）
         分类头按 EORS 惯例：GAP -> 1×1 Conv -> softmax
         算子全部落在构件生成器白名单内（无 Dense/MaxPool/Concat）
"""
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


def _conv_block(inputs, filters, kernel, strides):
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    x = Conv2D(filters, kernel, padding='same', strides=strides)(inputs)
    x = BatchNormalization(axis=channel_axis)(x)
    return Activation('relu6')(x)


def _mbconv(inputs, filters, kernel, strides, expand_ratio):
    """倒残差块：可选 1x1 扩张 -> 深度卷积 -> 1x1 投影(无激活)；stride=1且通道一致时接残差"""
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    in_filters = inputs.shape[channel_axis]
    hidden = in_filters * expand_ratio
    x = inputs
    if expand_ratio != 1:
        x = _conv_block(inputs, hidden, (1, 1), (1, 1))
    x = DepthwiseConv2D(kernel, strides=(strides, strides), depth_multiplier=1, padding='same')(x)
    x = BatchNormalization(axis=channel_axis)(x)
    x = Activation('relu6')(x)
    x = Conv2D(filters, (1, 1), strides=(1, 1), padding='same')(x)
    x = BatchNormalization(axis=channel_axis)(x)
    if strides == 1 and in_filters == filters:
        x = Add()([x, inputs])
    return x


def EfficientNetLite0(input_shape, k, width=1.0, depth=1.0):
    def wf(ch):
        return int(ch * width)

    inputs = Input(shape=input_shape)
    # stem：3x3 步长2 卷积
    x = _conv_block(inputs, wf(32), (3, 3), (2, 2))
    # 官方 stage 表：(重复次数, 卷积核, 首块步长, 扩张比, 输出通道)
    stages = [
        (1, 3, 1, 1, 16),
        (2, 3, 2, 6, 24),
        (2, 5, 2, 6, 40),
        (3, 3, 2, 6, 80),
        (3, 5, 1, 6, 112),
        (4, 5, 2, 6, 192),
        (1, 3, 1, 6, 320),
    ]
    for repeats, kernel, stride, exp, out_ch in stages:
        n = max(1, round(repeats * depth))
        for i in range(n):
            s = stride if i == 0 else 1
            x = _mbconv(x, wf(out_ch), (kernel, kernel), s, exp)
    # head：1x1 卷积扩到 1280
    x = _conv_block(x, wf(1280), (1, 1), (1, 1))
    # 分类头（同 MobileNetv2.py 写法）
    x = GlobalAveragePooling2D()(x)
    x = Reshape((1, 1, wf(1280)))(x)
    x = Dropout(0.4, name='Dropout')(x)
    x = Conv2D(k, (1, 1), padding='same')(x)
    x = Activation('softmax')(x)
    output = Reshape((k,))(x)
    return Model(inputs, output)


if __name__ == "__main__":
    pass
