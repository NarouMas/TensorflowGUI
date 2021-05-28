import tensorflow as tf
import os
import numpy as np
import sys
import traceback
import shutil

predict_dir = ['D:/Users/Wu/PycharmProjects/TensorflowGUI/predictData/mask_face','D:/Users/Wu/PycharmProjects/TensorflowGUI/predictData/no_mask_face']
def predict_resize_decode(filename):
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string)
    image_resized = tf.image.resize(image_decoded, [64, 64]) / 255.0
    image_resized = np.expand_dims(image_resized, axis=0)
    return image_resized
def predict(predict_path, model_name):
    files = os.listdir(predict_path)
    model = tf.saved_model.load("saved/" + model_name)
    for f in files:
        fullpath = os.path.join(predict_path, f)
        if os.path.isfile(fullpath):
            image = predict_resize_decode(fullpath)
            result = model(image)
            n, index = 0, 0
            for i in range(len(result[0])):
                if result[0][i] > n:
                    n = result[0][i]
                    index = i
            shutil.move(fullpath, predict_dir[index] + '/' + f)
if __name__ == '__main__':
    path = 'D:/Users/Wu/PycharmProjects/TensorflowGUI/predictData'
    modelName = 'myModel'
    for folder in predict_dir:
        os.mkdir(folder)
    f = open('result.txt', 'w')
    try:
        predict(path, modelName)
        f.write('success\n')
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
