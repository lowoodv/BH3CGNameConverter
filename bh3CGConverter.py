import os
import shutil
import filecmp
import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.folder_a_label = tk.Label(self, text='国服CG:')
        self.folder_a_label.grid(row=0, column=0)
        self.folder_a_entry = tk.Entry(self)
        self.folder_a_entry.grid(row=0, column=1)
        self.folder_a_button = tk.Button(self, text='Browse', command=self.browse_folder_a)
        self.folder_a_button.grid(row=0, column=2)

        self.folder_b_label = tk.Label(self, text='外服CG:')
        self.folder_b_label.grid(row=1, column=0)
        self.folder_b_entry = tk.Entry(self)
        self.folder_b_entry.grid(row=1, column=1)
        self.folder_b_button = tk.Button(self, text='Browse', command=self.browse_folder_b)
        self.folder_b_button.grid(row=1, column=2)

        self.folder_c_label = tk.Label(self, text='临时文件夹:')
        self.folder_c_label.grid(row=2, column=0)
        self.folder_c_entry = tk.Entry(self)
        self.folder_c_entry.grid(row=2, column=1)
        self.folder_c_button = tk.Button(self, text='Browse', command=self.browse_folder_c)
        self.folder_c_button.grid(row=2, column=2)

        self.rename_button = tk.Button(self, text='CG转化', command=self.rename_files)
        self.rename_button.grid(row=3, columnspan=3)

    def browse_folder_a(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_a_entry.delete(0, tk.END)
            self.folder_a_entry.insert(0, folder_path)

    def browse_folder_b(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_b_entry.delete(0, tk.END)
            self.folder_b_entry.insert(0, folder_path)

    def browse_folder_c(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_c_entry.delete(0, tk.END)
            self.folder_c_entry.insert(0, folder_path)

    def rename_files(self):
        source_folder = self.folder_a_entry.get()
        des_folder = self.folder_b_entry.get()
        temp_folder = self.folder_c_entry.get()

        prefix_strings = {}
        full_file_names = {}
        for file_d in os.listdir(des_folder):
            base_name, extension = os.path.splitext(file_d)
            if extension != '.usm':
                continue
            if '_' in base_name:
                prefix_string = self.get_prfix_string(file_d)
                prefix_strings[prefix_string] = file_d
                full_file_names[prefix_string] = file_d
            full_file_names[base_name] = file_d
                

        for file_s in os.listdir(source_folder):
            base_name, extension = os.path.splitext(file_s)
            if base_name in full_file_names:
                shutil.copy(os.path.join(source_folder, file_s), os.path.join(temp_folder, full_file_names[base_name]))
            else:
                prefix_string = self.get_prfix_string(file_s)
                if prefix_string in prefix_strings:
                    shutil.copy(os.path.join(source_folder, file_s), os.path.join(temp_folder, prefix_strings[prefix_string]))
                elif prefix_string in full_file_names:
                    shutil.copy(os.path.join(source_folder, file_s), os.path.join(temp_folder, full_file_names[prefix_string]))
        self.check_diff(des_folder, temp_folder)

    def get_prfix_string(self, file_name):
        parts = file_name.split('_')
        prefix_string = '_'.join(parts[:-1])
        return prefix_string
    def check_diff(self, des_folder, temp_folder):
        differ = filecmp.dircmp(des_folder, temp_folder)
        with open('需要人工处理的文件.txt', 'w') as f:
            for name in differ.left_only:
                f.write(f'{name}\n')
root = tk.Tk()
app = Application(master=root)
app.mainloop()