def get_model_file_text(layer_argument, train_dirs, wide_setting):
    model_file_text = ''
    import_text = 'import tensorflow as tf\nimport os\nimport numpy as np\n'
    import_text += 'import sys\n'
    import_text += 'import traceback\n'
    import_text += 'import matplotlib.pyplot as plt\n'
    model_file_text += import_text

    model_file_text += 'num_epochs = ' + str(wide_setting[0]['num_epochs']) + '\n'
    model_file_text += 'batch_size = ' + str(wide_setting[0]['batch_size']) + '\n'
    model_file_text += 'learning_rate = ' + str(wide_setting[0]['learning_rate']) + '\n'

    # generate train dir variable
    for i in range(len(train_dirs)):
        model_file_text += 'train_' + str(i) + '_dir = ' + '\'' + train_dirs[i] + '/\'\n'
    model_text = 'class MyModel():\n'
    model_text += '    def getModel(self):\n'
    model_text += '        model = tf.keras.Sequential([\n'
    # generate layer code
    for i in range(0, len(layer_argument)):
        argument = layer_argument[i][0]
        layer_text = ''
        layer_text += '            tf.keras.layers.' + argument['type'] + '('
        if argument['type'] == 'Conv2D':
            layer_text += str(argument['filters']) + ', ' + str(argument['kernel_size']) + ', activation=\'' + argument['activation'] + '\', padding=\'' + argument['padding'] + '\''
        elif argument['type'] == 'Flatten':
            layer_text += ''
        elif argument['type'] == 'MaxPool2D':
            layer_text += str(argument['pool_size']) + ', strides=' + str(argument['strides']) + ', padding=\'' + argument['padding'] + '\''
        elif argument['type'] == 'Dense':
            layer_text += str(argument['units']) + ', activation=\'' + argument['activation'] + '\', use_bias=' + str(argument['use_bias']) + ''
        elif argument['type'] == 'Dropout':
            layer_text += str(argument['rate'])
        if i == 0:
            layer_text += ', input_shape=(' + str(wide_setting[0]['width']) + ', ' + str(wide_setting[0]['height']) + ', ' + str(wide_setting[0]['channel']) + ')'
        layer_text += ')'

        if i != len(layer_argument) - 1:
            layer_text += ','
        layer_text += '\n'
        model_text += layer_text

    model_text += '        ])\n'
    model_text += '        model.compile(\n'
    model_text += '            optimizer=tf.keras.optimizers.Adam(learning_rate=' + str(wide_setting[0]['learning_rate']) + '),\n'
    model_text += '            loss=tf.keras.losses.sparse_categorical_crossentropy,\n'
    model_text += '            metrics=[tf.keras.metrics.sparse_categorical_accuracy]\n'
    model_text += '        )\n'
    model_text += '        return model\n\n\n'
    model_file_text += model_text

    function_text = ''
    function_text += 'def _decode_and_resize(filename, label):\n'
    function_text += '    image_string = tf.io.read_file(filename)\n'
    function_text += '    image_decoded = tf.image.decode_jpeg(image_string)\n'
    function_text += '    image_resized = tf.image.resize(image_decoded, [' + str(wide_setting[0]['width']) + ', ' + str(wide_setting[0]['height']) + ']) / 255.0\n'
    function_text += '    return image_resized, label\n\n\n'
    function_text += 'def predict_resize_decode(filename):\n'
    function_text += '    image_string = tf.io.read_file(filename)\n'
    function_text += '    image_decoded = tf.image.decode_jpeg(image_string)\n'
    function_text += '    image_resized = tf.image.resize(image_decoded, [' + str(wide_setting[0]['width']) + ', ' + str(wide_setting[0]['height']) + ']) / 255.0\n'
    function_text += '    image_resized = np.expand_dims(image_resized, axis=0)\n'
    function_text += '    return image_resized\n\n\n'
    function_text += 'def train():\n'
    for i in range(len(train_dirs)):
        function_text += '    train_' + str(i) + '_filenames = tf.constant([train_' + str(i) + '_dir + filename for filename in os.listdir(train_' + str(i) + '_dir)])\n'
    function_text += '    train_filenames = tf.concat(['
    for i in range(len(train_dirs)):
        function_text += 'train_' + str(i) + '_filenames'
        if i != len(train_dirs) - 1:
            function_text += ', '
    function_text += '], axis=-1)\n\n'
    function_text += '    train_labels = tf.concat([\n'
    for i in range(len(train_dirs)):
        if i != len(train_dirs) - 1:
            function_text += '        tf.constant([' + str(i) + '] * train_' + str(i) + '_filenames.shape[0]),\n'
        else:
            function_text += '        tf.constant([' + str(i) + '] * train_' + str(i) + '_filenames.shape[0])], axis=-1)\n'
    function_text += '    train_dataset = tf.data.Dataset.from_tensor_slices((train_filenames, train_labels))\n'
    function_text += '    train_dataset = train_dataset.map(\n'
    function_text += '        map_func=_decode_and_resize,\n'
    function_text += '        num_parallel_calls=tf.data.experimental.AUTOTUNE\n'
    function_text += '    )\n'
    function_text += '    train_dataset = train_dataset.shuffle(buffer_size=300)\n'
    function_text += '    train_dataset = train_dataset.batch(batch_size)\n'
    function_text += '    train_dataset = train_dataset.prefetch(tf.data.experimental.AUTOTUNE)\n'
    function_text += '    model = MyModel().getModel()\n'
    function_text += '    model.compile(\n'
    function_text += '        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),\n'
    function_text += '        loss=tf.keras.losses.sparse_categorical_crossentropy,\n'
    function_text += '        metrics=[tf.keras.metrics.sparse_categorical_accuracy]\n'
    function_text += '    )\n'
    function_text += '    history = model.fit(train_dataset, epochs=num_epochs)\n'
    function_text += '    tf.saved_model.save(model, "saved/' + wide_setting[0]['modelName'] + '")\n\n'
    function_text += '    plt.title(\'train_loss\')\n'
    function_text += '    plt.ylabel(\'loss\')\n'
    function_text += '    plt.xlabel(\'Epoch\')\n'
    function_text += '    plt.plot(history.history[\'loss\'])\n'
    function_text += '    plt.savefig(\'' + wide_setting[0]['modelName'] + '_loss.jpg\')\n\n'
    function_text += '    plt.clf()\n\n'
    function_text += '    plt.title(\'train_accuracy\')\n'
    function_text += '    plt.ylabel(\'accuracy\')\n'
    function_text += '    plt.xlabel(\'Epoch\')\n'
    function_text += '    plt.plot(history.history[\'sparse_categorical_accuracy\'])\n'
    function_text += '    plt.savefig(\'' + wide_setting[0]['modelName'] + '_accuracy.jpg\')\n\n'
    function_text += '    return model, history\n'
    model_file_text += function_text

    main_text = ''
    main_text += 'if __name__ == \'__main__\':\n'
    main_text += '    f = open(\'result.txt\', \'w\')\n'
    main_text += '    try:\n'
    main_text += '        model, history = train()\n'
    main_text += '        f.write(\'success\\n\')\n'
    main_text += '        f.write(\'loss:\' + str(history.history[\'loss\']) + \'\\n\')\n'
    main_text += '        f.write(\'sparse_categorical_accuracy:\' + str(history.history[\'sparse_categorical_accuracy\']) + \'\\n\')\n'
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


    model_file_text += main_text


    return model_file_text


def save_text_to_python_file(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()


if __name__ == '__main__':
    text = get_model_file_text()
    print(text)
    save_text_to_python_file(text, 'test.py')
