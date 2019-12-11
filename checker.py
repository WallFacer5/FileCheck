# -*- coding: utf-8 -*-
"""
@author: Yanhan Zhang
@Due_date: Dec. 12th, 2019
"""

from md5 import Md5Checker
from sha3 import Sha3Checker
import tkinter as tk
import tkinter.filedialog as fd
import bitstring


class Checker:
    def __init__(self, msg, algo, is_file=False):
        if is_file:
            origin_msg = msg
            msg = bitstring.BitArray(open(msg, 'rb').read()).int
            self.byte_stream = msg
            print('Msg:')
            print(bin(msg))
            print(hex(msg))
            print()
            if algo == 'md5':
                self.checker = Md5Checker(self.byte_stream)
            elif algo == 'sha3':
                self.checker = Sha3Checker(origin_msg, True)
        else:
            if msg == '':
                origin_msg = ''
                msg = 0
            else:
                origin_msg = msg
                msg = eval('0x' + bytes(msg.encode()).hex())
            self.byte_stream = msg
            print('Msg:')
            print(bin(msg))
            print(hex(msg))
            print()
            if algo == 'md5':
                self.checker = Md5Checker(self.byte_stream)
            elif algo == 'sha3':
                self.checker = Sha3Checker(origin_msg, False)

    def get_hash(self):
        return self.checker.get_hash()


def main():
    msg = input('Please input the msg: ')
    hash_func = input('Please input the hash function you want to use(md5, sha3): ')
    checker = Checker(msg, hash_func)
    print(hash_func, 'hash of', msg, 'is', checker.get_hash())


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.choose_input()

    def choose_input(self):
        self.radio_buttons = tk.Frame(self)
        self.choose_v = tk.IntVar()
        self.string_rb = tk.Radiobutton(self.radio_buttons, variable=self.choose_v, text='String Input', value=0)
        self.file_rb = tk.Radiobutton(self.radio_buttons, variable=self.choose_v, text='File Input', value=1)
        self.string_compare_rb = tk.Radiobutton(self.radio_buttons, variable=self.choose_v, text='String Compare',
                                                value=2)
        self.file_compare_rb = tk.Radiobutton(self.radio_buttons, variable=self.choose_v, text='File Compare', value=3)
        self.string_rb.grid(row=0, column=0, sticky=tk.W)
        self.file_rb.grid(row=1, column=0, sticky=tk.W)
        self.string_compare_rb.grid(row=2, column=0, sticky=tk.W)
        self.file_compare_rb.grid(row=3, column=0, sticky=tk.W)
        self.radio_buttons.pack()

        self.choose_button = tk.Button(self, text='Choose', command=self.choose_jump)
        self.choose_button.pack()

    def choose_jump(self):
        self.radio_buttons.destroy()
        self.choose_button.destroy()
        print(self.choose_v.get())
        if self.choose_v.get() == 0:
            self.jump_string()
        elif self.choose_v.get() == 1:
            self.jump_file()
        elif self.choose_v.get() == 2:
            self.jump_string_compare()
        elif self.choose_v.get() == 3:
            self.jump_file_compare()

    def back_to_main(self):
        try:
            self.string_frame.destroy()
        except Exception:
            pass
        try:
            self.file_frame.destroy()
        except Exception:
            pass
        try:
            self.strcmp_frame.destroy()
        except Exception:
            pass
        try:
            self.filecmp_frame.destroy()
        except Exception:
            pass
        self.choose_input()

    def jump_string(self):
        self.string_frame = tk.Frame(self)
        self.string_label = tk.Label(self.string_frame, text='Input string')
        self.string_input = tk.Entry(self.string_frame, width=39)
        self.string_label.grid(row=0, column=0, sticky=tk.W)
        self.string_input.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        self.hash_func = tk.IntVar()

        self.hash_label = tk.Label(self.string_frame, text='Hash Function')
        self.md5_rb = tk.Radiobutton(self.string_frame, variable=self.hash_func, text='md5', value=0)
        self.sha3_rb = tk.Radiobutton(self.string_frame, variable=self.hash_func, text='sha3', value=1)
        self.hash_label.grid(row=1, column=0, sticky=tk.W)
        self.md5_rb.grid(row=1, column=1, sticky=tk.W)
        self.sha3_rb.grid(row=1, column=2, sticky=tk.W)

        self.string_button = tk.Button(self.string_frame, text='Hash!', command=self.do_hash)
        self.string_button.grid(row=2, columnspan=3)

        self.hash_out_label = tk.Label(self.string_frame, text='Hash Result')
        self.hash_out_text = tk.Text(self.string_frame, height=2, width=50)
        self.hash_out_text.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label.grid(row=3, column=0)
        self.hash_out_text.grid(row=3, column=1, columnspan=2)

        self.back_button = tk.Button(self.string_frame, text='Back', command=self.back_to_main)
        self.back_button.grid(row=4, column=0, columnspan=3)

        self.string_frame.pack()

    def do_hash(self):
        msg = self.string_input.get()
        print(msg)
        hash_func = self.hash_func.get()
        if hash_func == 0:
            hash_func = 'md5'
        else:
            hash_func = 'sha3'
        print(hash_func)
        checker = Checker(msg, hash_func, is_file=False)
        print(hash_func, 'hash of', msg, 'is', checker.get_hash())

        self.hash_out_text.config(state=tk.NORMAL)
        self.hash_out_text.delete(0.0, tk.END)
        self.hash_out_text.insert(tk.END, checker.get_hash())
        self.hash_out_text.config(state=tk.DISABLED)

    def file_selection(self):
        file_want = fd.askopenfile()
        file_path = file_want.name
        print(file_path)
        self.file_input.delete(0, tk.END)
        self.file_input.insert(tk.END, file_path)
        file_want.close()
        self.file_input.config(text=file_path)

    def jump_file(self):
        self.file_frame = tk.Frame(self)
        self.file_label = tk.Label(self.file_frame, text='Input file')
        self.file_input = tk.Entry(self.file_frame, width=58)
        self.file_choose_btn = tk.Button(self.file_frame, text='Select File', command=self.file_selection)

        self.file_label.grid(row=0, column=0, sticky=tk.W)
        self.file_input.grid(row=0, column=1, sticky=tk.W)
        self.file_choose_btn.grid(row=0, column=2, sticky=tk.W)

        self.hash_func = tk.IntVar()

        self.hash_label = tk.Label(self.file_frame, text='Hash Function')
        self.hash_frame = tk.Frame(self.file_frame)
        self.md5_rb = tk.Radiobutton(self.hash_frame, variable=self.hash_func, text='md5', value=0)
        self.sha3_rb = tk.Radiobutton(self.hash_frame, variable=self.hash_func, text='sha3', value=1)
        self.hash_label.grid(row=1, column=0, sticky=tk.W)
        self.md5_rb.grid(row=0, column=0, sticky=tk.W)
        self.sha3_rb.grid(row=0, column=1, sticky=tk.W)
        self.hash_frame.grid(row=1, column=1, sticky=tk.W)

        self.file_button = tk.Button(self.file_frame, text='Hash!', command=self.do_file_hash)
        self.file_button.grid(row=2, columnspan=3)

        self.hash_out_label = tk.Label(self.file_frame, text='Hash Result')
        self.hash_out_text = tk.Text(self.file_frame, height=3, width=87)
        self.hash_out_text.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label.grid(row=3, column=0)
        self.hash_out_text.grid(row=3, column=1, columnspan=2)

        self.back_button = tk.Button(self.file_frame, text='Back', command=self.back_to_main)
        self.back_button.grid(row=4, column=0, columnspan=3)

        self.file_frame.pack()

    def warning_process(self):
        self.warning_window.destroy()
        self.file_input.delete(0, tk.END)

    def warning_process1(self):
        self.warning_window1.destroy()
        self.filecmp_input1.delete(0, tk.END)

    def warning_process2(self):
        self.warning_window2.destroy()
        self.filecmp_input2.delete(0, tk.END)

    def do_file_hash(self):
        try:
            self.warning_window.destroy()
        except Exception:
            pass
        self.hash_out_text.config(state=tk.NORMAL)
        self.hash_out_text.delete(0.0, tk.END)
        try:
            file_path = self.file_input.get()
            print('File path:', file_path)
            try_f = open(file_path, 'r')
            try_f.close()
            hash_func = self.hash_func.get()
            if hash_func == 0:
                hash_func = 'md5'
            else:
                hash_func = 'sha3'
            print(hash_func)
            checker = Checker(file_path, hash_func, is_file=True)
            print(hash_func, 'hash of', file_path, 'is', checker.get_hash())
            self.hash_out_text.insert(tk.END, checker.get_hash())
            self.hash_out_text.config(state=tk.DISABLED)
        except Exception:
            print('No such file!')
            self.warning_window = tk.Frame(self)
            self.warning_msg = tk.Label(self.warning_window, fg='red',
                                        text='No such file!\nPlease re-input your file path!')
            self.warning_btn = tk.Button(self.warning_window, text='Understand', command=self.warning_process)
            self.warning_msg.pack()
            self.warning_btn.pack()
            self.warning_window.pack()
            self.hash_out_text.config(state=tk.DISABLED)

    def jump_string_compare(self):
        self.strcmp_frame = tk.Frame(self)
        self.strcmp_label1 = tk.Label(self.strcmp_frame, text='Input string1')
        self.strcmp_input1 = tk.Entry(self.strcmp_frame, width=39)
        self.strcmp_label1.grid(row=0, column=0, sticky=tk.W)
        self.strcmp_input1.grid(row=0, column=1, columnspan=2, sticky=tk.W)

        self.strcmp_label2 = tk.Label(self.strcmp_frame, text='Input string2')
        self.strcmp_input2 = tk.Entry(self.strcmp_frame, width=39)
        self.strcmp_label2.grid(row=1, column=0, sticky=tk.W)
        self.strcmp_input2.grid(row=1, column=1, columnspan=2, sticky=tk.W)

        self.hash_func = tk.IntVar()

        self.hash_label = tk.Label(self.strcmp_frame, text='Hash Function')
        self.md5_rb = tk.Radiobutton(self.strcmp_frame, variable=self.hash_func, text='md5', value=0)
        self.sha3_rb = tk.Radiobutton(self.strcmp_frame, variable=self.hash_func, text='sha3', value=1)
        self.hash_label.grid(row=2, column=0, sticky=tk.W)
        self.md5_rb.grid(row=2, column=1, sticky=tk.W)
        self.sha3_rb.grid(row=2, column=2, sticky=tk.W)

        self.string_button = tk.Button(self.strcmp_frame, text='Compare!', command=self.do_hash_cmp)
        self.string_button.grid(row=3, columnspan=3)

        self.hash_out_label1 = tk.Label(self.strcmp_frame, text='Hash Result1')
        self.hash_out_text1 = tk.Text(self.strcmp_frame, height=5, width=50)
        self.hash_out_text1.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label1.grid(row=4, column=0)
        self.hash_out_text1.grid(row=4, column=1, columnspan=2)

        self.hash_out_label2 = tk.Label(self.strcmp_frame, text='Hash Result2')
        self.hash_out_text2 = tk.Text(self.strcmp_frame, height=5, width=50)
        self.hash_out_text2.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label2.grid(row=5, column=0)
        self.hash_out_text2.grid(row=5, column=1, columnspan=2)

        self.match_result = tk.Label(self.strcmp_frame, text='', fg='blue')
        self.match_result.grid(row=6, column=0, columnspan=3)

        self.back_button = tk.Button(self.strcmp_frame, text='Back', command=self.back_to_main)
        self.back_button.grid(row=7, column=0, columnspan=3)

        self.strcmp_frame.pack()

    def do_hash_cmp(self):
        msg1 = self.strcmp_input1.get()
        msg2 = self.strcmp_input2.get()
        print(msg1)
        print(msg2)
        hash_func = self.hash_func.get()
        if hash_func == 0:
            hash_func = 'md5'
        else:
            hash_func = 'sha3'
        print(hash_func)
        checker1 = Checker(msg1, hash_func, is_file=False)
        checker2 = Checker(msg2, hash_func, is_file=False)
        print(hash_func, 'hash of', msg1, 'is', checker1.get_hash())
        print(hash_func, 'hash of', msg2, 'is', checker2.get_hash())

        self.hash_out_text1.config(state=tk.NORMAL)
        self.hash_out_text1.delete(0.0, tk.END)
        self.hash_out_text1.insert(tk.END, checker1.get_hash())
        self.hash_out_text1.config(state=tk.DISABLED)

        self.hash_out_text2.config(state=tk.NORMAL)
        self.hash_out_text2.delete(0.0, tk.END)
        self.hash_out_text2.insert(tk.END, checker2.get_hash())
        self.hash_out_text2.config(state=tk.DISABLED)

        if checker1.get_hash() == checker2.get_hash():
            self.match_result.config(text='Match!')
        else:
            self.match_result.config(text='Not the same string!')

    def file_selection1(self):
        file_want = fd.askopenfile()
        file_path = file_want.name
        print(file_path)
        self.filecmp_input1.delete(0, tk.END)
        self.filecmp_input1.insert(tk.END, file_path)
        file_want.close()
        self.filecmp_input1.config(text=file_path)

    def file_selection2(self):
        file_want = fd.askopenfile()
        file_path = file_want.name
        print(file_path)
        self.filecmp_input2.delete(0, tk.END)
        self.filecmp_input2.insert(tk.END, file_path)
        file_want.close()
        self.filecmp_input2.config(text=file_path)

    def jump_file_compare(self):
        self.filecmp_frame = tk.Frame(self)
        self.filecmp_subframe1 = tk.Frame(self.filecmp_frame)
        self.filecmp_label1 = tk.Label(self.filecmp_subframe1, text='Input file1')
        self.filecmp_input1 = tk.Entry(self.filecmp_subframe1, width=58)
        self.file_choose_btn1 = tk.Button(self.filecmp_subframe1, text='Select File1', command=self.file_selection1)

        self.filecmp_label1.grid(row=0, column=0, sticky=tk.W)
        self.filecmp_input1.grid(row=0, column=1, sticky=tk.W)
        self.file_choose_btn1.grid(row=0, column=2, sticky=tk.W)
        self.filecmp_subframe1.grid(row=0, column=0, columnspan=3, sticky=tk.W)

        self.filecmp_subframe2 = tk.Frame(self.filecmp_frame)
        self.filecmp_label2 = tk.Label(self.filecmp_subframe2, text='Input file2')
        self.filecmp_input2 = tk.Entry(self.filecmp_subframe2, width=58)
        self.file_choose_btn2 = tk.Button(self.filecmp_subframe2, text='Select File2', command=self.file_selection2)

        self.filecmp_label2.grid(row=0, column=0, sticky=tk.W)
        self.filecmp_input2.grid(row=0, column=1, sticky=tk.W)
        self.file_choose_btn2.grid(row=0, column=2, sticky=tk.W)
        self.filecmp_subframe2.grid(row=1, column=0, columnspan=3, sticky=tk.W)

        self.hash_func = tk.IntVar()

        self.hash_label = tk.Label(self.filecmp_frame, text='Hash Function')
        self.hash_frame = tk.Frame(self.filecmp_frame)
        self.md5_rb = tk.Radiobutton(self.hash_frame, variable=self.hash_func, text='md5', value=0)
        self.sha3_rb = tk.Radiobutton(self.hash_frame, variable=self.hash_func, text='sha3', value=1)
        self.hash_label.grid(row=2, column=0, sticky=tk.W)
        self.md5_rb.grid(row=0, column=0, sticky=tk.W)
        self.sha3_rb.grid(row=0, column=1, sticky=tk.W)
        self.hash_frame.grid(row=2, column=1, sticky=tk.W)

        self.file_button = tk.Button(self.filecmp_frame, text='Compare!', command=self.do_file_hash_cmp)
        self.file_button.grid(row=3, columnspan=3)

        self.hash_out_label1 = tk.Label(self.filecmp_frame, text='Hash Result')
        self.hash_out_text1 = tk.Text(self.filecmp_frame, height=3, width=87)
        self.hash_out_text1.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label1.grid(row=4, column=0)
        self.hash_out_text1.grid(row=4, column=1, columnspan=2)

        self.hash_out_label2 = tk.Label(self.filecmp_frame, text='Hash Result')
        self.hash_out_text2 = tk.Text(self.filecmp_frame, height=3, width=87)
        self.hash_out_text2.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label2.grid(row=5, column=0)
        self.hash_out_text2.grid(row=5, column=1, columnspan=2)

        self.match_result = tk.Label(self.filecmp_frame, text='', fg='blue')
        self.match_result.grid(row=6, column=0, columnspan=3)

        self.back_button = tk.Button(self.filecmp_frame, text='Back', command=self.back_to_main)
        self.back_button.grid(row=7, column=0, columnspan=3)

        self.filecmp_frame.pack()

    def do_file_hash_cmp(self):
        try:
            self.warning_window1.destroy()
        except Exception:
            pass
        self.hash_out_text1.config(state=tk.NORMAL)
        self.hash_out_text1.delete(0.0, tk.END)
        try:
            file_path = self.filecmp_input1.get()
            print(file_path)
            try_f = open(file_path, 'r')
            try_f.close()
            hash_func = self.hash_func.get()
            if hash_func == 0:
                hash_func = 'md5'
            else:
                hash_func = 'sha3'
            print(hash_func)
            checker1 = Checker(file_path, hash_func, is_file=True)
            print(hash_func, 'hash of', file_path, 'is', checker1.get_hash())
            self.hash_out_text1.insert(tk.END, checker1.get_hash())
            self.hash_out_text1.config(state=tk.DISABLED)
        except Exception:
            print('No such file!')
            self.warning_window1 = tk.Frame(self)
            self.warning_msg1 = tk.Label(self.warning_window1, fg='red',
                                        text='No such file1!\nPlease re-input your file1 path!')
            self.warning_btn1 = tk.Button(self.warning_window1, text='Understand', command=self.warning_process1)
            self.warning_msg1.pack()
            self.warning_btn1.pack()
            self.warning_window1.pack()
            self.hash_out_text1.config(state=tk.DISABLED)

        try:
            self.warning_window2.destroy()
        except Exception:
            pass
        self.hash_out_text2.config(state=tk.NORMAL)
        self.hash_out_text2.delete(0.0, tk.END)
        try:
            file_path = self.filecmp_input2.get()
            print(file_path)
            try_f = open(file_path, 'r')
            try_f.close()
            hash_func = self.hash_func.get()
            if hash_func == 0:
                hash_func = 'md5'
            else:
                hash_func = 'sha3'
            print(hash_func)
            checker2 = Checker(file_path, hash_func, is_file=True)
            print(hash_func, 'hash of', file_path, 'is', checker2.get_hash())
            self.hash_out_text2.insert(tk.END, checker2.get_hash())
            self.hash_out_text2.config(state=tk.DISABLED)
        except Exception:
            print('No such file!')
            self.warning_window2 = tk.Frame(self)
            self.warning_msg2 = tk.Label(self.warning_window2, fg='red',
                                        text='No such file2!\nPlease re-input your file2 path!')
            self.warning_btn2 = tk.Button(self.warning_window2, text='Understand', command=self.warning_process2)
            self.warning_msg2.pack()
            self.warning_btn2.pack()
            self.warning_window2.pack()
            self.hash_out_text2.config(state=tk.DISABLED)

        if checker1.get_hash() == checker2.get_hash():
            self.match_result.config(text='Match!')
        else:
            self.match_result.config(text='Not the same string!')


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
