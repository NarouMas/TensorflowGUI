import tensorflow as tf
import os
import numpy as np
import sys
import traceback
import matplotlib.pyplot as plt
num_epochs = 10
batch_size = 32
learning_rate = 0.001
train_0_dir = 'D:/Users/Wu/PycharmProjects/TensorflowGUI/trainData/mask_face/'
train_1_dir = 'D:/Users/Wu/PycharmProjects/TensorflowGUI/trainData/no_mask_face/'
class MyModel():
    def getModel(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, 3, activation='relu', padding='valid', input_shape=(64, 64, 3)),
            tf.keras.layers.MaxPool2D(2, strides=3, padding='valid'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation='relu', use_bias=True),
            tf.keras.layers.Dense(2, activation='softmax', use_bias=True)
        ])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss=tf.keras.losses.sparse_categorical_crossentropy,
            metrics=[tf.keras.metrics.sparse_categorical_accuracy]
        )
        return model


def _decode_and_resize(filename, label):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string)
    image_resized = tf.image.resize(image_decoded, [64, 64]) / 255.0
    return image_resized, label


def predict_resize_decode(filename):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string)
    image_resized = tf.image.resize(image_decoded, [64, 64]) / 255.0
    image_resized = np.expand_dims(image_resized, axis=0)
    return image_resized


def train():
    train_0_filenames = tf.constant([train_0_dir + filename for filename in os.listdir(train_0_dir)])
    train_1_filenames = tf.constant([train_1_dir + filename for filename in os.listdir(train_1_dir)])
    train_filenames = tf.concat([train_0_filenames, train_1_filenames], axis=-1)

    train_labels = tf.concat([
        tf.constant([0] * train_0_filenames.shape[0]),
        tf.constant([1] * train_1_filenames.shape[0])], axis=-1)
    train_dataset = tf.data.Dataset.from_tensor_slices((train_filenames, train_labels))
    train_dataset = train_dataset.map(
        map_func=_decode_and_resize,
        num_parallel_calls=tf.data.experimental.AUTOTUNE
    )
    train_dataset = train_dataset.shuffle(buffer_size=300)
    train_dataset = train_dataset.batch(batch_size)
    train_dataset = train_dataset.prefetch(tf.data.experimental.AUTOTUNE)
    model = MyModel().getModel()
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.sparse_categorical_crossentropy,
        metrics=[tf.keras.metrics.sparse_categorical_accuracy]
    )
    history = model.fit(train_dataset, epochs=num_epochs)
    tf.saved_model.save(model, "saved/myModel")

    plt.title('train_loss')
    plt.ylabel('loss')
    plt.xlabel('Epoch')
    plt.plot(history.history['loss'])
    plt.savefig('myModel_loss.jpg')

    plt.clf()

    plt.title('train_accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('Epoch')
    plt.plot(history.history['sparse_categorical_accuracy'])
    plt.savefig('myModel_accuracy.jpg')

    return model, history
if __name__ == '__main__':
    f = open('result.txt', 'w')
    try:
        model, history = train()
        f.write('success\n')
        f.write('loss:' + str(history.history['loss']) + '\n')
        f.write('sparse_categorical_accuracy:' + str(history.history['sparse_categorical_accuracy']) + '\n')
    except Exception as e:
        traceback.print_exc()
        error_class = e.__class__.__name__
        detail = str(e)
        cl, exc, tb = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineNum = lastCallStack[1]
        funcName = lastCallStack[2]
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        f.write('error\n')
        f.write(errMsg)
    finally:
        f.close()
