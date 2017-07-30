# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2017 Vic Chan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from paddle.trainer.PyDataProvider2 import *
import numpy as np
import struct
import matplotlib.pyplot as plt


def read_image_files(filename, num):
    bin_file = open(filename, 'rb')
    buf = bin_file.read()
    index = 0
    magic, numImage, numRows, numCols = struct.unpack_from('>IIII', buf, index)
    index += struct.calcsize('>IIII')

    image_sets = []
    for i in range(num):
        images = struct.unpack_from('>784B', buf, index)
        index += struct.calcsize('>784B')
        images = np.array(images)
        images = images/255.0
        images = images.tolist()

        image_sets.append(images)
    bin_file.close()
    return image_sets


def read_label_files(filename):
    bin_file = open(filename, 'rb')
    buf = bin_file.read()
    index = 0
    magic, nums = struct.unpack_from('>II', buf, index)
    index += struct.calcsize('>II')
    labels = struct.unpack_from('>%sB' % nums, buf, index)
    bin_file.close()
    labels = np.array(labels)
    return labels

def fetch_traingset():
    path = '/Users/vic/Dev/DeepLearning/Paddle/DeepLearningWithPaddle/DNN-MNIST/'
    image_file = path + 'data/train-images-idx3-ubyte'
    label_file = path + 'data/train-labels-idx1-ubyte'
    images = read_image_files(image_file,60000)
    labels = read_label_files(label_file)
    return {'images': images,
            'labels': labels}


def fetch_testingset():
    path = '/Users/vic/Dev/DeepLearning/Paddle/DeepLearningWithPaddle/DNN-MNIST/'

    image_file = path + 'data/t10k-images-idx3-ubyte'
    label_file = path + 'data/t10k-labels-idx1-ubyte'
    images = read_image_files(image_file,10000)
    labels = read_label_files(label_file)
    return {'images': images,
            'labels': labels}





def test():

    data = fetch_testingset()
    image = data['images'][10]
    print("Label: %d" % data['labels'][10])
    images = np.reshape(image, [28, 28])
    plt.imshow(images, cmap='gray')
    plt.show()


