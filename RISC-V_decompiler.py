from tkinter import Tk
from tkinter.filedialog import askopenfilename
def convertFile():
    assemblyOut = ""
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    fi = open(filename, "r")
    fo = open(getOutFileName(filename, "output.txt"), "w+")
    hex_to_bin = {
        '0' : "0000",
        '1' : "0001",
        '2' : "0010",
        '3' : "0011",
        '4' : "0100",
        '5' : "0101",
        '6' : "0110",
        '7' : "0111",
        '8' : "1000",
        '9' : "1001",
        'a' : "1010",
        'b' : "1011",
        'c' : "1100",
        'd' : "1101",
        'e' : "1110",
        'f' : "1111",
    }
    lines = fi.readlines()

    for line in lines:
        outLine = ""
        for char in line:
            char = char.lower()
            binChar = hex_to_bin.get(char)
            if binChar is not None:
                outLine = outLine + binChar
        fo.write(outLine + "\n")
        print("Binary: " + outLine)
        assemblyOut += decompileBinaryToAssemblyRV32I(outLine) + "\n"
        print(decompileBinaryToAssemblyRV32I(outLine))
    fo.write("\n" + assemblyOut)

def getOutFileName(fileIn,fileName):
    fileIn = fileIn.split("/")
    # print(filename)
    fileIn = fileIn[:-1]
    fileIn = "/".join(fileIn)
    fileIn = fileIn + "/"
    return fileIn + fileName
def reg(location):
    return "x" + str(location)
def decompileBinaryToAssemblyRV32I(line):
    instruction = ""
    if len(line) != 32:
        print("invalid instruction")
    else:
        # [inclusive,exclusive]
        # [lesser,greater]
        line = list(line)
        opcode = ''.join(line[-7:])
        funct3 = ''.join(line[-15:-12])
        rs1 = ''.join(line[-20:-15])
        rs2 = ''.join(line[-25:-20])
        rd = ''.join(line[-12:-7])
        imm = ''.join(line[:-12]) #biggest imm value
        immL = ''.join(line[:-20]) #12 bit imm value, contiguous
        immb = ''.join(line[:-31] + line[-30:-24] + line[-11:-6] + line[-31:-30])
        imms = ''.join(line[:-25] + line[-12:-7])
        immi = immL
        shamt = rs2
        funct7 = ''.join(line[:-25])
        # print("opcode: " + opcode)
        # print("immb:" + immb)
        # print("")
        def LUI():
            return "LUI " + reg(int(rd,2)) + ", " + hex(int(imm,2))
        def AUIPC():
            return "AUIPC " + reg(int(rd,2)) + ", " + hex(int(imm,2))
        def JAL():
            return "JAL " + reg(int(rd,2)) + ", " + hex(int(imm,2))
        def JALR():
            return "JALR " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + hex(int(immL,2)) 
        def B():
            # check if the immb value is correct, unsure NOT correct
            if(int(funct3,2) == 0):
                return "BEQ " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
            if(int(funct3,2) == 1):
                return "BNE " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
            if(int(funct3,2) == 4):
                return "BLT " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
            if(int(funct3,2) == 5):
                return "BGE " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
            if(int(funct3,2) == 6):
                return "BLTU " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
            if(int(funct3,2) == 7):
                return "BGEU " + reg(int(rs1,2)) + ", " + reg(int(rs2,2)) + ", " + hex(int(immb,2))
        def L():
            if(int(funct3,2) == 0):
                return "LB " + reg(int(rd,2)) + ", " + hex(int(immL,2))+ "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 1):
                return "LH " + reg(int(rd,2)) + ", " + hex(int(immL,2))+ "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 2):
                return "LW " + reg(int(rd,2)) + ", " + hex(int(immL,2))+ "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 4):
                return "LBU " + reg(int(rd,2)) + ", " + hex(int(immL,2))+ "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 5):
                return "LHU " + reg(int(rd,2)) + ", " + hex(int(immL,2))+ "(" + reg(int(rs1,2)) + ")"
        def S():
            if(int(funct3,2) == 0):
                return "SB " + reg(int(rs2,2)) + ", " + hex(int(imms,2)) + "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 1):
                return "SH " + reg(int(rs2,2)) + ", " + hex(int(imms,2)) + "(" + reg(int(rs1,2)) + ")"
            if(int(funct3,2) == 2):
                print(imms)
                print(int(rs1,2))
                print(int(rs2,2))
                return "SW " + reg(int(rs2,2)) + ", " + hex(int(imms,2)) + "(" + reg(int(rs1,2)) + ")"
        def IMM():
            if(int(funct3,2) == 0):
                # print("rd:" + rd)
                # print("rs1:" + rs1)
                # print("immi:" + immi)
                return "ADDI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(immi,2))

            if(int(funct3,2) == 2):
                return "SLTI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(immi,2))
            if(int(funct3,2) == 3):
                return "SLTIU " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(immi,2))
            if(int(funct3,2) == 4):
                print()
                return "XORI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(immi,2))
            if(int(funct3,2) == 6):
                return "ORI " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", "+ hex(int(immi,2))
            if(int(funct3,2) == 7):
                return "ANDI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(immi,2))
            if(int(funct3,2) == 1):
                # uses shamt
                return "SLLI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(shamt,2))
            if(int(funct3,2) == 5):
                if(int(funct7,2) == 0):
                    # uses shamt
                    return "SRLI " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", "+ hex(int(shamt,2))
                else:
                    # uses shamt
                    return "SRAI " + reg(int(rd,2)) + ", " + reg(int(rs1,2))+ ", " + hex(int(shamt,2))
                    
        def OPERATORS():
            if(int(funct3,2) == 0):
                if(int(funct7 == 0)):
                    #add diff for add/sub
                    return "ADD " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
                else:
                    return "SUB " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            
            if(int(funct3,2) == 1):
                return "SLL " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 2):
                return "SLT " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 3):
                return "SLTU " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 4):
                return "XOR " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 1):
                # add comparison for SRL and SRA
                if(int(funct7,2) == 0):
                    return "SRL " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
                else:
                    return "SRA " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 6):
                return "OR " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
            if(int(funct3,2) == 7):
                return "AND " + reg(int(rd,2)) + ", " + reg(int(rs1,2)) + ", " + reg(int(rs2,2))
        switch = {
            55 : LUI,
            23 : AUIPC,
            111 : JAL,
            103 : JALR,
            99 : B,
            3 : L,
            35 : S,
            19 : IMM,
            51 : OPERATORS
        }
        func = switch.get(int(opcode,2))
        instruction = func()
    return instruction

if __name__ == "__main__":
    convertFile()
