import tkinter as tk
from tkinter import filedialog
from win32api import GetSystemMetrics
import subprocess


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
        self.train_data_directory_label = tk.Label(self.main_window, text='Train Data Directory', bg='#4e5254', fg='white')
        self.train_data_directory_label.grid(column=0, row=1)
        self.train_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white')
        self.train_data_path_label.grid(column=0, row=2)
        self.test_data_directory_label = tk.Label(self.main_window, text='Test Data Directory', bg='#4e5254', fg='white')
        self.test_data_directory_label.grid(column=0, row=3)
        self.test_data_path_label = tk.Label(self.main_window, text='Not Selected', bg='#4e5254', fg='white')
        self.test_data_path_label.grid(column=0, row=4)

        self.add_layer_button = tk.Button(self.main_window, text='Add Layer', command=self.add_layer)
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button = tk.Button(self.main_window, text='Remove Layer', command=self.remove_layer)
        self.remove_layer_button.grid(column=2, row=self.layerCount)

    def add_layer(self):
        self.layer_variable.append(tk.StringVar(self.main_window, name=str(self.layerCount)))
        self.layer_variable[self.layerCount].set(self.layerOption[0])
        self.layer_opt.append(tk.OptionMenu(self.main_window, self.layer_variable[self.layerCount], *self.layerOption))
        self.layer_variable[self.layerCount].trace("w", self.layer_opt_listener)
        self.layer_opt[self.layerCount].config(width=20, font=('Helvetica', 8))
        self.layer_opt[self.layerCount].grid(column=2, row=self.layerCount)
        self.layerCount += 1
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button.grid(column=2, row=self.layerCount)

    def remove_layer(self):
        if self.layerCount <= 0:
            return
        self.layer_opt[self.layerCount - 1].destroy()
        self.layer_opt.pop(self.layerCount - 1)
        self.layer_variable.pop(self.layerCount - 1)
        self.layerCount -= 1
        self.add_layer_button.grid(column=1, row=self.layerCount)
        self.remove_layer_button.grid(column=2, row=self.layerCount)


    def layer_opt_listener(self, var, index, mode):
        text = self.layer_variable[int(var)].get()
        print('layer index:', var, ' text:', text)

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
