def get_model_file_text(layer_argument, train_dirs, test_dirs):
    model_file_text = ''
    import_text = 'import tensorflow as tf\nimport os\nimport numpy as np\nimport cv2\n'
    model_file_text += import_text

    model_file_text += 'num_epochs = 20\n'
    model_file_text += 'batch_size = 32\n'
    model_file_text += 'learning_rate = 0.001\n'

    # generate train dir variable
    for i in range(len(train_dirs)):
        model_file_text += 'train_' + str(i) + '_dir = ' + '\'' + train_dirs[i] + '\'/\n'
    model_text = 'class MyModel():\n'
    model_text += '    def getModel(self):\n'
    model_text += '        model = tf.keras.Sequential([\n'
    # generate layer code
    for i in range(0, len(layer_argument)):
        argument = layer_argument[i][0]
        layer_text = ''
        layer_text += '            tf.keras.layers.' + argument['type'] + '('
        if argument['type'] == 'Conv2D':
            layer_text += str(argument['filters']) + ', ' + str(argument['kernel_size']) + ', activation=\'' + argument['activation'] + '\', padding=\'' + argument['padding'] + '\')'
        elif argument['type'] == 'Flatten':
            layer_text += ')'
        elif argument['type'] == 'MaxPool2D':
            layer_text += str(argument['pool_size']) + ', strides=' + str(argument['strides']) + ', padding=\'' + argument['padding'] + '\')'
        elif argument['type'] == 'Dense':
            layer_text += str(argument['units']) + ', activation=\'' + argument['activation'] + '\', use_bias=' + str(argument['use_bias']) + ')'

        if i != len(layer_argument) - 1:
            layer_text += ','
        layer_text += '\n'
        model_text += layer_text

    model_text += '        ])\n'
    model_text += '        model.compile(\n'
    model_text += '            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),\n'
    model_text += '            loss=tf.keras.losses.sparse_categorical_crossentropy,\n'
    model_text += '            metrics=[tf.keras.metrics.sparse_categorical_accuracy]\n'
    model_text += '        )\n'
    model_text += '        return model\n\n\n'
    model_file_text += model_text

    function_text = ''
    function_text += 'def _decode_and_resize(filename, label):\n'
    function_text += '    image_string = tf.io.read_file(filename)\n'
    function_text += '    image_decoded = tf.image.decode_jpeg(image_string)\n'
    function_text += '    image_resized = tf.image.resize(image_decoded, [64, 64]) / 255.0\n'
    function_text += '    return image_resized, label\n\n\n'
    function_text += 'def predict_resize_decode(filename):\n'
    function_text += '    image_string = tf.io.read_file(filename)\n'
    function_text += '    image_decoded = tf.image.decode_jpeg(image_string)\n'
    function_text += '    image_resized = tf.image.resize(image_decoded, [64, 64]) / 255.0\n'
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
    function_text += '    model.fit(train_dataset, epochs=num_epochs)\n'
    function_text += '    tf.saved_model.save(model, "saved/job_WRN_back")\n'
    function_text += '    return model\n'
    function_text += ''
    function_text += ''
    function_text += ''

    main_text = ''
    main_text += 'if __name__ == \'__main__\':\n'
    main_text += '    model = train()\n'
    main_text += ''

    model_file_text += function_text

    return model_file_text


def save_text_to_python_file(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()


if __name__ == '__main__':
    text = get_model_file_text()
    print(text)
    save_text_to_python_file(text, 'test.py')
