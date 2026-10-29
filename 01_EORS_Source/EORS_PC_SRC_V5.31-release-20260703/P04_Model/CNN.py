from keras.layers import (Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout)
from keras.models import Model

custom_objects = {}
custom_attrs = {
    'epochs': 15,
    'batch_size': 32,
    'learning_rate': 0.001
}

def CNN(input_shape, k):
    input = Input(shape=input_shape)
    x = Conv2D(32, (3, 3), activation='relu')(input)
    x = MaxPooling2D(3, 3)(x)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D(3, 3)(x)
    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = MaxPooling2D(3, 3)(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)

    x = Dense(64, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    output = Dense(k, activation='softmax')(x)
    model = Model(input, output)
    return model

