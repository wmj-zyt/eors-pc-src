from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Reshape, RNN, Activation
from keras.models import Model
from .kerasncp import *

custom_objects = {
                    "LTCCell": LTCCell,
                }

custom_attrs = {
    'epochs': 15,
    'batch_size': 32,
    'learning_rate': 0.001
}
"""
函数名称：NCP
参数说明：input_shape:输入尺寸 k:物体种类数
函数返回：NCP模型
功能概要：定义NCP模型结构
"""
# def NCP(input_shape, k):
#     ncp_wiring = kncp(
#         inter_neurons=9,  # 中间神经元个数
#         command_neurons=6,  # 命令神经元个数
#         motor_neurons=k,  # 运动神经元个数
#         sensory_fanout=5,  # 每个感觉神经元有多少个外突触
#         inter_fanout=5,  # 每个中间神经元有多少个向外突触
#         recurrent_command_synapses=3,  # 现在在命令神经元层有多少循环突触
#         motor_fanin=3,  # 每个运动神经元有多少传入突触
#     )
#     ncp_cell = LTCCell(ncp_wiring)
#     model = Sequential()
#     model.add(Conv2D(6, (5, 5), activation="relu", input_shape=input_shape))
#     model.add(MaxPooling2D())
#     model.add(Conv2D(6, (5, 5), activation="relu"))
#     model.add(MaxPooling2D())
#     model.add(Flatten())
#     model.add(BatchNormalization())
#     model.add(Dense(2 * k, activation="relu"))
#     model.add(Reshape((-1, 2 * k)))
#     model.add(RNN(ncp_cell, return_sequences=True))
#     model.add(Activation("softmax"))
#     return model


def NCP(input_shape, k):
    ncp_wiring = kncp(
        inter_neurons=9,  # 中间神经元个数
        command_neurons=6,  # 命令神经元个数
        motor_neurons=k,  # 运动神经元个数
        sensory_fanout=5,  # 每个感觉神经元有多少个外突触
        inter_fanout=5,  # 每个中间神经元有多少个向外突触
        recurrent_command_synapses=3,  # 现在在命令神经元层有多少循环突触
        motor_fanin=3,  # 每个运动神经元有多少传入突触
    )
    ncp_cell = LTCCell(ncp_wiring)
    input = Input(shape=input_shape)
    x = Conv2D(filters=6, kernel_size=(5,5), activation="relu")(input)
    x = MaxPooling2D()(x)
    x = Conv2D(6, (5, 5), activation="relu")(x)
    x = MaxPooling2D()(x)
    x = Flatten()(x)
    x = BatchNormalization()(x)
    x = Dense(2 * k, activation="relu")(x)
    x = Reshape((-1, 2 * k))(x)
    x = RNN(ncp_cell, return_sequences=True)(x)
    output = Activation("softmax")(x)
    model = Model(input, output)
    return model
# def NCP(input_shape, k):
    # ncp_wiring = kncp(
    #     inter_neurons=9,  # 中间神经元个数
    #     command_neurons=6,  # 命令神经元个数
    #     motor_neurons=k,  # 运动神经元个数
    #     sensory_fanout=5,  # 每个感觉神经元有多少个外突触
    #     inter_fanout=5,  # 每个中间神经元有多少个向外突触
    #     recurrent_command_synapses=3,  # 现在在命令神经元层有多少循环突触
    #     motor_fanin=3,  # 每个运动神经元有多少传入突触
    # )
    # ncp_cell = LTCCell(ncp_wiring)
    # input = Input(shape=input_shape)
    # x = Conv2D(filters=6, kernel_size=(5,5))(input)
    # x = Activation('relu')(x)
    # x = MaxPooling2D()(x)
    # x = Conv2D(filters=6, kernel_size=(5,5))(x)
    # x = Activation('relu')(x)
    # x = MaxPooling2D()(x)
    # x = Flatten()(x)
    # x = BatchNormalization()(x)
    # x = Dense(2 * k)(x)
    # x = Activation('relu')(x)
    # x = Reshape((-1, 2 * k))(x)
    # x = RNN(ncp_cell, return_sequences=True)(x)
    # output = Activation('softmax')(x)
    # model = Model(input, output)
    # return model