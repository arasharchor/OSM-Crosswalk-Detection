from __future__ import absolute_import
from __future__ import print_function
import numpy as np
from PIL import Image
from random import randint


from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.regularizers import l2
import theano



def load_network(hd5f_path, verbose):

    batch_size = 128
    nb_classes = 2
    nb_epoch = 12

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 4#3
    #image is rgb
    img_channels = 3


    if(verbose):
        print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    if(verbose):
        print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    if(verbose):
        print("load weights")
    model.load_weights(hd5f_path)
    if(verbose):
        print("network loaded")

    return model

def load_64f4c(hd5f_path, verbose):

    batch_size = 128
    nb_classes = 2
    nb_epoch = 12

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 64
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 4#3
    #image is rgb
    img_channels = 3


    if(verbose):
        print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    if(verbose):
        print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    if(verbose):
        print("load weights")
    model.load_weights(hd5f_path)
    if(verbose):
        print("network loaded")

    return model

def load_big_convnet(hd5f_path, verbose):
    nb_classes = 2

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3
    #image is rgb
    img_channels = 3

    if(verbose):
        print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv, border_mode='valid'))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    if(verbose):
        print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    if(verbose):
        print("load weights")
    model.load_weights(hd5f_path)
    if(verbose):
        print("network loaded")
    return model

def load_big_convnet2(hd5f_path):
    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3
    #image is rgb
    img_channels = 3
    print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv, border_mode='valid'))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv, border_mode='valid'))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(2))
    model.add(Activation('softmax'))

    print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    model.load_weights(hd5f_path)
    return model

def load_big_convnet8(hd5f_path):
     # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 48
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 4
    #image is rgb
    img_channels = 3

    print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(nb_filters*2, nb_conv -1, nb_conv -1))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters*2, nb_conv -1, nb_conv -1))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('softmax'))

    print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    model.load_weights(hd5f_path)
    return model

def load_big_convnet9(hd5f_path):
     # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters = 64
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 4
    #image is rgb
    img_channels = 3

    model = Sequential()

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.5))

    nb_conv = 3
    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters*2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('softmax'))

    print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    model.load_weights(hd5f_path)
    return model
def convnet26(network_path):
    batch_size = 128
    nb_classes = 2
    nb_epoch = 70

    # input image dimensions
    img_rows, img_cols = 50, 50
    # number of convolutional filters to use
    nb_filters1 = 64
    nb_filters2 = 128
    nb_filters3 = 256
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3
    #image is rgb
    img_channels = 3

    print("put convnet together")
    model = Sequential()

    model.add(Convolution2D(nb_filters1, nb_conv, nb_conv, border_mode='full', input_shape=(img_channels, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters1, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Convolution2D(nb_filters2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters2, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Convolution2D(nb_filters3, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters3, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Flatten())

    model.add(Dropout(0.5))
    model.add(Dense(4096, W_regularizer=l2(0.01)))
    model.add(Activation('relu'))

    model.add(Dropout(0.5))
    model.add(Dense(4096, W_regularizer=l2(0.01)))
    model.add(Activation('relu'))

    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, W_regularizer=l2(0.01)))
    model.add(Activation('softmax'))

    print("start compiling")
    model.compile(loss='categorical_crossentropy', optimizer='adadelta')
    model.load_weights(network_path)
    return model
def predict_list(x):
    predictions = network.predict(x)
    results = []
    for predict in predictions:
        isCrosswalk = predict[0] > 0.999 and predict[1] < 1e-300
        if(isCrosswalk): print("Zerba " + str(predict))
        else: print(str(predict))
        results.append(isCrosswalk)

    return results

network = None

def initialize():
    global network
    theano.config.openmp = True
    #Best Net 64f4:
    network_path = "/home/osboxes/Documents/OSM-Crosswalk-Detection/src/detection/fourier/deep/klein64-4f.e11-l0.045.hdf5"
    network = load_64f4c(network_path, True)
    #Schwellwert: 1e-150, isCrosswalk = predict[0] > 0.9 and predict[1] < 1e-150
