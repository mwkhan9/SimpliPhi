from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import END, Label, filedialog, Text, Entry, PhotoImage, ttk
from PIL import Image, ImageTk
from fileClass import file
import ttg

root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
canvas = tk.Canvas(root, height = SCREEN_HEIGHT, width = SCREEN_WIDTH, bg = "#F6F1F1", highlightthickness=SCREEN_WIDTH/40, highlightbackground="#E1DAD8")
qFile = file("questions.txt")
questionList, typeList = qFile.importQuestions("questions.txt")


def init():
    global image, mainFrame, qNum, mode, correctText, incorrectText, TTButton, workingsButton, isQuestion

    qNum = 0
    mode = None
    isQuestion = False
    correctText = canvas.create_text(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.15), text = "", font = ('Helvetica','60'), fill = 'black')
    incorrectText = canvas.create_text(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.15), text = "", font = ('Helvetica','60'), fill = 'black')
    TTButton = tk.Button(root, text = "", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 250), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = userModeCommand)
    workingsButton = tk.Button(root, text = "", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 250), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = userModeCommand)
    
    topBanner = tk.Frame(root, bg = "black")
    topBanner.place(relwidth = 1, relheight = 0.1)

    image = Image.open("logo.png")
    image = image.resize((int(SCREEN_WIDTH / 6), int(SCREEN_HEIGHT / 12)))
    image = ImageTk.PhotoImage(image) 
    logo = Label(width = int(SCREEN_WIDTH / 6), height = int(SCREEN_HEIGHT / 10), image = image, borderwidth=0)
    logo.pack()

    topBannerBlue = tk.Frame(root, bg = "#19BDE6")
    topBannerBlue.tkraise(aboveThis=logo)
    topBannerBlue.place(relwidth = 1, relheight = 0.01)

    topBannerGrey = tk.Frame(root, bg = "#838B8B")
    topBannerGrey.place(relwidth = 1, relheight = 0.01, rely = 0.1)

    startPageText()
    startButtons()



def questionReform():
    reformedQList = []
    for question in questionList:
        question = question.replace(">>","→")
        question = question.replace("|","∨")
        question = question.replace("~","¬")
        question = question.replace("&","∧")
        question = question.replace("<>","↔")
        reformedQList.append(question)

    return reformedQList

####################ME
def typeReform():
    reformedTList = []
    for t in typeList:
        t = t.replace('\n','')
        reformedTList.append(t)

    return reformedTList
####################


def startPageText():
    global canvas_text

    test_string = "Welcome to Simpliφ."
    canvas_text = canvas.create_text(int(SCREEN_WIDTH/2.5), int(SCREEN_HEIGHT) / 3, text='', anchor=tk.NW, fill = "Black", font = ('Helvetica','30','bold'))
    
    #Time delay between chars, in milliseconds
    delta = 100
    delay = 0
    for i in range(len(test_string) + 1):
        s = test_string[:i]
        update_text = lambda s=s: canvas.itemconfigure(canvas_text, text=s)
        canvas.after(delay, update_text)
        delay += delta

def getQuestionText():
    global question_text

    test_string = "Enter question here."
    question_text = canvas.create_text(int(SCREEN_WIDTH/2.5), int(SCREEN_HEIGHT) / 10, text='', anchor=tk.NW, fill = "Black", font = ('Helvetica','30','bold'))
    #Time delay between chars, in milliseconds
    delta = 100
    delay = 0
    for i in range(len(test_string) + 1):
        s = test_string[:i]
        update_text = lambda s=s: canvas.itemconfigure(question_text, text=s)
        canvas.after(delay, update_text)
        delay += delta

def qText(text):
    global question_text

    test_string = "Simpliφ " + text
    question_text = canvas.create_text(int(SCREEN_WIDTH/2.5), int(SCREEN_HEIGHT) / 10, text='', anchor=tk.NW, fill = "Black", font = ('Helvetica','30','bold'))
    #Time delay between chars, in milliseconds
    delta = 100
    delay = 0
    for i in range(len(test_string) + 1):
        s = test_string[:i]
        update_text = lambda s=s: canvas.itemconfigure(question_text, text=s)
        canvas.after(delay, update_text)
        delay += delta

def userModeCommand():
    global mode
    mode = 0
    canvas.delete(canvas_text)
    userMode.destroy()
    teacherMode.destroy()
    userInputPage()

def teacherModeCommand():
    global mode
    mode = 1
    canvas.delete(canvas_text)
    userMode.destroy()
    teacherMode.destroy()
    teacherInputPage(0)


def startButtons():
    global userMode, teacherMode

    userMode = tk.Button(root, text = "User Input", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 200), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = userModeCommand)
    userMode.place(x = SCREEN_WIDTH * 0.25, y = SCREEN_HEIGHT * 0.6)

    teacherMode = tk.Button(root, text = "Teacher Input", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 200), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = teacherModeCommand)
    teacherMode.place(x = SCREEN_WIDTH * 0.6, y = SCREEN_HEIGHT * 0.6)


#USER INPUT PAGES

def submitQuestionButton():
    global sqb

    sqb = tk.Button(root, text = 'Submit', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), highlightbackground='#19BDE6', command = entryGet)
    sqb.place(x = int(SCREEN_WIDTH * 0.45), y = int(SCREEN_HEIGHT * 0.6)) 


def entryGet():
    global question, mode

    print("MODE: ", mode)
    question = entryBox.get()
    print(question)
    entryBox.delete(0, END)

    if mode == 0:
        canvas.delete(question_text)   
        qText(question)
        mode = 2

    elif mode == 1:
        if answerCorrect(question):
            canvas.delete(correctText)
            correct()

        else:
            print("WHYYY")
            incorrect()

    elif mode == 2:
        if answerUserModeCorrect(question):
            canvas.delete(correctText)
            correct()

        else:
            incorrect()


def lenAnswer():
    return len(entryBox.get())

def andButtonCommand():
    entryBox.insert(lenAnswer(), "∧")

def orButtonCommand():
    entryBox.insert(lenAnswer(), "∨")

def notButtonCommand():
    entryBox.insert(lenAnswer(), "¬")

def implicationButtonCommand():
    entryBox.insert(lenAnswer(), "→")

def biimplicationButtonCommand():
    entryBox.insert(lenAnswer(), "↔")

def symbolButtons():
    global andButton, orButton, notButton, implicationButton, biimplicationButton

    andButton = tk.Button(root, text = 'AND - ∧', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=andButtonCommand)
    andButton.place(x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.5))

    orButton = tk.Button(root, text = 'OR - ∨', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=orButtonCommand)
    orButton.place(x = int(SCREEN_WIDTH * 0.35), y = int(SCREEN_HEIGHT * 0.5))

    notButton = tk.Button(root, text = 'NOT - ¬', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=notButtonCommand)
    notButton.place(x = int(SCREEN_WIDTH * 0.45), y = int(SCREEN_HEIGHT * 0.5))

    implicationButton = tk.Button(root, text = 'IMP - →', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=implicationButtonCommand)
    implicationButton.place(x = int(SCREEN_WIDTH * 0.55), y = int(SCREEN_HEIGHT * 0.5))

    biimplicationButton = tk.Button(root, text = 'BIMP - ↔', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=biimplicationButtonCommand)
    biimplicationButton.place(x = int(SCREEN_WIDTH * 0.65), y = int(SCREEN_HEIGHT * 0.5))



def userInputPage():
    global entryBox, inputFrame

    inputFrame = tk.Frame(root, bg = "#1EBDE5", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)

    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))

    getQuestionText()
    symbolButtons()
    submitQuestionButton()
    homeButton()

def answerUserModeCorrect(answer):
    global ABSCURRENT
    ABSCURRENT = answer
    listOfSteps, listOfResults = file.solveSeperate(answer)
    answer = answerFixUp(answer)
    print("ANSWER: ", answer)
    check = str(listOfResults[len(listOfResults) - 1])
    check = answerFixUp(check)
    print("CHECK: ", check)
    if answer == check:
        return True

    return False


#TEACHER INPUT PAGES  

def teacherInputPage(qNum):
    global entryBox, inputFrame, formText

    inputFrame = tk.Frame(root, bg = "#1EBDE5", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)

    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))

    qText(str(reformedQList[qNum]))
    formText = canvas.create_text(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT) / 5, text = typeList[qNum], font = ('Helvetica','30'), fill = 'black')
    symbolButtons()
    submitQuestionButton()
    nextButtonFunction()
    homeButton()


    if qNum == len(reformedQList) - 1:
        deleteNextButton()

def nextButtonFunction():
    global nextButton
    nextButton = tk.Button(root, text = 'Next', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=nextButtonCommand)
    nextButton.place(x = int(SCREEN_WIDTH * 0.75), y = int(SCREEN_HEIGHT * 0.75))

def deleteNextButton():
    nextButton.destroy()

def nextButtonCommand():
    global qNum
    canvas.delete(formText)
    canvas.delete(question_text)
    canvas.delete(correctText)
    inputFrame.destroy()
    entryBox.destroy()
    andButton.destroy()
    orButton.destroy()
    notButton.destroy()
    implicationButton.destroy()
    biimplicationButton.destroy()
    home.destroy()
    nextButton.destroy()
    sqb.destroy()
    TTButton.destroy()
    workingsButton.destroy()
    qNum += 1
    teacherInputPage(qNum)
    home.destroy() 
    homeButton()

def homeButton():
    global home

    home = tk.Button(root, text = 'Home', width = int(SCREEN_WIDTH / 200), height = int(SCREEN_HEIGHT / 500), font = ('Helvetica','30'), command=homeButtonCommand)
    home.place(x = int(SCREEN_WIDTH * 0.15), y = int(SCREEN_HEIGHT * 0.75))

def homeButtonCommand():
    sqb.destroy()
    canvas.delete(formText)
    canvas.delete(question_text)
    canvas.delete(correctText)
    entryBox.destroy()
    inputFrame.destroy()
    andButton.destroy()
    orButton.destroy()
    notButton.destroy()
    implicationButton.destroy()
    biimplicationButton.destroy()
    nextButton.destroy()
    home.destroy()
    TTButton.destroy()
    workingsButton.destroy()
    
    init()

def answerCorrect(answer):
    gaps = " "
    for gaps in reformedTList[qNum]:
        reformedTList[qNum] = reformedTList[qNum].replace(" ","")
        
    if reformedTList[qNum] == "DNF":
        listOfSteps, listOfResults = file.solveSeperate(reformedQList[qNum])
        answer = answerFixUp(answer)
        print("ANSWER: ", answer)
        check = str(listOfResults[len(listOfResults) - 1])
        check = answerFixUp(check)
        print("CHECK: ", check)
        if answer == check:
            return True

        return False
    else:
        listOfSteps = file.solveAON(reformedQList[qNum])
        answer = answerFixUp(answer)
        print("ANSWER: ", answer)
        check = str(listOfSteps[len(listOfSteps) - 1])
        check = answerFixUp(check)
        print("CHECK: ", check)
        if answer == check:
            return True

        return False

def correct():
    global inputFrame, correctText, entryBox

    inputFrame.destroy()
    inputFrame = tk.Frame(root, bg = "#2fba2f", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)
    entryBox.destroy()
    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))
    correctText = canvas.create_text(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.15), text = "CORRECT!", font = ('Helvetica','60'), fill = 'black')
    canvas.delete(formText)
    canvas.delete(question_text)
    sqb.destroy()
    showButtons()

def showButtons():
    global TTButton, workingsButton

    TTButton = tk.Button(root, text = "Truth Table", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 250), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = displayTT)
    TTButton.place(x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.57)

    workingsButton = tk.Button(root, text = "Show Working", width = int(SCREEN_WIDTH / 100), height = int(SCREEN_HEIGHT / 250), activeforeground = "blue", font = ('Helvetica','30'), highlightbackground='#19BDE6', command = displayWorkings)
    workingsButton.place(x = SCREEN_WIDTH * 0.61, y = SCREEN_HEIGHT * 0.57)

def incorrect():
    global inputFrame, entryBox

    print("WHYYY")

    inputFrame.destroy()
    inputFrame = tk.Frame(root, bg = "#c9262e", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)
    entryBox.destroy()
    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))
    inputFrame.after(1000, destroyInputFrame)
    print("AAAA")

    """entryBox.destroy()
    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))
    inputFrame = tk.Frame(root, bg = "#1EBDE5", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)"""

def destroyInputFrame():
    global inputFrame, entryBox
    inputFrame.destroy()
    inputFrame = tk.Frame(root, bg = "#1EBDE5", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)
    entryBox.destroy()
    entryBox = Entry(root, width = int(SCREEN_WIDTH * 0.2), font = ('Helvetica','30'), bg = 'white', fg = 'black')
    entryBox.place(relwidth = 0.5, relheight = 0.07, x = int(SCREEN_WIDTH * 0.25), y = int(SCREEN_HEIGHT * 0.36))

def returnInputFrame():
    global inputFrame
    inputFrame = tk.Frame(root, bg = "#1EBDE5", highlightcolor="#19BDE6", borderwidth=5, relief='raised')
    inputFrame.place(relwidth = 0.6, relheight = 0.2, x = SCREEN_WIDTH * 0.2, y = SCREEN_HEIGHT * 0.3)

def displayTT():
    if mode==2:
        listOfSteps, listOfResults = file.solveSeperate(ABSCURRENT)
        arguments = getArguments(str(listOfResults[len(listOfResults) - 1]))
        print(arguments)
        question = (TTFormat(TTPreFormat(str(listOfResults[len(listOfResults) - 1])))).lower()
        expression = [question]
        truthTable = ttg.Truths(arguments, expression, ints = False)
        top = Toplevel(root)
        top.geometry("750x750")
        top.title("Truth Table")
        Label(top, text= truthTable, font=('Mistral 18 bold')).place(x=150,y=80)

    else:
        listOfSteps, listOfResults = file.solveSeperate(reformedQList[qNum])
        arguments = getArguments(str(listOfResults[len(listOfResults) - 1]))
        print(arguments)
        question = (TTFormat(TTPreFormat(str(listOfResults[len(listOfResults) - 1])))).lower()
        expression = [question]
        truthTable = ttg.Truths(arguments, expression, ints = False)
        top = Toplevel(root)
        top.geometry("750x750")
        top.title("Truth Table")
        Label(top, text= truthTable, font=('Mistral 18 bold')).place(x=150,y=80)

def displayWorkings():
    y = 80
    if mode==2:
        listOfSteps, listOfResults = file.solveSeperate(ABSCURRENT)
        top = Toplevel(root)
        top.geometry("750x750")
        top.title("Workings")
        for i in range (0, len(listOfResults)):
            Label(top, text= listOfSteps[i], font=('Mistral 18 bold')).place(x=150,y=y)
            y += 30
            Label(top, text= listOfResults[i], font=('Mistral 18 bold')).place(x=150,y=y)
            y += 30
        return
    
    if reformedTList[qNum] == "DNF":
        listOfSteps, listOfResults = file.solveSeperate(reformedQList[qNum])
        top = Toplevel(root)
        top.geometry("750x750")
        top.title("Workings")
        for i in range (0, len(listOfResults)):
            Label(top, text= listOfSteps[i], font=('Mistral 18 bold')).place(x=150,y=y)
            y += 30
            Label(top, text= listOfResults[i], font=('Mistral 18 bold')).place(x=150,y=y)
            y += 30
    else:
        workings = file.solveAON(reformedQList[qNum])
        top = Toplevel(root)
        top.geometry("750x750")
        top.title("Workings")
        for line in (workings):
            Label(top, text= line, font=('Mistral 18 bold')).place(x=150,y=y)
            y += 30
        #####

def answerFixUp(question):
   
    question = question.replace("∧","&")
    question = question.replace("∨","|")
    question = question.replace("¬","~")
    question = question.replace("→", ">>")
    question = question.replace("↔", "<>")
    question = question.replace(" ","") #Remove redundant spaces - if any

    return question

alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
statement = []

def getArguments(expression):
    arguments = []
    expression = expression.lower()
    numberofUses = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, "i":0, "j":0,
        "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, "r":0, "s":0,
        "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0
    }
    for i in alpha:
        occurences = expression.count(i)
        numberofUses[i] = occurences

    for i in numberofUses:
        if numberofUses[i] != 0:
            arguments.append(i)

    return arguments

def TTFormat(question):
    question = question.replace("→"," implies ")
    question = question.replace("∨"," or ")
    question = question.replace("¬"," ~")
    question = question.replace("∧"," and ")
    question = question.replace("↔","=")

    return question

def TTPreFormat(question):
    question = question.replace(">>","→")
    question = question.replace("|","∨")
    question = question.replace("~","¬")
    question = question.replace("&","∧")
    question = question.replace("<>","↔")

    return question

  



    


init()
reformedQList = questionReform()
reformedTList = typeReform()
canvas.pack()
root.mainloop()


