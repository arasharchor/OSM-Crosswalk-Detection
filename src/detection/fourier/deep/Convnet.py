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
    model.add(Dense(64))
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

def predict(x):
    xe = np.array([x])
    prediction = network.predict(xe)
    prediction = prediction[0]
    isCrosswalk = prediction[0] == 1 and prediction[1] < 1e-200
    if(isCrosswalk): print("Zerba " + str(prediction))
    #else: print(prediction)
    return isCrosswalk

theano.config.openmp = True
network_path = "/home/osboxes/Documents/OSM-Crosswalk-Detection/src/detection/fourier/deep/keras_saver_weights.10-0.07.hdf5"
network = load_network(network_path, True)
#network = load_big_convnet(network_path, True)

	