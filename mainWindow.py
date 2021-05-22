import tkinter as tk
from win32api import GetSystemMetrics


class TfMainWindow:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title('TensorFlow Window')
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)
        self.main_window.geometry('{}x{}'.format(screen_width, screen_height))
        self.main_window['background'] = '#3c3f41'
        self.init_tool_bar()

        model_info_label = tk.Label(self.main_window, text='Model Info', bg='#4e5254', fg='white')
        model_info_label.grid(column=0, row=0)

    def init_tool_bar(self):
        menu_bar = tk.Menu(self.main_window)
        self.main_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label='Open', command=self.file_menu_open)
        file_menu.add_command(label='Exit', command=self.file_menu_exit)
        menu_bar.add_cascade(label='File', menu=file_menu)

    def file_menu_open(self):
        print('open')

    def file_menu_exit(self):
        self.main_window.quit()

    def start(self):
        self.main_window.mainloop()


if __name__ == '__main__':
    main_window = TfMainWindow()
    main_window.start()