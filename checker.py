from md5 import Md5Checker
from sha3 import Sha3Checker
import tkinter as tk
import tkinter.filedialog as fd
import bitstring


class Checker:
    def __init__(self, msg, algo, is_file=False):
        if is_file:
            msg = bitstring.BitArray(open(msg, 'rb').read()).int
            self.byte_stream = msg
            print('Msg:')
            print(bin(msg))
            print(hex(msg))
            print()
            if algo == 'md5':
                self.checker = Md5Checker(self.byte_stream)
            elif algo == 'sha3':
                self.checker = Sha3Checker(self.byte_stream)
        else:
            if msg == '':
                msg = 0
            else:
                msg = eval('0x' + bytes(msg.encode()).hex())
            self.byte_stream = msg
            print('Msg:')
            print(bin(msg))
            print(hex(msg))
            print()
            if algo == 'md5':
                self.checker = Md5Checker(self.byte_stream)
            elif algo == 'sha3':
                self.checker = Sha3Checker(self.byte_stream)

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
        self.string_rb.grid(row=0, column=0, sticky=tk.W)
        self.file_rb.grid(row=1, column=0, sticky=tk.W)
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
        self.hash_out_text = tk.Text(self.string_frame, height=1, width=50)
        self.hash_out_text.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label.grid(row=3, column=0)
        self.hash_out_text.grid(row=3, column=1, columnspan=2)
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
        checker = Checker(msg, hash_func)
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
        self.file_input = tk.Entry(self.file_frame)
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
        self.hash_out_text = tk.Text(self.file_frame, height=1, width=87)
        self.hash_out_text.config(highlightbackground='#80C0FF', state=tk.DISABLED)
        self.hash_out_label.grid(row=3, column=0)
        self.hash_out_text.grid(row=3, column=1, columnspan=2)
        self.file_frame.pack()

    def warning_process(self):
        self.warning_window.destroy()
        self.file_input.delete(0, tk.END)

    def do_file_hash(self):
        try:
            self.warning_window.destroy()
        except Exception:
            pass
        self.hash_out_text.delete(0.0, tk.END)
        self.hash_out_text.config(state=tk.NORMAL)
        try:
            file_path = self.file_input.get()
            print(file_path)
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
        except Exception:
            print('No such file!')
            self.warning_window = tk.Frame(self)
            self.warning_msg = tk.Label(self.warning_window, fg='red', text='No such file!\nPlease re-input your file path!')
            self.warning_btn = tk.Button(self.warning_window, text='Understand', command=self.warning_process)
            self.warning_msg.pack()
            self.warning_btn.pack()
            self.warning_window.pack()
            self.hash_out_text.config(state=tk.DISABLED)


def say_hi(self):
    print("hi there, everyone!")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    '''
    root = Tk()

    string_input = Entry(root)
    string_input.pack()
    f1 = Frame(root)

    a1 = Radiobutton(f1, text="one", value=1)
    a2 = Radiobutton(f1, text="two", value=2)
    a3 = Radiobutton(f1, text="three", value=3)
    a1.grid(row=0, column=0)
    a2.grid(row=0, column=1)
    a3.grid(row=0, column=2)
    f1.pack()
    root.mainloop()
    '''
