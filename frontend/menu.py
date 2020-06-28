"""
from tkinter import *
from tkinter.ttk import *

def donothing():
   x = 0
   
root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
 

class HelpSection(Toplevel): 
      
    def __init__(self, root = None): 
          
        super().__init__(root = root) 
        self.title("Help Section") 
        self.geometry("200x200") 
        label = Label(self, text ="Input descriptions of various parts of program here.") 
        label.pack() 
  

def openHelp():
    helpSect = Toplevel()
    # display message
    inputMessage = "Input descriptions of various parts of program here."
    Label(helpSect, text=inputMessage).pack()
    # quit child window and return to root window
    # the button is optional here, simply use the corner x of the child window
    Button(helpSect, text="DONE", command=helpSect.destroy).pack()
    
# create root window
root = Tk()
# put a button on it, or a menu
Button(root, text='Bring up Message', command=openHelp).pack()
# start event-loop
root.mainloop()



# creates a Tk() object 
root = Tk() 
  
# sets the geometry of  
# main root window 
root.geometry("200x200") 
  
label = Label(root, text ="This is the main window") 
label.pack(side = TOP, pady = 10) 
  
# a button widget which will 
# open a new window on button click 
btn = Button(root,  
             text ="Click to open a new window") 
  
# Following line will bind click event 
# On any click left / right button 
# of mouse a new window will be opened 
btn.bind("<Button>",  
         lambda e: HelpSection(root)) 
  
btn.pack(pady = 10) 
  
# mainloop, runs infinitely 
mainloop()
"""