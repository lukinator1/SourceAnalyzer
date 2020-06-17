import os
import tkinter as tk
from tkinter import filedialog as fd
from Winnowing import compare_documents

file1 = ''
file2 = ''

root = tk.Tk()
root.geometry("480x240")
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
        res = compare_documents(file1, file2)
        global out_text
        out_text.insert(tk.END, "\nThe documents have " + str(res) + " fingerprint(s) in common.")
    else:
        print("Please select two files to compare!")

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
runQuery.pack()

bottom_frame = tk.Frame(root)
bottom_frame.pack(side = "bottom", fill='x', pady=5)

output_lbl = tk.Label(bottom_frame, text = "Output")
output_lbl.grid(row=0,column=0,padx=1, sticky="w")

out_text = tk.Text(bottom_frame, height=4, width=57)
out_text.grid(row=1,column=0,padx=1,pady=1)
out_text.insert(tk.END, "Results: ")

def main():
    root.mainloop()

if __name__ == "__main__":
    main()

