import sys
sys.path.append('../')
from tkinter import filedialog as fd
from source.backend.interface import *
import os
import tkinter as tk



def remove_spaces(str_remove):
    before = len(str_remove)
    str_remove = str_remove.replace(' ', '')
    str_remove = str_remove.replace('\t', '')
    str_remove = str_remove.replace('\n', '')
    after = len(str_remove)

    spaces_removed = before - after

    return str_remove, spaces_removed


class SourceAnalyzer:

    def open_file1(self):
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py")))
        # print(files)
        self.files1 = files
        for file in files:
            self.file_name1.insert(tk.END, file)

    def clear_file1(self):
        self.file1 = []
        self.file_name1.delete(0, tk.END)

    def open_file2(self):
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py")))
        # print(files)
        self.files2 = files
        for file in files:
            self.file_name2.insert(tk.END, file)

    def clear_file2(self):
        self.file2 = []
        self.file_name2.delete(0, tk.END)

    def export_files(self):
        if self.file_name1.curselection() and self.file_name2.curselection():

            self.clear_output()

            file1 = self.file_name1.get(self.file_name1.curselection()[0])
            file2 = self.file_name2.get(self.file_name2.curselection()[0])

            k = int(self.k_input.get())
            w = int(self.windowSizeInput.get())

            file1out = open(file1, 'r').read()
            file2out = open(file2, 'r').read()

            #Python
            if self.language_var.get() == "Python":
                res, num_common_fps = compare_files_py(file1, file2, k, w)
                fp = get_fps_py(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()))
            #Text
            else:
                res, num_common_fps = compare_files_txt(file1, file2, k, w)
                fp = get_fps_txt(file1, file2, k, w, num_common_fps, int(self.ignore_input.get()))

            
            self.out_result.configure(state='normal')
            self.out_text1.configure(state='normal')
            self.out_text2.configure(state='normal')

            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "File A is " + str(round(res, 2)) + "% similar to File B.\n" + str(len(fp)) + " fingerprints.")
            if self.language_var.get() == "Python":
                if file1[(len(file1) - 4):] == '.txt' or file2[(len(file2) - 4):] == '.txt':
                    self.out_result.insert(tk.END, " WARNING: Used 'Python' analyzer on .txt files. Results will be inaccurate!")

            self.out_text1.tag_config("match", background='yellow')
            self.out_text2.tag_config("match", background='yellow')
            self.out_text1.tag_config("found")
            self.out_text2.tag_config("found")
            self.out_text1.delete('1.0', tk.END)
            self.out_text2.delete('1.0', tk.END)
            self.out_text1.insert(tk.END, file1out)
            self.out_text2.insert(tk.END, file2out)

            index_track1 = '1.0'

            for fingerprint in fp:

                index1 = []
                index2 = []

                len1 = []
                len2 = []

                index_track2 = '1.0'

                for i in range(len(fingerprint[0])):
                    index1.append(self.out_text1.search(fingerprint[0][i].substring, index_track1, tk.END, exact=False))
                    if index1[i] != '':
                        self.out_text1.tag_add("found", index1[i], str(index1[i]) + "+" + str(len(fingerprint[0][i].substring)) + "c")
                        len1.append(len(fingerprint[0][i].substring))
                    else:
                        index1.pop(i)

                for i in range(len(fingerprint[1])):
                    index2.append(self.out_text2.search(fingerprint[1][i].substring, index_track2, tk.END, exact=False))
                    if index2[i] != '':
                        self.out_text2.tag_add("found", index2[i], str(index2[i]) + "+" + str(len(fingerprint[1][i].substring)) + "c")
                        len2.append(len(fingerprint[1][i].substring))
                        index_track2 = index2[i]
                    else:
                        index2.pop(i)              

                if len(index1) > 0:
                    index_track1 = index1[0]
    
                    
                self.index1s.append((index1, len1))
                self.index2s.append((index2, len2))

            self.out_result.configure(state='disabled')
            self.out_text1.configure(state='disabled')
            self.out_text2.configure(state='disabled')

            self.fp = fp

            print(len(self.index1s))
            print(len(self.index2s))

            self.max_fp = len(self.fp)
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

            self.show_fp()


        else:
            print("Please select two files to compare!")
            self.out_result.configure(state='normal')
            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "Please select two files to compare!")
            self.out_result.configure(state='disabled')

    def show_fp(self):

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        if self.view_var.get() == 1:
            
            for i in range(len(self.index1s)):
                for j in range(len(self.index1s[i][0])):
                    self.out_text1.tag_add("match", self.index1s[i][0][j], str(self.index1s[i][0][j]) + "+" + str(self.index1s[i][1][j]) + "c")
                for j in range(len(self.index2s[i][0])):
                    self.out_text2.tag_add("match", self.index2s[i][0][j], str(self.index2s[i][0][j]) + "+" + str(self.index2s[i][1][j]) + "c")

        else:
            self.out_text1.tag_remove("match", '1.0', tk.END)
            self.out_text2.tag_remove("match", '1.0', tk.END)
            if self.max_fp > 0:
                self.cur_fp = 1
                
                for i in range(len(self.index1s[0][0])):
                    self.out_text1.tag_add("match", self.index1s[0][0][i], str(self.index1s[0][0][i]) + "+" + str(self.index1s[0][1][i]) + "c")
                for i in range(len(self.index2s[0][0])):
                    self.out_text2.tag_add("match", self.index2s[0][0][i], str(self.index2s[0][0][i]) + "+" + str(self.index2s[0][1][i]) + "c")
                
            else:
                self.cur_fp = 0
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

    def next_fp(self):
        if self.view_var.get() == 0:
            if self.cur_fp < self.max_fp:
                self.out_text1.tag_remove("match", '1.0', tk.END)
                self.out_text2.tag_remove("match", '1.0', tk.END)

                for i in range(len(self.index1s[self.cur_fp][0])):
                    self.out_text1.tag_add("match", self.index1s[self.cur_fp][0][i], str(self.index1s[self.cur_fp][0][i]) + "+" + str(self.index1s[self.cur_fp][1][i]) + "c")
                for i in range(len(self.index2s[self.cur_fp][0])):
                    self.out_text2.tag_add("match", self.index2s[self.cur_fp][0][i], str(self.index2s[self.cur_fp][0][i]) + "+" + str(self.index2s[self.cur_fp][1][i]) + "c")

                #self.out_text1.see(self.index1s[self.cur_fp][0][0]  + "+" + str(self.index1s[self.cur_fp][1][0]) + "c")
                #self.out_text2.see(self.index2s[self.cur_fp][0][0] + "+" + str(self.index1s[self.cur_fp][1][0]) + "c")
                
                self.cur_fp = self.cur_fp + 1
                self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

    def last_fp(self):
        if self.view_var.get() == 0:
            if self.cur_fp > 1:
                self.out_text1.tag_remove("match", '1.0', tk.END)
                self.out_text2.tag_remove("match", '1.0', tk.END)

                for i in range(len(self.index1s[self.cur_fp - 2][0])):
                    self.out_text1.tag_add("match", self.index1s[self.cur_fp - 2][0][i], str(self.index1s[self.cur_fp - 2][0][i]) + "+" + str(self.index1s[self.cur_fp - 2][1][i]) + "c")
                for i in range(len(self.index2s[self.cur_fp - 2][0])):
                    self.out_text2.tag_add("match", self.index2s[self.cur_fp - 2][0][i], str(self.index2s[self.cur_fp - 2][0][i]) + "+" + str(self.index2s[self.cur_fp - 2][1][i]) + "c")

                #self.out_text1.see(self.index1s[self.cur_fp - 2][0][0])
                #self.out_text2.see(self.index2s[self.cur_fp - 2][0][0])
                
                self.cur_fp = self.cur_fp - 1
                self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)


    def clear_output(self):

        self.out_result.configure(state='normal')
        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        self.out_result.delete('1.0', tk.END)
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)

        self.out_result.configure(state='disabled')
        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        self.fp = []
        self.index1s = []
        self.index2s = []

    def mult_yview(self, *args):
        self.out_text1.yview(*args)
        self.out_text2.yview(*args)

    def donothing(self):
        x = 0

    def openHelp(self):
        helpSect = tk.Toplevel()
        helpSect.title("Source Analyzer Help Section")
        inputMessage = "Input descriptions of various parts of program here. Troubleshooting problems. Analysis of algorithms"
        tk.Label(helpSect, text=inputMessage).pack()
        tk.Button(helpSect, text="DONE", command=helpSect.destroy).pack()

    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        self.files1 = []
        self.files2 = []

        self.cur_fp = 0
        self.max_fp = 0
        self.fp = []
        self.index1s = []
        self.index2s = []

        self.menubar = tk.Menu(self.master)
        
        self.upper = tk.Frame(self.master)
        self.upper.pack(side = "top", fill='both', pady=5, padx=5)

        self.top_frame = tk.Frame(self.upper)
        self.top_frame.pack(expand=True, side = "left", fill='both', pady=5)

        self.button_panel = tk.Frame(self.upper)
        self.button_panel.pack(side="right", fill='x', padx=10, pady=5)

        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack(expand=True, fill='both', pady=5, side='bottom')

        self.bottom_frame = tk.Frame(self.output_frame)
        self.bottom_frame.pack(expand=True, fill='both', pady=5)

        self.very_bottom = tk.Frame(self.output_frame, width=0)
        self.very_bottom.pack(expand=False, fill='none', padx=(0, 125), pady=5, side="bottom")

    #Menubar - Currently Non-Functional

        #self.filemenu = tk.Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="New Window", command=self.donothing) #newWindow
        ##self.filemenu.add_command(label="Save Settings", command=self.donothing)
        #self.filemenu.add_separator()
        #self.filemenu.add_command(label="Exit", command=self.master.quit)
        #self.menubar.add_cascade(label="File", menu=self.filemenu)

        #self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        #self.toolsmenu.add_command(label="Check Matches", command=self.donothing)
        #self.toolsmenu.add_command(label="Fingerprint Offest", command=self.donothing)
        #self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        #self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        #self.helpmenu.add_command(label="Open Help", command= self.openHelp)
        #self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        #self.master.config(menu=self.menubar) 
          
    #Filename Display

        self.file1_frame = tk.Frame(self.top_frame)
        self.file1_frame.pack(side='top', expand=True, fill='both')

        self.file2_frame = tk.Frame(self.top_frame)
        self.file2_frame.pack(side='bottom', expand=True, fill='both')

        #Filebox 1

        self.cur_file_label1 = tk.Label(self.file1_frame, text = "Click to select File A: ")
        self.cur_file_label1.pack(anchor='w')
        self.cur_file_label1.config(font=(None, 9))

        self.file_name1 = tk.Listbox(self.file1_frame, height=5, exportselection=False)

        self.file_scroll1 = tk.Scrollbar(self.file1_frame, command=self.file_name1.yview)
        self.file_name1['yscrollcommand'] = self.file_scroll1.set
        self.file_scroll1.pack(expand=False, fill="y", side='right')

        self.file_name1.pack(expand=True, pady=(0, 10), fill='both')

        #Filebox 2

        self.cur_file_label2 = tk.Label(self.file2_frame, text = "Click to select File B: ")
        self.cur_file_label2.pack(anchor='w')
        self.cur_file_label2.config(font=(None, 9))

        self.file_name2 = tk.Listbox(self.file2_frame, height=5, exportselection=False)

        self.file_scroll2 = tk.Scrollbar(self.file2_frame, command=self.file_name2.yview)
        self.file_name2['yscrollcommand'] = self.file_scroll2.set
        self.file_scroll2.pack(expand=False, fill="y", side='right')

        self.file_name2.pack(expand=True, fill='both')

    #Button Panel

        #File Selection

        #self.filter_label = tk.Label(self.button_panel, text = "Added File Filter: ")
        #self.filter_label.grid(row=0, column=0)
        #self.filter_label.config(font=(None, 9))

        #self.file_filter = tk.Text(self.button_panel, height=1, width=30, state='disabled')
        #self.file_filter.grid(row=0, column=1, columnspan=4)

        self.k_desc_label = tk.Label(self.button_panel, text = "K (noise threshold) impacts sensitivity. Fingerprints size < k will be ignored.\nWindow Size is the winnow size used by the algorithm.\nIgnore Count determines fingerprint threshold for commonality.\nPython files should be able to be compiled for the best results.")
        self.k_desc_label.grid(row=0, column=0, columnspan=4)
        self.k_desc_label.config(font=(None, 8))

        self.w_desc_label = tk.Label(self.button_panel, text = "All values may be left at default.")
        self.w_desc_label.grid(row=1, column=0, columnspan=4)
        self.w_desc_label.config(font=(None, 8))

        #self.ignore_label = tk.Label(self.button_panel, text = "Ignore Files: ")
        #self.ignore_label.grid(row=1, column=0)
        #self.ignore_label.config(font=(None, 9))

        #self.file_ignore = tk.Text(self.button_panel, height=1, width=30, state='disabled')
        #self.file_ignore.grid(row=1, column=1, columnspan=4)

        self.button1 = tk.Button(self.button_panel, text="Add File A", command=self.open_file1, bg="gray75", width=15)
        self.button1.grid(row = 2, column = 0, padx = 1, pady = 5, columnspan=2)

        self.button1a = tk.Button(self.button_panel, text="Clear File A(s)", command=self.clear_file1, bg="gray80", width=15)
        self.button1a.grid(row = 2, column = 2, padx = 1, pady = 5, columnspan=2)

        self.button2 = tk.Button(self.button_panel, text="Add File B", command=self.open_file2, bg="gray75", width=15)
        self.button2.grid(row = 3, column = 0, padx =1, pady = 2, columnspan=2)

        self.button2a = tk.Button(self.button_panel, text="Clear File B(s)", command=self.clear_file2, bg="gray80", width=15)
        self.button2a.grid(row = 3, column = 2, padx = 1, pady = 2, columnspan=2)

        #Commands

        self.lang_label = tk.Label(self.button_panel, text = "Language: ")
        self.lang_label.grid(row = 4, column = 0, pady = 10)
        self.lang_label.config(font=(None, 9))

        self.language_var = tk.StringVar(self.button_panel)
        self.language_var.set("Python")
        self.languageMenu = tk.OptionMenu(self.button_panel, self.language_var, "Text", "Python")
        self.languageMenu.grid(row=4, column=1, pady=10, sticky='w', columnspan=2)

        self.ignore_count_label = tk.Label(self.button_panel, text = "Ignore Count: ")
        self.ignore_count_label.grid(row = 4, column = 2, pady = 10)
        self.ignore_count_label.config(font=(None, 9))

        self.ignore_input = tk.Spinbox(self.button_panel, from_=0, to=255, width=5)
        self.ignore_input.grid(row=4, column=3, pady=10)
        self.ignore_input.delete(0, tk.END)
        self.ignore_input.insert(0, '5')

        #Advanced

        self.k_label = tk.Label(self.button_panel, text = "K-grams: ")
        self.k_label.grid(row = 6, column = 0, padx = 1, pady = (10,0))
        self.k_label.config(font=(None, 9))

        self.k_input = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.k_input.grid(row=6, column=1, padx=5, pady = (10,0))

        self.k_input.delete(0, tk.END)
        self.k_input.insert(0, '10')

        self.w_label = tk.Label(self.button_panel, text = "Window Size: ")
        self.w_label.grid(row = 6, column = 2, padx = 1, pady = (10,0))
        self.w_label.config(font=(None, 9))

        self.windowSizeInput = tk.Spinbox(self.button_panel, from_=1, to=255, width=5)
        self.windowSizeInput.grid(row=6, column=3, padx=5, pady = (10,0))

        self.windowSizeInput.delete(0, tk.END)
        self.windowSizeInput.insert(0, '5')

        #Compare

        self.run_label = tk.Button(self.button_panel, text="Compare", height = 1, width = 40, command=self.export_files, bg="gray75", bd=3)
        self.run_label.grid(row=8, column=0, pady=(20, 0), columnspan=4)

        self.clear_label = tk.Button(self.button_panel, text="Clear Output", height = 1, width = 40, command=self.clear_output, bg="gray80", bd=3)
        self.clear_label.grid(row=9, column=0, pady=2.5, columnspan=4)

    #Bottom Frame

        self.output_lbl = tk.Label(self.bottom_frame, text = "Output")
        self.output_lbl.pack()

        self.out_result = tk.Text(self.bottom_frame, width=1, height=2)
        self.out_result.pack(fill="x", side='top', padx=10, pady=5)
        self.out_result.configure(state='disabled')

        self.out_text1 = tk.Text(self.bottom_frame, width=1, height=1, )
        self.out_text1.configure(state='disabled')

        self.txt_scroll1 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text1['yscrollcommand'] = self.txt_scroll1.set

        self.out_text1.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll1.pack(side='left', padx=(0,10), fill='y', pady=10)

        self.out_text2 = tk.Text(self.bottom_frame, width=1, height=1, )
        self.out_text2.configure(state='disabled')

        self.txt_scroll2 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text2['yscrollcommand'] = self.txt_scroll2.set

        self.out_text2.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll2.pack(side='left', padx=(0,10), fill='y', pady=10)

    #Very Bottom
        
        self.view_label = tk.Label(self.very_bottom, text="View All?")
        self.view_label.grid(row=0, column=0, padx=(20,5), pady=5)

        self.view_var = tk.IntVar()

        self.view_all = tk.Checkbutton(self.very_bottom, command=self.show_fp, variable=self.view_var)
        self.view_all.grid(row=0, column=1, padx=5, pady=5)

        self.last_fp = tk.Button(self.very_bottom, text="Last Fingerprint", command=self.last_fp)
        self.last_fp.grid(row=0, column=2, padx=5, pady=5)

        self.current_fp = tk.Label(self.very_bottom, text="Current: " + str(self.cur_fp) + "/" + str(self.max_fp))
        self.current_fp.grid(row=0, column=3, padx=5, pady=5)

        self.next_fp = tk.Button(self.very_bottom, text="Next Fingerprint", command=self.next_fp)
        self.next_fp.grid(row=0, column=4, padx=5, pady=5)


def main():
    root = tk.Tk()
    root.geometry("1080x720")
    root.title("Source Analyzer")
    gui = SourceAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

