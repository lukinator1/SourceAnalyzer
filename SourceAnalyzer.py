import os
import tkinter as tk
from tkinter import filedialog as fd
from Winnowing import compare_files, get_common_fingerprints

file1 = ''
file2 = ''

root = tk.Tk()
root.geometry("720x480")
root.title("Source Analyzer")

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

        res = compare_files(file1, file2, kint, wint)
        fp = get_common_fingerprints(file1, file2, kint, wint)

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

klabel = tk.Label(topFrame, text = "Input k value: ")
klabel.grid(row = 2, column = 0, padx = 1, pady = 5)

kinput = tk.Entry(topFrame)
kinput.grid(row = 2, column = 1 , padx = 1, pady = 5)
try:
   kint = tk.IntVar()
   kint = int(kinput.get())
except ValueError:
   kint = 5

wlabel = tk.Label(topFrame, text = "Input w value: ")
wlabel.grid(row = 2, column = 2 , padx = 1, pady = 5)

winput = tk.Entry(topFrame)
winput.grid(row = 2, column = 3, padx = 1, pady = 5)

try:
   wint = tk.IntVar()
   wint = int(winput.get())
except ValueError:
   wint = 4

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

