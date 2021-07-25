import sys
import random
from time import sleep
import math

#----------------------------------------------------------------------

# Line Pointer
lp = 0

# Registers
a = 0
x = 0
y = 0

# Ram
ram = [0] * 16

# Labels
lbls = {}

# Sub routines
inSR = False
sr = {}
recentLine = 0

# ERAM
eram = []

#---------------------------------------------------------------------

def push(s):
    global eram, x, y, ram, lp

    if s.isdigit():
        eram.append(int(s))

    elif s == 'a':
        eram.append(a)

    elif s =='x':
        eram.append(x)
    
    elif s =='y':
        eram.append(y)

    else:
        print(f"Invalid argument for push at line {lp + 1} ...")
        lp = len(code)


def _del(i):
    global eram, lp
    try:
        del eram[int(i)]
    except:
        print(f"Invalid argument for del command(argument shoud be int) on line {lp + 1} ...")
        lp = len(code)

#---------------------------------------------------------------------

def filer(n):
    global eram, lp

    if n[0] == '"' and n[-1] == '"':
        f = open(n[1:-1])
        for c in f.read():
            eram.append(ord(c))
    else:
        print(f"File name should be enclosed in \" on line {lp + 1}")
        lp = len(code)


#---------------------------------------------------------------------

def fwrite(s):
    global x, lp

    try:
        s = s.split(', ')
        if s[0][0] == '"' and s[0][-1] == '"' and s[1][0] == '"' and s[1][-1] == '"':
            f = open(s[0][1:-1], 'a')
            f.write(s[1][1:-1])
        if s[0][0] == '"' and s[0][-1] == '"' and s[1] == 'x':
            f = open(s[0][1:-1], 'a')
            f.write(chr(x))
    except FileNotFoundError:
        print(f"File {s[0][1:-1]} not found online {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def ifjsr(s):
    global sr, lp, inSR, recentLine, a

    if a:
        recentLine = lp
        try:
            lp = sr[s]
        except:
            print(f"{s} is not a subroutine on line {lp + 1}")
            lp = len(code)
        inSR = True

#---------------------------------------------------------------------

def fwln(s):
    global lp
    if s[0] == '"' and s[-1] == '"':
        f = open(s[1:-1], 'a')
        f.writelines('\n')
    else:
        print(f"File name should be enclosed in \" on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def fclr(s):
    global lp
    if s[0] == '"' and s[-1] == '"':
        f = open(s[1:-1], 'w')
        f.writelines('')
    else:
        print(f"File name should be enclosed in \" on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def out(s):
    global x, y, ram, lp, a

    STRINGTOKEN = '"'

    if s[0] == STRINGTOKEN and s[-1] == STRINGTOKEN:
        print(s[1:-1])

    elif s.isdigit():
        print(s)

    elif s == 'x':
        print(x)

    elif s == 'y':
        print(y)

    elif s == 'a':
        print(a)

    elif s == '##':
        print(ram)

    elif '#' in s:
        if s != '##':
            index = int(s[1:])
            print(ram[index])

    elif s == '$$':
        print(eram)

    elif '$' in s:
        if s != '$$':
            if s == '$x':
                print(eram[x])
            else:
                index = int(s[1:])
                print(eram[index])

    else:
        print(f"Invalid Argument for 'out' on line {lp + 1}...")
        lp = len(code)

#---------------------------------------------------------------------

# Load X
def ldx(val):
    global x, lp, ram, eram

    if val.isdigit():
        x = abs(int(val))

    elif val == 'lp':
        x = lp

    elif '#' in val:
        index = int(val[1:])
        x = ram[index]
        ram[index] = 0

    elif '$' in val:
        if val != '$$':
            index = int(val[1:])
            x = eram[index]
            del eram[index]

    else:
        print(f"Invaild Load Argument for 'ldx' on line {lp + 1}...")
        lp = len(code)

#---------------------------------------------------------------------

# Load Y
def ldy(val):
    global y, lp, ram

    if val.isdigit():
        y = abs(int(val))

    elif '#' in val:
        index = int(val[1:])
        y = ram[index]
        ram[index] = 0

    else:
        print(f"Invaild Load Argument for 'ldy' on line {lp + 1}...")
        lp = len(code)

#---------------------------------------------------------------------

def sta(ramBank):
    global a, ram, lp

    if '#' in ramBank:
        index = int(ramBank[1:])
        ram[index] = a
        a = 0
    else:
        print(f"Invalid argument (ram banks are mentioned like this -> #0) on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def _in():
    global x

    char = ord(input()[0])
    x = char

#---------------------------------------------------------------------

def createLabel(name):
    global lbls, lp

    lbls[name] = lp

#---------------------------------------------------------------------

def stx(ramBank):
    global x, ram, lp

    if '#' in ramBank:
        index = int(ramBank[1:])
        ram[index] = x
        x = 0
    else:
        print(f"Invalid argument (ram banks are mentioned like this -> #0) on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def sty(ramBank):
    global y, ram, lp

    if '#' in ramBank:
        index = int(ramBank[1:])
        ram[index] = y
        y = 0
    else:
        print(f"Invalid argument (ram banks are mentioned like this -> #0) on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def aout(s):
    global x, a, y, lp

    if s == 'x':
        print(chr(x), end="")

    elif s == 'y':
        print(chr(y), end="")

    elif s == 'a':
        print(chr(a), end="")

    elif s.isdigit():
        num = int(s)
        print(chr(num), end="")
    else:
        print(f"Invalid argument for aout on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

def max_():
    global a, x

    x = a
    a = 0

#---------------------------------------------------------------------

def may():
    global a, y

    y = a
    a = 0

#---------------------------------------------------------------------

def rnd():
    global a

    _min = 0
    _max = 255

    a = random.randint(_min, _max)

#---------------------------------------------------------------------

def sxy():
    global x, y

    temp = x
    x = y
    y = temp

#---------------------------------------------------------------------

def debug():
    global x, y, a, ram, lp, lbls, inSR, sr, recentLine
    print('a:', a)
    print('x:', x)
    print('y:', y)
    print('lp:', lp + 1)
    print('ram:', ram)
    print('Labels: ', lbls)
    print('SR: ', sr)
    print('Recent Line: ', recentLine)
    print('In SR: ', inSR)
    print('ERAM: ', eram)

#---------------------------------------------------------------------

def inc():
    global x
    x += 1

#---------------------------------------------------------------------

def dec():
    global x
    x -= 1

#--------------------------------------------------------------------

def add():
    global x, y, a
    a = x + y

#--------------------------------------------------------------------

def sub():
    global x, y, a
    a = x - y

#--------------------------------------------------------------------

def mul():
    global x, y, a
    a = x * y

#--------------------------------------------------------------------

def div():
    global x, y, a
    a = x / y

#--------------------------------------------------------------------

def _pow():
    global x, y, a
    a = x ** y

#--------------------------------------------------------------------

def equ():
    global x, y, a
    a = x == y

#--------------------------------------------------------------------

def neq():
    global x, y, a
    a = x != y

#--------------------------------------------------------------------

def gtr():
    global x, y, a
    a = x > y

#--------------------------------------------------------------------

def lsr():
    global x, y, a
    a = x < y

#--------------------------------------------------------------------

def gtreq():
    global x, y, a
    a = x >= y

#--------------------------------------------------------------------

def lsreq():
    global x, y, a
    a = x <= y

#--------------------------------------------------------------------

def ifgt(s):
    global lp, a

    try:
        if a:
            index = int(s) - 2
            lp = index
    except:
        print(f'Invalid argument for ifgt on line {lp + 1}')
        lp = len(code)

#---------------------------------------------------------------------

def addSR(s):
    global sr, lp

    sr[s] = lp

def jsr(n):
    global sr, lp, inSR, recentLine
    recentLine = lp
    try:
        lp = sr[n]
    except:
        print(f"Sub routine not defined, ERROR on linee {lp + 1}")
        lp = len(code)
    inSR = True

def ret():
    global lp, recentLine, inSR
    if inSR:
        inSR = False
        lp = recentLine
        recentLine = 0
    else:
        print(f'Unexcepted ret on line {lp + 1}')
        lp = len(code)

#---------------------------------------------------------------------

def sin():
    global x, a
    a = math.sin(x)

def cos():
    global x, a
    a = math.cos(x)

def tan():
    global x, a
    a = math.tan(x)

#---------------------------------------------------------------------

def dex(s):
    global x, lp
    try:
        x = float(s)
    except:
        print(f"{s} is not a proper float (ex: 3.1415926) on line {lp + 1}")
        lp = len(code)

#---------------------------------------------------------------------

# Run the code
def run(code):
    global lp

    try:

        while lp < len(code):
            line = code[lp]

            if line[:3] == 'out':
                out(line[4:])

            elif line[:3] == 'sin':
                sin()

            elif line[:3] == 'dex':
                dex(line[4:])

            elif line[:3] == 'cos':
                cos()

            elif line[:3] == 'tan':
                tan()

            elif line[:4] == 'aout':
                aout(line[5:])

            elif line[:3] == 'ldx':
                ldx(line[4:])

            elif line[:3] == 'ldy':
                ldy(line[4:])

            elif line[:3] == 'sta':
                sta(line[4:])

            elif line[:3] == 'stx':
                stx(line[4:])

            elif line[:3] == 'sty':
                sty(line[4:])

            elif line[:6] == 'fwrite':
                fwrite(line[7:])

            elif line == 'max':
                max_()

            elif line == 'rnd':
                rnd()

            elif line[:4] == 'fwln':
                fwln(line[5:])

            elif line[:4] == 'fclr':
                fclr(line[5:])

            elif line == 'may':
                may()

            elif line == 'sxy':
                sxy()

            elif line == 'inc':
                inc()

            elif line == 'dec':
                dec()

            elif line[:5] == 'filer':
                filer(line[6:][1:-1])

            elif line == 'debug':
                debug()

            elif line[:5] == 'ifjsr':
                ifjsr(line[6:])

            elif line == 'add':
                add()

            elif line == 'sub':
                sub()

            elif line == 'mul':
                mul()

            elif line == 'div':
                div()

            elif line == 'pow':
                _pow()

            elif line == 'equ':
                equ()

            elif line == 'neq':
                neq()

            elif line == 'gtr':
                gtr()

            elif line == 'lsr':
                lsr()

            elif line == 'gtreq':
                gtreq()

            elif line == 'lsreq':
                lsreq()

            elif line == 'in':
                _in()

            elif line[:4] == 'ifgt':
                ifgt(line[5:])

            elif line[:3] == 'jmp':
                for i in range(10):
                    k = str(i)
                    if k in line[4:]:
                        index = int(line[4:]) - 2
                        lp = index
                        break
                else:
                    index = lbls[line[4:]]
                    lp = index
            
            elif line[:3] == 'def':
                addSR(line[4:])
                flag = False
                i = 0
                while i < len(code):
                    if code[i] == line:
                        flag = True

                    if flag and code[i] == 'ret':
                        lp = i + 1
                    i += 1
                continue

            elif line[:3] == 'jsr':
                jsr(line[4:])

            elif line == 'ret':
                ret()

            elif line == '':
                lp += 1
                continue

            elif line[:3] == 'lbl':
                createLabel(line[4:])

            elif line[0] == ';':
                pass

            elif line[:4] == 'push':
                push(line[5:])

            elif line[:3] == 'del':
                _del(line[4:])

            elif line[:3] == 'slp':
                sleep(int(line[4:]))

            lp += 1
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    except:
        print(f"Unexecpted Error on line {lp + 1} ...")

#---------------------------------------------------------------------

if len(sys.argv) > 1:

    file = open(sys.argv[1])

    code = []

    for line in file.readlines():
        while line[0] == ' ' or line[0] == '\t':
            line = line[1:]
        code.append(line.rstrip())

    run(code)

else:
    print("File should be specified...")

#---------------------------------------------------------------------
