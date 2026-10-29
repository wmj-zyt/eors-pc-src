from keras import Model
from keras.layers import (Input, BatchNormalization, Add,Dense, ReLU, 
                                    DepthwiseConv2D, Reshape, Permute,Conv2D, 
                                    GlobalAveragePooling2D, concatenate, AveragePooling2D, MaxPooling2D)




custom_objects = {}

custom_attrs = {
    'epochs': 25,
    'batch_size': 32,
    'learning_rate': 0.001
}

def channel_shuffle(x, groups):
    _, width, height, channels = x.get_shape().as_list()
    group_ch = channels // groups
    x = Reshape([width, height, group_ch, groups])(x)
    x = Permute([1, 2, 4, 3])(x)
    x = Reshape([width, height, channels])(x)
    return x


def shuffle_unit(x, groups, channels, strides):
    y = x
    x = Conv2D(channels // 4, kernel_size=1, strides=(1, 1), padding='same', groups=groups)(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = channel_shuffle(x, groups)
    x = DepthwiseConv2D(kernel_size=(3, 3), strides=strides, padding='same')(x)
    x = BatchNormalization()(x)
    if strides == (2, 2):
        channels = channels - y.shape[-1]
    x = Conv2D(channels, kernel_size=1, strides=(1, 1), padding='same', groups=groups)(x)
    x = BatchNormalization()(x)

    if strides == (1, 1):
        x = Add()([x, y])
    if strides == (2, 2):
        y = AveragePooling2D((3, 3), strides=(2, 2), padding='same')(y)
        x = concatenate([x, y])
    x = ReLU()(x)
    return x


def ShuffleNetv1(input_shape, k, start_channels=200):
    groups = 2
    input = Input(input_shape)
    x = Conv2D(24, kernel_size=3, strides=(2, 2), padding='same')(input)
    x = BatchNormalization()(x)
    x = ReLU()(x)
    x = MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(x)
    repetitions = [3, 7, 3]
    for i, repetition in enumerate(repetitions):
        channels = start_channels * (2 ** i)
        x = shuffle_unit(x, groups, channels, strides=(2, 2))
        for i in range(repetition):
            x = shuffle_unit(x, groups, channels, strides=(1, 1))
    x = GlobalAveragePooling2D()(x)
    output = Dense(k, activation='softmax')(x)
    model = Model(input, output)
    return model
