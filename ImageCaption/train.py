# -*- coding: utf-8 -*-

import gzip
import copy
import numpy as np
from PIL import Image
import paddle.v2 as paddle
from model import train_caption_net
from data_reader import create_reader

DATA_DIM = 224*224*3
DICT_DIM = 4529
image = paddle.layer.data(name="image", type=paddle.data_type.dense_vector(DATA_DIM))
target = paddle.layer.data(name="target", type=paddle.data_type.integer_value_sequence(DICT_DIM))
label = paddle.layer.data(name="label", type=paddle.data_type.integer_value_sequence(DICT_DIM))

paddle.init(use_gpu=False, trainer_count=1)


def train(epoches):

    train_reader = create_reader(True)
    test_reader = create_reader(False)
    train_batch = paddle.batch(reader=paddle.reader.shuffle(train_reader, buf_size=8), batch_size=4)
    test_batch = paddle.batch(reader=paddle.reader.shuffle(test_reader, buf_size=8), batch_size=4)

    feeding = {'image': 0, 'target': 1, 'label': 2}

    cost = train_caption_net(dict_dim=DICT_DIM, target=target, label=label, input_images=image)
    adam_optimizer = paddle.optimizer.Adam(
        learning_rate=1e-4,
        regularization=paddle.optimizer.L2Regularization(rate=8e-4),
        model_average=paddle.optimizer.ModelAverage(average_window=0.5)
    )

    parameters = paddle.parameters.create(cost)
    parameters.init_from_tar(gzip.open('params/Paddle_ResNet50.tar.gz'))

    def event_handler(event):
        if isinstance(event, paddle.event.EndIteration):
            if event.batch_id % 2 == 0:
                print "Pass %d, Batch %d, Cost %f, %s" % (
                    event.pass_id, event.batch_id, event.cost, event.metrics)
        if isinstance(event, paddle.event.EndPass):
            with gzip.open('params_pass_%d.tar.gz' % event.pass_id, 'w') as f:
                parameters.to_tar(f)
            result = trainer.test(reader=test_batch)
            print "Test with Pass %d, %s" % (event.pass_id, result.metrics)

    trainer = paddle.trainer.SGD(
        cost=cost,
        parameters=parameters,
        update_equation=adam_optimizer
    )

    trainer.train(
        reader=train_batch,
        event_handler=event_handler,
        feeding=feeding,
        num_passes=epoches
    )


if __name__ == '__main__':

    train(10)









