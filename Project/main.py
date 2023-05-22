import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import random
import textwrap

def connection() :
    global conn,cursor
    conn = sqlite3.connect("Database/Project.db")
    cursor = conn.cursor()

def mainwindow() :
    root = Tk()
    w = 1280
    h = 720
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/2
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    root.resizable(width=0, height=0)
    root.config(bg='#FFF3E2')
    root.title("Trivia Boss")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    
    # root.option_add('*Font', default_font)

    return root


def titlepage() :
    mainframe.grid_forget()
    titleframe.rowconfigure((0,3), weight=2)
    titleframe.rowconfigure(2, weight=1)
    titleframe.columnconfigure((0,1), weight=1)
    default_font = font.Font(family="Segoe Print", size=16)
    titleframe.option_add('*Font', default_font)

    titleframe.grid(row=0, column=0, sticky='news')

    title = Label(titleframe, text="Trivia Boss", image=icon, compound=TOP, font=("Segoe Print", 72, 'bold'), bg='#FFF3E2')
    title.grid(row=0, column=0, columnspan=2, sticky='news')

    Button(titleframe, text="New Game", image=def_button, compound=CENTER, borderwidth=0, command=newgameclicked, bg='#FFF3E2').grid(row=2, column=0, padx=30, sticky=E)
    Button(titleframe, text="Continue", image=def_button, compound=CENTER, borderwidth=0, command=continueclicked, bg='#FFF3E2').grid(row=2, column=1, padx=30, sticky=W)


def newgameclicked() :
    warning = messagebox.askquestion("Start a new game", "The progress saved will be lost, Are you sure?")
    if warning == 'yes' :
        sql = """
                update player
                set progress=1, life=3, fifty=1, hint=1, protect=1;
            """
        cursor.execute(sql)
        conn.commit()
        mainpage(1)


def continueclicked() :
    sql = "select progress from player;"
    cursor.execute(sql)
    level = cursor.fetchone()
    mainpage(level[0])


def getquiz(level) :
    global id
    
    sql = "select id from trivia where level=?;"
    cursor.execute(sql, [level])
    result = cursor.fetchall()

    x = [0, 1, 2, 3]
    id = [result[0][0], result[1][0], result[2][0], result[3][0]]
    rng = random.choice(x)


    sql = "select * from trivia where id=?;"
    cursor.execute(sql,[id[rng]])
    quiz = cursor.fetchone()

    return quiz


def mainpage(level) :
    titleframe.grid_forget()

    mainframe.rowconfigure(0, weight=1)
    mainframe.rowconfigure((1,4,5,6), weight=2)
    mainframe.rowconfigure(3, weight=3)

    mainframe.columnconfigure(2, weight=1)
    mainframe.columnconfigure((1,3), weight=3)

    mainframe.grid(row=0, column=0, sticky='news')

    global protection
    protection = 0

    sql = "select * from player"
    cursor.execute(sql)
    player = cursor.fetchone()
    fiftycheck = player[2]
    hintcheck = player[3]
    protectcheck = player[4]

    quiz = getquiz(level)

    Label(mainframe, text="Level " + str(quiz[1]), bg='#FFF3E2', font=("Segoe Print", 36)).grid(row=1, column=1, columnspan=3, pady=45)

    life = StringVar()
    Label(mainframe, textvariable=life, bg='#FFF3E2', font=("Segoe Print", 24), fg='#E74646').grid(row=2, column=3, sticky=S)
    if player[1] == 3 :
        life.set("♥ ♥ ♥")
    elif player[1] == 2 :
        life.set("  ♥ ♥")
    elif player[1] == 1 :
        life.set("    ♥")

    Label(mainframe, image=questionbox, text=textwrap.fill(quiz[2], width=60), font=("Segoe Print", 18), compound=CENTER, bg='#FFF3E2').grid(row=3, column=1, columnspan=3)

    choice1 = Button(mainframe, text=quiz[4], image=choicebox, compound=CENTER, borderwidth=0, bg='#FFF3E2', command=lambda:checkanswer(quiz[0], quiz[4]))
    choice1.grid(row=4, column=1, padx=5, sticky=E)
    choice2 = Button(mainframe, text=quiz[5], image=choicebox, compound=CENTER, borderwidth=0, bg='#FFF3E2', command=lambda:checkanswer(quiz[0], quiz[5]))
    choice2.grid(row=4, column=3, padx=5, sticky=W)
    choice3 = Button(mainframe, text=quiz[6], image=choicebox, compound=CENTER, borderwidth=0, bg='#FFF3E2', command=lambda:checkanswer(quiz[0], quiz[6]))
    choice3.grid(row=5, column=1, padx=5, sticky=E)
    choice4 = Button(mainframe, text=quiz[7], image=choicebox, compound=CENTER, borderwidth=0, bg='#FFF3E2', command=lambda:checkanswer(quiz[0], quiz[7]))
    choice4.grid(row=5, column=3, padx=5, sticky=W)

    Label(mainframe, text="Lifeline: ", bg='#FFF3E2').grid(row=0, column=3, sticky=E)

    fifty = Button(mainframe, text="50:50",fg='#FA9884', image=roundedbutton, compound=CENTER, borderwidth=0, bg='#FFF3E2', command=lambda: showfifty(quiz[0], ))
    fifty.grid(row=0, column=4, padx=5)
    if fiftycheck == 0 :
        fifty.config(image=disabled_roundedbutton, fg='black')
        fifty["state"] = DISABLED

    hint = Button(mainframe, image=hintbutton, borderwidth=0, bg='#FFF3E2', command=lambda: showhint(quiz[0]))
    hint.grid(row=0, column=5)
    if hintcheck == 0 :
        hint.config(image=disabled_hintbutton)
        hint["state"] = DISABLED

    protect = Button(mainframe, image=protectbutton, borderwidth=0, bg='#FFF3E2', command=protection_on)
    protect.grid(row=0, column=6, padx=5)
    if protectcheck == 0 :
        protect.config(image=disabled_protectbutton)
        protect["state"] = DISABLED


    Button(mainframe, text="Quit", image=def_button, compound=CENTER, borderwidth=0, fg='#FA9884', bg='#FFF3E2', command=titlepage).grid(row=5, column=5, columnspan=2)


def checkanswer(id, choice) :
    sql = "select answer from trivia where id=?;"
    cursor.execute(sql, [id])
    answer = cursor.fetchone()

    if choice == answer[0] :
        messagebox.showinfo("Congratulations!", "You have answered correctly!")
        levelup()
    else :
        messagebox.showinfo("Too bad", "You chose the wrong answer")
        lifedown(id)


def levelup() :
    sql = """
            update player
            set progress=progress + 1;
    """
    cursor.execute(sql)
    conn.commit()

    sql = "select progress from player"
    cursor.execute(sql)
    level = cursor.fetchone()

    if level[0] > 8 :
        messagebox.showinfo("Congratulations!", "You have cleared the game!")
        sql = """
                update player
                set progress=1, life=3;
        """
        cursor.execute(sql)
        conn.commit()
        titlepage()
    else :
        mainpage(level[0])

    

def lifedown(current) :
    global protection
    
    if protection == 0 :
        sql = """
            update player
            set life = life-1
        """
        cursor.execute(sql)
        conn.commit()
    else :
        messagebox.showinfo("Protection", "You have been protected! No life has been lost.")

    sql = "select * from player"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result[1] == 0 :
        messagebox.showinfo("Game Over", "You have ran out of life.\nBetter luck next time!")
        sql = """
                update player
                set progress=1, life=3;
        """
        cursor.execute(sql)
        conn.commit()
        titlepage()
    else :
        id.remove(current)
        mainpage(result[0])


def showfifty(id) :
    sql = "select * from trivia where id=?;"
    cursor.execute(sql,[id])
    result = cursor.fetchone()
    x = [4, 5, 6, 7]
    for i in x :
        if result[i] == result[8] :
            x.remove(i)
    rng = random.choice(x)

    choices = ["[" + result[8] + "]", "[" + result[rng] + "]"]
    messagebox.showinfo("50:50","Your 50:50 choices:\n\n" + str(random.sample(choices, len(choices))))

    sql = """
            update player
            set fifty=0;
    """
    cursor.execute(sql)
    conn.commit()


def showhint(id) :
    sql = "select hint from trivia where id=?;"
    cursor.execute(sql,[id])
    result = cursor.fetchone()
    messagebox.showinfo("Hint","Your hint:\n\n" + result[0])

    sql = """
            update player
            set hint=0;
    """
    cursor.execute(sql)
    conn.commit()


def protection_on() :
    global protection
    protection = 1
    messagebox.showinfo("Protection", "You have activated the protection, no life will be lost if you chose the wrong answer.")
    sql = """
                update player
                set protect=0
        """
    cursor.execute(sql)
    conn.commit()

    


connection()
root = mainwindow()
titleframe = Frame(root, bg='#FFF3E2')
mainframe = Frame(root, bg='#FFF3E2')


icon = PhotoImage(file="Pic/icon.png").subsample(9, 9)
questionbox = PhotoImage(file="Pic/questionbox.png")
choicebox = PhotoImage(file="Pic/choice.png")
def_button = PhotoImage(file="Pic/button.png")
roundedbutton = PhotoImage(file="Pic/roundedbutton.png")
disabled_roundedbutton = PhotoImage(file="Pic/roundedbutton_disabled.png")
hintbutton = PhotoImage(file="Pic/hintbutton.png")
disabled_hintbutton = PhotoImage(file="Pic/hintbutton_disabled.png")
protectbutton = PhotoImage(file="Pic/protectbutton.png")
disabled_protectbutton = PhotoImage(file="Pic/protectbutton_disabled.png")

protection = 0

selectoption = StringVar()

titlepage()


root.mainloop()
cursor.close()
conn.close()