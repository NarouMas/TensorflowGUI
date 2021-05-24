import tkinter as tk
from tkinter import filedialog
from win32api import GetSystemMetrics
import subprocess
import createModelFile
import os


class TfMainWindow:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('TensorFlow Window')
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)
        self.main_window.geometry('{}x{}'.format(screen_width, screen_height))
        self.main_window['background'] = '#3c3f41'
        self.init_tool_bar()

        self.trainDataPath = None
        self.testDataPath = None
        self.modelStructure = []
        self.layer_opt = []
        self.layer_variable = []
        self.layer_argument = []
        self.layerOption = ['Conv2D', 'Flatten', 'MaxPool2D', 'Dense']
        self.layerCount = 0

        self.model_info_label = tk.Label(self.main_window, text='Model Info', bg='#4e5254', fg='white')
        self.model_info_label.grid(column=0, row=0)
        self.train_data_directory_label = tk.Label(self.main_window, text='Train Data Directory', bg='#4e5254',
                                                   fg='white')
        self.train_data_directory_label.grid(column=0, row=1)
        self.train_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white')
        self.train_data_path_label.grid(column=0, row=2)
        self.test_data_directory_label = tk.Label(self.main_window, text='Test Data Directory', bg='#4e5254',
                                                  fg='white')
        self.test_data_directory_label.grid(column=0, row=3)
        self.test_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white')
        self.test_data_path_label.grid(column=0, row=4)

        self.add_layer_button = tk.Button(self.main_window, text='Add Layer', command=self.add_layer)
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button = tk.Button(self.main_window, text='Remove Layer', command=self.remove_layer)
        self.remove_layer_button.grid(column=2, row=self.layerCount)

        self.run_button = tk.Button(self.main_window, text='Run', command=self.run)
        self.run_button.grid(column=1, row=10)

    def add_layer(self):
        # add the drop layer drop down menu
        self.layer_variable.append(tk.StringVar(self.main_window, name=str(self.layerCount)))
        self.layer_variable[self.layerCount].set(self.layerOption[0])
        self.layer_opt.append(tk.OptionMenu(self.main_window, self.layer_variable[self.layerCount], *self.layerOption))
        self.layer_variable[self.layerCount].trace("w", self.layer_opt_listener)
        self.layer_opt[self.layerCount].config(width=20, font=('Helvetica', 8))
        self.layer_opt[self.layerCount].grid(column=2, row=self.layerCount)
        # add layer argument
        layer_argument_conv2d = [{'type': 'Conv2D', 'filters': 32, 'kernel_size': 3, 'strides': 1,
                                  'padding': 'valid', 'activation': 'relu'},
                                 tk.Label(self.main_window, text='filters', bg='#4e5254', fg='white'),
                                 tk.Entry(self.main_window, width=10),
                                 tk.Label(self.main_window, text='kernel_size', bg='#4e5254', fg='white'),
                                 tk.Entry(self.main_window, width=10),
                                 tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white'),
                                 tk.Entry(self.main_window, width=10),
                                 ]
        self.layer_argument.append(layer_argument_conv2d)
        layer_argument_conv2d[1].grid(column=3, row=self.layerCount)  # filter label
        layer_argument_conv2d[2].grid(column=4, row=self.layerCount)  # filter entry
        layer_argument_conv2d[2].insert(tk.END, '32')
        layer_argument_conv2d[3].grid(column=5, row=self.layerCount)  # filter label
        layer_argument_conv2d[4].grid(column=6, row=self.layerCount)  # filter entry
        layer_argument_conv2d[4].insert(tk.END, '3')
        layer_argument_conv2d[5].grid(column=7, row=self.layerCount)  # filter label
        layer_argument_conv2d[6].grid(column=8, row=self.layerCount)  # filter entry
        layer_argument_conv2d[6].insert(tk.END, '1')
        # grid button in window
        self.layerCount += 1
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button.grid(column=2, row=self.layerCount)

    def remove_layer(self):
        if self.layerCount <= 0:
            return
        self.layer_opt[self.layerCount - 1].destroy()
        for i in range(1, len(self.layer_argument[self.layerCount - 1])):
            self.layer_argument[self.layerCount - 1][i].destroy()
        self.layer_opt.pop(self.layerCount - 1)
        self.layer_variable.pop(self.layerCount - 1)
        self.layer_argument.pop(self.layerCount - 1)
        self.layerCount -= 1
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button.grid(column=2, row=self.layerCount)

    def run(self):
        train_dirs = os.listdir(self.trainDataPath)
        test_dirs = os.listdir(self.testDataPath)
        for i in range(len(train_dirs)):
            fullpath = os.path.join(self.trainDataPath, train_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            train_dirs[i] = fullpath
        """
        for i in range(len(test_dirs)):
            fullpath = os.path.join(self.testDataPath, test_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            test_dirs[i] = fullpath
        """

        text = createModelFile.get_model_file_text(self.layer_argument, train_dirs, test_dirs)
        #createModelFile.save_text_to_python_file(text, 'myModel.py')

        cmd = ['python', 'myModel.py']
        os.system('python myModel.py')
        #output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        #print('capture output:', str(output))

    def layer_opt_listener(self, var, index, mode):
        var = int(var)
        text = self.layer_variable[var].get()
        print('layer index:', var, ' text:', text)

        # clear old argument
        for i in range(1, len(self.layer_argument[var])):
            self.layer_argument[var][i].destroy()
        self.layer_argument[var] = []

        # add new argument
        if text == 'Conv2D':
            layer_argument_conv2d = [{'type': 'Conv2D', 'filters': 32, 'kernel_size': 3, 'strides': 1,
                                      'padding': 'valid', 'activation': 'relu'},
                                     tk.Label(self.main_window, text='filters', bg='#4e5254', fg='white'),
                                     tk.Entry(self.main_window, width=10),
                                     tk.Label(self.main_window, text='kernel_size', bg='#4e5254', fg='white'),
                                     tk.Entry(self.main_window, width=10),
                                     tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white'),
                                     tk.Entry(self.main_window, width=10)
                                     ]
            self.layer_argument[var] = layer_argument_conv2d
            layer_argument_conv2d[1].grid(column=3, row=var)  # filter label
            layer_argument_conv2d[2].grid(column=4, row=var)  # filter entry
            layer_argument_conv2d[2].insert(tk.END, '32')
            layer_argument_conv2d[3].grid(column=5, row=var)  # filter label
            layer_argument_conv2d[4].grid(column=6, row=var)  # filter entry
            layer_argument_conv2d[4].insert(tk.END, '3')
            layer_argument_conv2d[5].grid(column=7, row=var)  # filter label
            layer_argument_conv2d[6].grid(column=8, row=var)  # filter entry
            layer_argument_conv2d[6].insert(tk.END, '1')
        elif text == 'Flatten':
            layer_argument_flatten = [{'type': 'Flatten'}]
            self.layer_argument[var] = layer_argument_flatten
        elif text == 'MaxPool2D':
            layer_argument_pool = [{'type': 'MaxPool2D', 'pool_size': 2, 'strides': 3, 'padding': 'valid'},
                                   tk.Label(self.main_window, text='pool size', bg='#4e5254', fg='white'),
                                   tk.Entry(self.main_window, width=10),
                                   tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white'),
                                   tk.Entry(self.main_window, width=10)
                                   ]
            self.layer_argument[var] = layer_argument_pool
            layer_argument_pool[1].grid(column=3, row=var)  # pool_size label
            layer_argument_pool[2].grid(column=4, row=var)  # pool_size entry
            layer_argument_pool[2].insert(tk.END, '2')
            layer_argument_pool[3].grid(column=5, row=var)  # strides label
            layer_argument_pool[4].grid(column=6, row=var)  # strides entry
            layer_argument_pool[4].insert(tk.END, '3')
        elif text == 'Dense':
            layer_argument_dense = [{'type': 'Dense', 'units': 10, 'use_bias': True, 'activation': 'relu'},
                                   tk.Label(self.main_window, text='units', bg='#4e5254', fg='white'),
                                   tk.Entry(self.main_window, width=10),
                                   tk.Label(self.main_window, text='use_bias', bg='#4e5254', fg='white'),
                                   tk.Entry(self.main_window, width=10)
                                   ]
            self.layer_argument[var] = layer_argument_dense
            layer_argument_dense[1].grid(column=3, row=var)  # units label
            layer_argument_dense[2].grid(column=4, row=var)  # units entry
            layer_argument_dense[2].insert(tk.END, '10')
            layer_argument_dense[3].grid(column=5, row=var)  # use_bias label
            layer_argument_dense[4].grid(column=6, row=var)  # use_bias entry
            layer_argument_dense[4].insert(tk.END, 'True')

    def init_tool_bar(self):
        menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label='Open', command=self.file_menu_open)
        file_menu.add_command(label='Select Train Data', command=self.file_menu_select_train)
        file_menu.add_command(label='Select Test Data', command=self.file_menu_select_test)
        file_menu.add_command(label='Exit', command=self.file_menu_exit)
        menu_bar.add_cascade(label='File', menu=file_menu)

    def file_menu_open(self):
        print('open')
        cmd = ['python', 'test.py']
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        print('capture output:', str(output))

    def file_menu_select_train(self):
        data_path = tk.filedialog.askdirectory(parent=self.main_window, title='Select Train Directory',
                                               initialdir='./')
        if len(data_path) > 0:
            self.trainDataPath = data_path
            self.train_data_path_label['text'] = data_path
            print('train data path:' + self.trainDataPath)
        else:
            print('train data path is not selected')

    def file_menu_select_test(self):
        data_path = tk.filedialog.askdirectory(parent=self.main_window, title='Select Test Directory',
                                               initialdir='./')
        if len(data_path) > 0:
            self.testDataPath = data_path
            self.test_data_path_label['text'] = data_path
            print('test data path:' + self.testDataPath)
        else:
            print('test data path is not selected')

    def file_menu_exit(self):
        self.main_window.quit()

    def start(self):
        self.main_window.mainloop()


if __name__ == '__main__':
    main_window = TfMainWindow()
    main_window.start()
