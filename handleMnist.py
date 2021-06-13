import tensorflow as tf
import cv2

def main():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    for i in range(10000):
        cv2.imwrite('./trainData/number/' + str(y_train[i]) + '/' + str(i) + '.jpg', x_train[i])
    for i in range(1000):
        cv2.imwrite('./predictData/number/' + str(i) + '.jpg', x_test[i])

if __name__ == '__main__':
    main()
