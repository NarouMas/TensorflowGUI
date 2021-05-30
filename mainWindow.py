import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from win32api import GetSystemMetrics
import subprocess
import createModelFile
import createPredictFile
import os
import threading


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
        self.activationOption = ['relu', 'None', 'linear', 'softmax']
        self.paddingOption = ['valid', 'same']
        self.booleanOption = ['True', 'False']
        self.layerCount = 0

        self.model_info_label = tk.Label(self.main_window, text='Model Info', bg='#4e5254', fg='white', width=20)
        self.model_info_label.grid(column=0, row=0)
        self.train_data_directory_label = tk.Label(self.main_window, text='Train Data Directory', bg='#4e5254',
                                                   fg='white', width=20)
        self.train_data_directory_label.grid(column=0, row=1)
        self.train_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white', width=20)
        self.train_data_path_label.grid(column=0, row=2)
        self.test_data_directory_label = tk.Label(self.main_window, text='Predict Data Directory', bg='#4e5254',
                                                  fg='white', width=20)
        self.test_data_directory_label.grid(column=0, row=3)
        self.test_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white', width=20)
        self.test_data_path_label.grid(column=0, row=4)

        self.add_layer_button = tk.Button(self.main_window, text='Add Layer', command=self.add_layer)
        self.add_layer_button.grid(column=1, row=17)
        self.remove_layer_button = tk.Button(self.main_window, text='Remove Layer', command=self.remove_layer)
        self.remove_layer_button.grid(column=2, row=17)

        self.run_button = tk.Button(self.main_window, text='Run', command=self.run)
        self.run_button.grid(column=3, row=17)

        self.status_label = tk.Label(self.main_window, text='Status', bg='#4e5254', fg='white')
        self.status_label.grid(column=4, row=17)

        self.status_content_label = tk.Label(self.main_window, text='Setting', bg='#4e5254', fg='#00ff00')
        self.status_content_label.grid(column=5, row=17)

        self.predict_button = tk.Button(self.main_window, text='predict', command=self.predictModel)
        self.predict_button.grid(column=6, row=17)

        self.wide_setting = [{'num_epochs': 10, 'batch_size': 32, 'learning_rate': 0.01, 'width': 64, 'height': 64,
                              'channel': 3, 'modelName' : 'myModel'},
                             tk.Label(self.main_window, text='num_epochs', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='batch_size', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='learning_rate', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='width', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='height', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='channel', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             tk.Label(self.main_window, text='model name', bg='#4e5254', fg='white'),
                             tk.Entry(self.main_window, width=10),
                             ]
        self.wide_setting[1].grid(column=3, row=16, padx=5, pady=5)  # num_epochs label
        self.wide_setting[2].grid(column=4, row=16, padx=5, pady=5)  # num_epochs entry
        self.wide_setting[2].insert(tk.END, '10')
        self.wide_setting[3].grid(column=5, row=16, padx=5, pady=5)  # batch_size label
        self.wide_setting[4].grid(column=6, row=16, padx=5, pady=5)  # batch_size entry
        self.wide_setting[4].insert(tk.END, '32')
        self.wide_setting[5].grid(column=7, row=16, padx=5, pady=5)  # learning_rate label
        self.wide_setting[6].grid(column=8, row=16, padx=5, pady=5)  # learning_rate entry
        self.wide_setting[6].insert(tk.END, '0.001')
        self.wide_setting[7].grid(column=9, row=16, padx=5, pady=5)  # width label
        self.wide_setting[8].grid(column=10, row=16, padx=5, pady=5)  # width entry
        self.wide_setting[8].insert(tk.END, '64')
        self.wide_setting[9].grid(column=11, row=16, padx=5, pady=5)  # height label
        self.wide_setting[10].grid(column=12, row=16, padx=5, pady=5)  # height entry
        self.wide_setting[10].insert(tk.END, '64')
        self.wide_setting[11].grid(column=13, row=16, padx=5, pady=5)  # channel label
        self.wide_setting[12].grid(column=14, row=16, padx=5, pady=5)  # channel entry
        self.wide_setting[12].insert(tk.END, '3')
        self.wide_setting[13].grid(column=1, row=16, padx=5, pady=5)  # model name label
        self.wide_setting[14].grid(column=2, row=16, padx=5, pady=5)  # model name entry
        self.wide_setting[14].insert(tk.END, 'myModel')

    def add_layer(self):
        if self.layerCount > 14:
            tk.messagebox.showerror(title='Error', message='You can at most add 15 layers')
            return
        # add the drop layer drop down menu
        self.layer_variable.append(tk.StringVar(self.main_window, name=str(self.layerCount)))
        self.layer_variable[self.layerCount].set(self.layerOption[0])
        self.layer_opt.append(tk.OptionMenu(self.main_window, self.layer_variable[self.layerCount], *self.layerOption))
        self.layer_variable[self.layerCount].trace("w", self.layer_opt_listener)
        self.layer_opt[self.layerCount].config(width=10, font=('Helvetica', 8))
        self.layer_opt[self.layerCount].grid(column=2, row=self.layerCount, padx=5, pady=5)
        # add layer argument
        layer_argument_conv2d = [{'type': 'Conv2D', 'filters': 32, 'kernel_size': 3, 'strides': 1,
                                  'padding': 'valid', 'activation': 'relu'},
                                 tk.Label(self.main_window, text='filters', bg='#4e5254', fg='white', width=10),
                                 tk.Entry(self.main_window, width=10),
                                 tk.Label(self.main_window, text='kernel_size', bg='#4e5254', fg='white', width=10),
                                 tk.Entry(self.main_window, width=10),
                                 tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white', width=10),
                                 tk.Entry(self.main_window, width=10),
                                 tk.Label(self.main_window, text='activation', bg='#4e5254', fg='white', width=10),
                                 tk.StringVar(self.main_window, name='activation' + str(self.layerCount)),
                                 None,
                                 tk.Label(self.main_window, text='padding', bg='#4e5254', fg='white', width=10),
                                 tk.StringVar(self.main_window, name='padding' + str(self.layerCount)),
                                 None
                                 ]

        layer_argument_conv2d[8].set(self.activationOption[0])
        layer_argument_conv2d[9] = tk.OptionMenu(self.main_window, layer_argument_conv2d[8], *self.activationOption)
        layer_argument_conv2d[8].trace("w", self.layer_activation_opt_listener)

        layer_argument_conv2d[11].set(self.paddingOption[0])
        layer_argument_conv2d[12] = tk.OptionMenu(self.main_window, layer_argument_conv2d[11], *self.paddingOption)

        self.layer_argument.append(layer_argument_conv2d)
        layer_argument_conv2d[1].grid(column=3, row=self.layerCount, padx=5, pady=5)  # filter label
        layer_argument_conv2d[2].grid(column=4, row=self.layerCount, padx=5, pady=5)  # filter entry
        layer_argument_conv2d[2].insert(tk.END, '32')
        layer_argument_conv2d[3].grid(column=5, row=self.layerCount, padx=5, pady=5)  # filter label
        layer_argument_conv2d[4].grid(column=6, row=self.layerCount, padx=5, pady=5)  # filter entry
        layer_argument_conv2d[4].insert(tk.END, '3')
        layer_argument_conv2d[5].grid(column=7, row=self.layerCount, padx=5, pady=5)  # filter label
        layer_argument_conv2d[6].grid(column=8, row=self.layerCount, padx=5, pady=5)  # filter entry
        layer_argument_conv2d[6].insert(tk.END, '1')
        layer_argument_conv2d[7].grid(column=9, row=self.layerCount, padx=5, pady=5)  # activation label
        layer_argument_conv2d[9].config(width=10, font=('Helvetica', 8))
        layer_argument_conv2d[9].grid(column=10, row=self.layerCount, padx=5, pady=5)  # activation option
        layer_argument_conv2d[10].grid(column=11, row=self.layerCount, padx=5, pady=5)  # padding label
        layer_argument_conv2d[12].config(width=10, font=('Helvetica', 8))
        layer_argument_conv2d[12].grid(column=12, row=self.layerCount, padx=5, pady=5)  # padding option
        # grid button in window
        self.layerCount += 1
        #self.add_layer_button.grid(column=1, row=self.layerCount)
        #self.remove_layer_button.grid(column=2, row=self.layerCount)

    def remove_layer(self):
        if self.layerCount <= 0:
            tk.messagebox.showerror(title='Error', message='No more layer to be removed')
            return
        self.layer_opt[self.layerCount - 1].destroy()
        for i in range(1, len(self.layer_argument[self.layerCount - 1])):
            if str(type(self.layer_argument[self.layerCount - 1][i])) != '<class \'tkinter.StringVar\'>':
                self.layer_argument[self.layerCount - 1][i].destroy()
        self.layer_opt.pop(self.layerCount - 1)
        self.layer_variable.pop(self.layerCount - 1)
        self.layer_argument.pop(self.layerCount - 1)
        self.layerCount -= 1
        #self.add_layer_button.grid(column=1, row=self.layerCount)
        #self.remove_layer_button.grid(column=2, row=self.layerCount)

    def run(self):
        if self.trainDataPath is None:
            tk.messagebox.showerror(title='Error', message='Please select train data')
            return
        if self.testDataPath is None:
            tk.messagebox.showerror(title='Error', message='Please select predict data')
            return
        train_dirs = os.listdir(self.trainDataPath)
        test_dirs = os.listdir(self.testDataPath)
        for i in range(len(train_dirs)):
            fullpath = os.path.join(self.trainDataPath, train_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            train_dirs[i] = fullpath

        for i in range(len(test_dirs)):
            fullpath = os.path.join(self.testDataPath, test_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            test_dirs[i] = fullpath

        # set layer arguments
        self.run_button.configure(state='disabled')
        for i in range(0, len(self.layer_argument)):
            self.layer_opt[i].configure(state='disabled')
            if self.layer_argument[i][0]['type'] == 'Conv2D':
                self.layer_argument[i][0]['filters'] = int(self.layer_argument[i][2].get())
                self.layer_argument[i][0]['kernel_size'] = int(self.layer_argument[i][4].get())
                self.layer_argument[i][0]['strides'] = int(self.layer_argument[i][6].get())
                self.layer_argument[i][0]['padding'] = self.layer_argument[i][11].get()
                self.layer_argument[i][0]['activation'] = self.layer_argument[i][8].get()

                self.layer_argument[i][2].configure(state='disabled')
                self.layer_argument[i][4].configure(state='disabled')
                self.layer_argument[i][6].configure(state='disabled')
                self.layer_argument[i][9].configure(state='disabled')
                self.layer_argument[i][12].configure(state='disabled')

            elif self.layer_argument[i][0]['type'] == 'Flatten':
                pass
            elif self.layer_argument[i][0]['type'] == 'MaxPool2D':
                self.layer_argument[i][0]['pool_size'] = int(self.layer_argument[i][2].get())
                self.layer_argument[i][0]['strides'] = int(self.layer_argument[i][4].get())
                self.layer_argument[i][0]['padding'] = self.layer_argument[i][6].get()

                self.layer_argument[i][2].configure(state='disabled')
                self.layer_argument[i][4].configure(state='disabled')
                self.layer_argument[i][7].configure(state='disabled')
            elif self.layer_argument[i][0]['type'] == 'Dense':
                self.layer_argument[i][0]['units'] = int(self.layer_argument[i][2].get())
                self.layer_argument[i][0]['use_bias'] = self.layer_argument[i][8].get()
                self.layer_argument[i][0]['activation'] = self.layer_argument[i][6].get()

                self.layer_argument[i][2].configure(state='disabled')
                self.layer_argument[i][7].configure(state='disabled')
                self.layer_argument[i][9].configure(state='disabled')

        self.wide_setting[0]['num_epochs'] = int(self.wide_setting[2].get())
        self.wide_setting[0]['batch_size'] = int(self.wide_setting[4].get())
        self.wide_setting[0]['learning_rate'] = float(self.wide_setting[6].get())
        self.wide_setting[0]['width'] = int(self.wide_setting[8].get())
        self.wide_setting[0]['height'] = int(self.wide_setting[10].get())
        self.wide_setting[0]['channel'] = int(self.wide_setting[12].get())
        self.wide_setting[0]['modelName'] = self.wide_setting[14].get()

        self.wide_setting[2].configure(state='disabled')
        self.wide_setting[4].configure(state='disabled')
        self.wide_setting[6].configure(state='disabled')
        self.wide_setting[8].configure(state='disabled')
        self.wide_setting[10].configure(state='disabled')
        self.wide_setting[12].configure(state='disabled')
        self.wide_setting[14].configure(state='disabled')

        self.add_layer_button.configure(state='disabled')
        self.remove_layer_button.configure(state='disabled')

        text = createModelFile.get_model_file_text(self.layer_argument, train_dirs, test_dirs, self.wide_setting)
        createModelFile.save_text_to_python_file(text, 'myModel.py')

        cmd = ['python', 'myModel.py']
        thread = threading.Thread(target=self.execute_os_system, args=('python myModel.py',))
        self.status_content_label['text'] = 'Training Model'
        self.status_content_label['fg'] = '#ff0000'
        thread.start()


    def predictModel(self):
        if self.trainDataPath is None:
            tk.messagebox.showerror(title='Error', message='Please select train data')
            return
        if self.testDataPath is None:
            tk.messagebox.showerror(title='Error', message='Please select predict data')
            return
        train_dirs = os.listdir(self.trainDataPath)
        test_dirs = os.listdir(self.testDataPath)
        for i in range(len(train_dirs)):
            fullpath = os.path.join(self.trainDataPath, train_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            #train_dirs[i] = fullpath

        for i in range(len(test_dirs)):
            fullpath = os.path.join(self.testDataPath, test_dirs[i])
            fullpath = fullpath.replace('\\', '/')
            test_dirs[i] = fullpath
        self.predict_button.configure(state='disable')
        text = createPredictFile.get_predict_file_text(self.testDataPath, train_dirs, self.wide_setting)
        createPredictFile.save_text_to_python_file(text, 'predictImage.py')
        thread = threading.Thread(target=self.execute_os_system, args=('python predictImage.py',))
        self.status_content_label['text'] = 'Predicting Model'
        self.status_content_label['fg'] = '#ff0000'
        thread.start()


    def execute_os_system(self, command):
        os.system(command)

        self.run_button.configure(state='normal')
        for i in range(0, len(self.layer_argument)):
            self.layer_opt[i].configure(state='normal')
            if self.layer_argument[i][0]['type'] == 'Conv2D':
                self.layer_argument[i][2].configure(state='normal')
                self.layer_argument[i][4].configure(state='normal')
                self.layer_argument[i][6].configure(state='normal')
                self.layer_argument[i][9].configure(state='normal')
                self.layer_argument[i][12].configure(state='normal')

            elif self.layer_argument[i][0]['type'] == 'Flatten':
                pass
            elif self.layer_argument[i][0]['type'] == 'MaxPool2D':
                self.layer_argument[i][2].configure(state='normal')
                self.layer_argument[i][4].configure(state='normal')
                self.layer_argument[i][7].configure(state='normal')
            elif self.layer_argument[i][0]['type'] == 'Dense':
                self.layer_argument[i][2].configure(state='normal')
                self.layer_argument[i][7].configure(state='normal')
                self.layer_argument[i][9].configure(state='normal')

        self.wide_setting[2].configure(state='normal')
        self.wide_setting[4].configure(state='normal')
        self.wide_setting[6].configure(state='normal')
        self.wide_setting[8].configure(state='normal')
        self.wide_setting[10].configure(state='normal')
        self.wide_setting[12].configure(state='normal')
        self.wide_setting[14].configure(state='normal')

        self.add_layer_button.configure(state='normal')
        self.remove_layer_button.configure(state='normal')

        f = open('result.txt', 'r')
        status = f.readline()
        print('status:', status)
        if status == 'success\n':
            self.status_content_label['text'] = 'Finish'
            self.status_content_label['fg'] = '#00ff00'
        elif status == 'error\n':
            self.status_content_label['text'] = 'Error'
            self.status_content_label['fg'] = '#ff0000'
        else:
            self.status_content_label['text'] = 'WTF?'
            self.status_content_label['fg'] = '#0000ff'

    def excute_os_system_predict(self, command):
        os.system(command)
        self.predict_button.configure(state='normal')
        f = open('result.txt', 'r')
        status = f.readline()
        print('status:', status)
        if status == 'success\n':
            self.status_content_label['text'] = 'Finish'
            self.status_content_label['fg'] = '#00ff00'
        elif status == 'error\n':
            self.status_content_label['text'] = 'Error'
            self.status_content_label['fg'] = '#ff0000'
        else:
            self.status_content_label['text'] = 'WTF?'
            self.status_content_label['fg'] = '#0000ff'

    def layer_opt_listener(self, var, index, mode):
        var = int(var)
        text = self.layer_variable[var].get()
        print('layer index:', var, ' text:', text)

        # clear old argument
        for i in range(1, len(self.layer_argument[var])):
            if str(type(self.layer_argument[var][i])) != '<class \'tkinter.StringVar\'>':
                self.layer_argument[var][i].destroy()
        self.layer_argument[var] = []

        # add new argument
        if text == 'Conv2D':
            layer_argument_conv2d = [{'type': 'Conv2D', 'filters': 32, 'kernel_size': 3, 'strides': 1,
                                      'padding': 'valid', 'activation': 'relu'},
                                     tk.Label(self.main_window, text='filters', bg='#4e5254', fg='white', width=10),
                                     tk.Entry(self.main_window, width=10),
                                     tk.Label(self.main_window, text='kernel_size', bg='#4e5254', fg='white', width=10),
                                     tk.Entry(self.main_window, width=10),
                                     tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white', width=10),
                                     tk.Entry(self.main_window, width=10),
                                     tk.Label(self.main_window, text='activation', bg='#4e5254', fg='white', width=10),
                                     tk.StringVar(self.main_window, name='activation' + str(var)),
                                     None,
                                     tk.Label(self.main_window, text='padding', bg='#4e5254', fg='white', width=10),
                                     tk.StringVar(self.main_window, name='padding' + str(var)),
                                     None
                                     ]
            layer_argument_conv2d[8].set(self.activationOption[0])
            layer_argument_conv2d[9] = tk.OptionMenu(self.main_window, layer_argument_conv2d[8], *self.activationOption)
            layer_argument_conv2d[8].trace("w", self.layer_activation_opt_listener)

            layer_argument_conv2d[11].set(self.paddingOption[0])
            layer_argument_conv2d[12] = tk.OptionMenu(self.main_window, layer_argument_conv2d[11], *self.paddingOption)

            self.layer_argument[var] = layer_argument_conv2d
            layer_argument_conv2d[1].grid(column=3, row=var, padx=5, pady=5)  # filter label
            layer_argument_conv2d[2].grid(column=4, row=var, padx=5, pady=5)  # filter entry
            layer_argument_conv2d[2].insert(tk.END, '32')
            layer_argument_conv2d[3].grid(column=5, row=var, padx=5, pady=5)  # filter label
            layer_argument_conv2d[4].grid(column=6, row=var, padx=5, pady=5)  # filter entry
            layer_argument_conv2d[4].insert(tk.END, '3')
            layer_argument_conv2d[5].grid(column=7, row=var, padx=5, pady=5)  # filter label
            layer_argument_conv2d[6].grid(column=8, row=var, padx=5, pady=5)  # filter entry
            layer_argument_conv2d[6].insert(tk.END, '1')
            layer_argument_conv2d[7].grid(column=9, row=var, padx=5, pady=5)  # activation label
            layer_argument_conv2d[9].config(width=10, font=('Helvetica', 8))
            layer_argument_conv2d[9].grid(column=10, row=var, padx=5, pady=5)  # activation option
            layer_argument_conv2d[10].grid(column=11, row=var, padx=5, pady=5)  # padding label
            layer_argument_conv2d[12].config(width=10, font=('Helvetica', 8))
            layer_argument_conv2d[12].grid(column=12, row=var, padx=5, pady=5)  # padding option
        elif text == 'Flatten':
            layer_argument_flatten = [{'type': 'Flatten'}]
            self.layer_argument[var] = layer_argument_flatten
        elif text == 'MaxPool2D':
            layer_argument_pool = [{'type': 'MaxPool2D', 'pool_size': 2, 'strides': 3, 'padding': 'valid'},
                                   tk.Label(self.main_window, text='pool size', bg='#4e5254', fg='white', width=10),
                                   tk.Entry(self.main_window, width=10),
                                   tk.Label(self.main_window, text='strides', bg='#4e5254', fg='white', width=10),
                                   tk.Entry(self.main_window, width=10),
                                   tk.Label(self.main_window, text='padding', bg='#4e5254', fg='white', width=10),
                                   tk.StringVar(self.main_window, name='padding' + str(var)),
                                   None
                                   ]

            layer_argument_pool[6].set(self.paddingOption[0])
            layer_argument_pool[7] = tk.OptionMenu(self.main_window, layer_argument_pool[6], *self.paddingOption)

            self.layer_argument[var] = layer_argument_pool
            layer_argument_pool[1].grid(column=3, row=var, padx=5, pady=5)  # pool_size label
            layer_argument_pool[2].grid(column=4, row=var, padx=5, pady=5)  # pool_size entry
            layer_argument_pool[2].insert(tk.END, '2')
            layer_argument_pool[3].grid(column=5, row=var, padx=5, pady=5)  # strides label
            layer_argument_pool[4].grid(column=6, row=var, padx=5, pady=5)  # strides entry
            layer_argument_pool[4].insert(tk.END, '3')
            layer_argument_pool[5].grid(column=7, row=var, padx=5, pady=5)  # padding label
            layer_argument_pool[7].config(width=10, font=('Helvetica', 8))
            layer_argument_pool[7].grid(column=8, row=var, padx=5, pady=5)  # padding option
        elif text == 'Dense':
            layer_argument_dense = [{'type': 'Dense', 'units': 10, 'use_bias': True, 'activation': 'relu'},
                                    tk.Label(self.main_window, text='units', bg='#4e5254', fg='white', width=10),
                                    tk.Entry(self.main_window, width=10),
                                    tk.Label(self.main_window, text='use_bias', bg='#4e5254', fg='white', width=10),
                                    tk.Entry(self.main_window, width=10),
                                    tk.Label(self.main_window, text='activation', bg='#4e5254', fg='white', width=10),
                                    tk.StringVar(self.main_window, name='activation' + str(var)),
                                    tk.Label(self.main_window, text='use_bias', bg='#4e5254', fg='white', width=10),
                                    tk.StringVar(self.main_window, name='use_bias' + str(var)),
                                    None
                                    ]

            layer_argument_dense[6].set(self.activationOption[0])
            layer_argument_dense[7] = tk.OptionMenu(self.main_window, layer_argument_dense[6], *self.activationOption)

            layer_argument_dense[8].set(self.booleanOption[0])
            layer_argument_dense[9] = tk.OptionMenu(self.main_window, layer_argument_dense[8], *self.booleanOption)

            self.layer_argument[var] = layer_argument_dense
            layer_argument_dense[1].grid(column=3, row=var, padx=5, pady=5)  # units label
            layer_argument_dense[2].grid(column=4, row=var, padx=5, pady=5)  # units entry
            layer_argument_dense[2].insert(tk.END, '10')
            layer_argument_dense[3].grid(column=5, row=var, padx=5, pady=5)  # use_bias label
            #layer_argument_dense[4].grid(column=6, row=var)  # use_bias entry
            #layer_argument_dense[4].insert(tk.END, 'True')
            layer_argument_dense[5].grid(column=7, row=var, padx=5, pady=5)  # activation label
            layer_argument_dense[7].config(width=10, font=('Helvetica', 8))
            layer_argument_dense[7].grid(column=8, row=var, padx=5, pady=5)  # activation option
            #layer_argument_dense[5].grid(column=9, row=var)  # use_bias label
            layer_argument_dense[9].config(width=10, font=('Helvetica', 8))
            layer_argument_dense[9].grid(column=6, row=var, padx=5, pady=5)  # use_bias option

    def layer_activation_opt_listener(self, var, index, mode):
        pass

    def init_tool_bar(self):
        menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label='Open', command=self.file_menu_open)
        file_menu.add_command(label='Select Train Data', command=self.file_menu_select_train)
        file_menu.add_command(label='Select Predict Data', command=self.file_menu_select_test)
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
        index = 0
        for i in range(len(data_path) - 1, 0, -1):
            if data_path[i] == '/':
                index = i
                break
        if len(data_path) > 0:
            self.trainDataPath = data_path
            self.train_data_path_label['text'] = data_path[index + 1:]
            print('train data path:' + self.trainDataPath)
        else:
            print('train data path is not selected')

    def file_menu_select_test(self):
        data_path = tk.filedialog.askdirectory(parent=self.main_window, title='Select Test Directory',
                                               initialdir='./')
        index = 0
        for i in range(len(data_path) - 1, 0, -1):
            if data_path[i] == '/':
                index = i
                break
        if len(data_path) > 0:
            self.testDataPath = data_path
            self.test_data_path_label['text'] = data_path[index + 1:]
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
