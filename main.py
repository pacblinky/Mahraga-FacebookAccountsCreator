from tkinter import Tk, Label, Button, messagebox
from mailu import Mailu
from mailer import Mailer
from facebot import FaceBot
from person import Person
from uuid import uuid4
from saver import Saver
from dotenv import dotenv_values
from easygui import enterbox
from re import fullmatch

root = Tk()
bot = None
mailuer = None
email = None
password = None
gender = None
saver = None
config = dotenv_values("config.env")
Person.initUsers("data.json")

def openBrowser():
    global bot
    bot = FaceBot()
    openBrowser_btn.configure(state="disabled")
    closeBrowser_btn.configure(state="active")
    createAccount_btn.configure(state="active")

def closeBrowser():
    global bot
    bot.close()
    openBrowser_btn.configure(state="active")
    closeBrowser_btn.configure(state="disabled")
    createAccount_btn.configure(state="disabled")
    bot = None

def loginMailu():
    global mailuer
    mailuer = Mailu(config["MAILU_URL"])
    if mailuer.login(config["MAILU_USERNAME"],config["MAILU_PASSWORD"]):
        loginMailu_btn.configure(state="disabled")
        logoutMailu_btn.configure(state="active")
        createAccount_btn.configure(state="active")
        messagebox.showinfo("Mailu logged in", "tam tsgeel el do8al 3la mailu")
    else:
        createAccount_btn.configure(state="disabled")
        mailuer = None
        messagebox.showerror("Can't login to Mailu","Shoflak klba 7ad l3b fe el router")
    
def logoutMailu(): 
    mailuer.logout()
    loginMailu_btn.configure(state="active")
    logoutMailu_btn.configure(state="disabled")
    createAccount_btn.configure(state="disabled")
    mailuer = None

def createAccount():
    global email
    global password
    global gender
    customMail = False
    code = str(uuid4())
    signup = True
    while True:
        reply = enterbox("Do you want to use a custom email?","Custom email")
        if reply:
            if fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', reply):
                customMail = True
                email = reply
                break
            else:
                messagebox.showwarning("Invalid email","Please enter a valid email")
        else:
            email = code.split("-")[0]+"@mahraga.com"
            break
    if customMail:
        getCode_btn.configure(state="disabled")
    else:
        if mailuer:
            if mailuer.addUser(email.split("@")[0],password):
                getCode_btn.configure(state="active")
            else:
                signup = False
                messagebox.showerror("Can't create account","yorga el m7wla mn gdded")
        else:
            signup = False
            messagebox.showwarning("Can't create account","Please login to mailu first")
    if signup:
        person = Person.getUser()
        gender = int(person.gender)
        password = code.split("-")[1]+code.split("-")[2]
        bot.signup(email,password,person)
        messagebox.showinfo("Creating account","no touch el browser")

def getCode():
    mail = Mailer(config["MAIL_HOST"],int(config["MAIL_PORT"]))
    if mail.login(email+"@mahraga.com",password):
        code = mail.getCode()
        if code == False:
            messagebox.showinfo("No code yet","el code lsa mwaslash")
        else:
            root.clipboard_clear()
            root.clipboard_append(code)
            messagebox.showinfo("Got the code",code)
    else:
        messagebox.showerror("Can't login to get code","msh 3raf aft7 el email ageeb el code yasta")
    mail.logout()

def openSaver():
    global saver
    saver = Saver(config["SAVER_DBHOST"],int(config["SAVER_DBPORT"]),config["SAVER_DBUSER"],config["SAVER_DBPASS"],config["SAVER_DBNAME"])
    if saver.open():
        closeSaver_btn.configure(state="active")
        openSaver_btn.configure(state="disabled")
        save_btn.configure(state="active")
        messagebox.showinfo("Saver opened successfully","el saver bymse 3lek")
    else:
        messagebox.showerror("Can't open the saver","shoflak klba yala")
        saver = None

def closeSaver():
    global saver
    saver.close()
    closeSaver_btn.configure(state="disabled")
    openSaver_btn.configure(state="active")
    save_btn.configure(state="disabled")
    saver = None

def saveAccount(table):
    if saver.addAccount(email,password,int(gender),table):
        messagebox.showinfo("Saved account","el account ra7 m3a a5wato")
        bot.logout()
    else:
        messagebox.showerror("Can't save account","el account ra7 el teen")

def exitProgram():
    confirm = messagebox.askyesno("Confirmation","Are you sure you want to quit?")
    if confirm:
        if bot:
            bot.close()
        if mailuer:
            mailuer.logout()
        if saver:
            saver.close()
        root.destroy()

openBrowser_btn = Button(root,text="Open Browser",command=openBrowser)
closeBrowser_btn = Button(root,text="Close Browser",command=closeBrowser,state="disabled")
loginMailu_btn = Button(root,text="Login Mailu", command=loginMailu)
logoutMailu_btn = Button(root,text="Logout Mailu",command=logoutMailu,state="disabled")
createAccount_btn = Button(root,text="Create account",command=createAccount,state="disabled") 
getCode_btn = Button(root,text="Hat el Code",command=getCode,state="disabled")
openSaver_btn = Button(root,text="Open Saver",command=openSaver)
closeSaver_btn = Button(root,text="Close Saver",command=closeSaver,state="disabled")
save_btn = Button(root,text="Save account",command= lambda: saveAccount("uncomplete_accounts"),state="disabled")
saveError_btn = Button(root,text="Save account(error)",command= lambda: saveAccount("closed_accounts"),state="disabled")
exit_btn = Button(root,text="Exit",command=exitProgram )

loginMailu_btn.grid(row=1,column=0)
logoutMailu_btn.grid(row=1,column=1)
openBrowser_btn.grid(row=2,column=0)
closeBrowser_btn.grid(row=2,column=1)
createAccount_btn.grid(row=3,column=0)
getCode_btn.grid(row=3,column=1)
openSaver_btn.grid(row=4,column=0)
closeSaver_btn.grid(row=4,column=1)
save_btn.grid(row=5,column=0)
saveError_btn.grid(row=5,column=1)
exit_btn.grid(row=6,column=0)

root.mainloop()