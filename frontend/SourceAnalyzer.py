import os
import tkinter as tk
from tkinter import filedialog as fd
from backend.interface import *


file1 = ''
file2 = ''

root = tk.Tk()
root.geometry("720x480")
root.title("Source Analyzer")

menubar = tk.Menu(root)
topFrame = tk.Frame(root)
topFrame.pack(side = "top", fill='x', pady=5)

def OpenFile1():
    file = fd.askopenfilename(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    global file1
    file1 = file
    print(file1)
    global fileName1
    fileName1["text"] = os.path.basename(file)

def OpenFile2():
    file = fd.askopenfilename(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    global file2
    file2 = file
    print(file2)
    global fileName2
    fileName2["text"] = os.path.basename(file)

def exportFiles():
    if file1 and file2:

        file1txt = open(file1, "r")
        file1out = file1txt.read()

        file2txt = open(file2, "r")
        file2out = file2txt.read()

        k = 10
        w = 5
        res, num_common_fps = compare_files_txt(file1, file2, k, w)
        fp = get_fps_txt(file1, file2, k, w, num_common_fps, 5)

        global out_text1
        global out_text2

        out_text1.tag_config("matchTrue", background='yellow')
        out_text2.tag_config("matchTrue", background='yellow')
        out_text1.tag_config("matchFalse", background='green')
        out_text2.tag_config("matchFalse", background='green')
        out_text1.insert(tk.END, file1out)
        out_text2.insert(tk.END, file2out)

        answer = True

        for fingerprint in fp:
            first, second = fp[fingerprint]
            out_text1.tag_add("match" + str(answer), "1.0+" + str(first[0]) + "c", "1.0+" + str(first[0] + 10) + "c")
            out_text2.tag_add("match" + str(answer), "1.0+" + str(second[0]) + "c", "1.0+" + str(second[0] + 10) + "c")
            answer = not answer


    else:
        print("Please select two files to compare!")

def mult_yview(*args):
    out_text1.yview(*args)
    out_text2.yview(*args)

def donothing():
   x = 0

"""
class newWindow():
    def __init__(self, master = None):  
        super().__init__(master = root) 
        self.title("Help Section") 
        self.geometry("200x200") 
        label = Label(self, text ="Input descriptions of various parts of program here.") 
        label.pack() 
"""

def openHelp():
    helpSect = tk.Toplevel()
    helpSect.title("Source Analyzer Help Section")
    inputMessage = "Input descriptions of various parts of program here. Troubleshooting problems. Analysis of algorithms"
    tk.Label(helpSect, text=inputMessage).pack()
    tk.Button(helpSect, text="DONE", command=helpSect.destroy).pack()


filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New Window", command=donothing) #newWindow
filemenu.add_command(label="Save Settings", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

toolsmenu = tk.Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Check Matches", command=donothing)
toolsmenu.add_command(label="Fingerprint Offest", command=donothing)
menubar.add_cascade(label="Tools", menu=toolsmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Open Help", command= openHelp)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

button1 = tk.Button(topFrame, text="Select File 1", command=OpenFile1, bg="gray75")
button1.grid(row = 0, column = 0, padx = 5, pady = 5)

curFileLabel1 = tk.Label(topFrame, text = "Current File 1: ")
curFileLabel1.grid(row = 0, column = 1, padx = 1, pady = 5)

fileName1 = tk.Label(topFrame, text="")
fileName1.grid(row = 0, column = 2, padx = 1, pady = 5, sticky="w")

button2 = tk.Button(topFrame, text="Select File 2", command=OpenFile2, bg="gray75")
button2.grid(row = 1, column = 0, padx = 5, pady = 5)

curFileLabel2 = tk.Label(topFrame, text = "Current File 2: ")
curFileLabel2.grid(row = 1, column = 1, padx = 1, pady = 5)

fileName2 = tk.Label(topFrame, text="")
fileName2.grid(row = 1, column = 2, padx = 1, pady = 5, sticky="w")

runQuery = tk.Button(root, text="Compare", height = 1, width = 50, command=exportFiles, bg="gray75", bd=5)
runQuery.pack(pady=(20,10))

bottom_frame = tk.Frame(root)
bottom_frame.pack(expand=True, fill='both', pady=5)

output_lbl = tk.Label(bottom_frame, text = "Output")
output_lbl.pack()

out_text1 = tk.Text(bottom_frame, width=1, height=1, )

txt_scroll1 = tk.Scrollbar(bottom_frame, command=mult_yview)
out_text1['yscrollcommand'] = txt_scroll1.set

out_text1.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
txt_scroll1.pack(side='left', padx=(0,10), fill='y', pady=10)


out_text2 = tk.Text(bottom_frame, width=1, height=1, )

txt_scroll2 = tk.Scrollbar(bottom_frame, command=mult_yview)
out_text2['yscrollcommand'] = txt_scroll2.set

out_text2.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
txt_scroll2.pack(side='left', padx=(0,10), fill='y', pady=10)



def main():
    root.mainloop()

if __name__ == "__main__":
    main()

