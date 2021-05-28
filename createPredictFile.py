def get_predict_file_text(predict_dir, train_dirs, wide_setting):
    predict_text = ''
    import_text = 'import tensorflow as tf\n'
    import_text += 'import os\n'
    import_text += 'import numpy as np\n'
    import_text += 'import sys\n'
    import_text += 'import traceback\n'
    import_text += 'import shutil\n\n'
    predict_text += import_text
    predict_text += 'predict_dir = ['
    for i in range(len(train_dirs)):
        predict_text += "'" + predict_dir + '/' + train_dirs[i] + "'"
        if i != len(train_dirs) - 1:
            predict_text += ','
    predict_text += ']\n'

    function_text = ''
    function_text += 'def predict_resize_decode(filename):\n'
    function_text += '    image_string = tf.io.read_file(filename)\n'
    function_text += '    image_decoded = tf.image.decode_jpeg(image_string)\n'
    function_text += '    image_resized = tf.image.resize(image_decoded, [' + str(wide_setting[0]['width']) + ', ' + str(wide_setting[0]['height']) + ']) / 255.0\n'
    function_text += '    image_resized = np.expand_dims(image_resized, axis=0)\n'
    function_text += '    return image_resized\n'
    predict_text += function_text

    predict_text += 'def predict(predict_path, model_name):\n'
    predict_text += '    files = os.listdir(predict_path)\n'
    predict_text += '    model = tf.saved_model.load("saved/" + model_name)\n'
    predict_text += '    for f in files:\n'
    predict_text += '        fullpath = os.path.join(predict_path, f)\n'
    predict_text += '        if os.path.isfile(fullpath):\n'
    predict_text += '            image = predict_resize_decode(fullpath)\n'
    predict_text += '            result = model(image)\n'
    predict_text += '            n, index = 0, 0\n'
    predict_text += '            for i in range(len(result[0])):\n'
    predict_text += '                if result[0][i] > n:\n'
    predict_text += '                    n = result[0][i]\n'
    predict_text += '                    index = i\n'
    predict_text += '            shutil.move(fullpath, predict_dir[index] + \'/\' + f)\n'

    main_text = ''
    main_text += 'if __name__ == \'__main__\':\n'
    main_text += '    path = \'' + predict_dir + '\'\n'
    main_text += '    modelName = \'' + wide_setting[0]['modelName'] + '\'\n'
    main_text += '    for folder in predict_dir:\n'
    main_text += '        os.mkdir(folder)\n'
    main_text += '    f = open(\'result.txt\', \'w\')\n'
    main_text += '    try:\n'
    main_text += '        predict(path, modelName)\n'
    main_text += '        f.write(\'success\\n\')\n'
    main_text += '    except Exception as e:\n'
    main_text += '        traceback.print_exc()\n'
    main_text += '        error_class = e.__class__.__name__\n'
    main_text += '        detail = str(e)\n'
    main_text += '        cl, exc, tb = sys.exc_info()\n'
    main_text += '        lastCallStack = traceback.extract_tb(tb)[-1]\n'
    main_text += '        fileName = lastCallStack[0]\n'
    main_text += '        lineNum = lastCallStack[1]\n'
    main_text += '        funcName = lastCallStack[2]\n'
    main_text += '        errMsg = "File \\"{}\\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)\n'
    main_text += '        f.write(\'error\\n\')\n'
    main_text += '        f.write(errMsg)\n'
    main_text += '    finally:\n'
    main_text += '        f.close()\n'
    main_text += ''
    predict_text += main_text



    return predict_text

def save_text_to_python_file(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()


if __name__ == '__main__':
    text = get_predict_file_text('D:/Users/Wu/PycharmProjects/TensorflowGUI/predictData', ['mask_face', 'no_mask_face'])
    print(text)
    save_text_to_python_file(text, 'test.py')