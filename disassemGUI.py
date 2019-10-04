from tkinter import Tk, Label, Button, Frame,Entry,Text, Scrollbar
import tkinter as tk
from tkinter.filedialog import askopenfilename
from rv32Idisassemble import convertFile, translateLines
class GUI_main:
    def __init__(self, master):
        self.master = master
        master.title("RV32I Disassembler")
        self.label = Label(master,text = "RV32I disassembler")
        self.label.pack()
        self.open_button = Button(master, text="Open File to Convert", command=self.openFileButtonClick)
        self.open_button.pack()

        self.convert_button = Button(master, text="CONVERT", command=self.convertButtonClick)
        self.convert_button.pack()


        self.text_add = Text(master,height = 20, width = 50)
        self.scroll_barA = Scrollbar(master)
        self.scroll_barA.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_add.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll_barA.config(command=self.text_add.yview)
        self.text_add.config(yscrollcommand=self.scroll_barA.set)


        self.text_result = Text(master,height = 20, width = 50)
        self.scroll_barR = Scrollbar(master)
        self.scroll_barR.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_result.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll_barR.config(command=self.text_result.yview)
        self.text_result.config(yscrollcommand=self.scroll_barR.set)

    def openFileButtonClick(self):
        filename = askopenfilename()
        file = open(filename)
        lines = "".join(file.readlines())
        self.text_add.insert(tk.END,lines)
        self.text_result.insert(tk.END, convertFile(filename))

    def convertButtonClick(self):
        lines = self.text_add.get(1.0,tk.END).strip().split("\n")
        
        self.text_result.insert(tk.END,translateLines(lines))



def openGUI():
    root = Tk()
    my_gui = GUI_main(root)
    root.mainloop()


    # filename = askopenfilename()
    # convertFile(filename)


if __name__ == "__main__":
    openGUI()

