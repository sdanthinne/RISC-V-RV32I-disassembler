from tkinter import Tk
from tkinter.filedialog import askopenfilename
from rv32Idisassemble import convertFile
class GUI_main:
    def __init__(self, master):
        self.master = master
        master.title("RV32I Disassembler")


def openGUI():
    root = Tk()
    my_gui = GUI_main(root)
    root.mainloop()


    filename = askopenfilename()
    convertFile(filename)
def openFileButtonClick():
    filename = askopenfilename()
    convertFile(filename)

def convertButtonClick():
    #in-GUI converter button
    pass  
if __name__ == "__main__":
    openGUI()

