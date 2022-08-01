from email import message
from tkinter import Tk, Label, Button,messagebox
from mailu import Mailu
from mailer import FaceMailer
from facebook import Facebook
from person import Person
from uuid import uuid4
from saver import Saver

Person.initUsers("data.json")
root = Tk()

bot = None
mailer = None
mailuer = None
email = None
password = None
gender = None
saver = None

def openBrowser():
    global bot
    bot = Facebook()
    openBrowser_btn.configure(state="disabled")
    closeBrowser_btn.configure(state="active")
    createAccount_btn.configure(state="active")

def closeBrowser():
    global bot
    bot.close()
    openBrowser_btn.configure(state="active")
    closeBrowser_btn.configure(state="disabled")
    createAccount_btn.configure(state="disabled")

def loginMailu():
    global mailuer
    mailuer = Mailu("http://mail.mahraga.com/")
    if mailuer.login("admin@mahraga.com","Mail012243543"):
        loginMailu_btn.configure(state="disabled")
        logoutMailu_btn.configure(state="active")
        createAccount_btn.configure(state="active")
        messagebox.showinfo("Connected",  "tam tsgeel el do8al")
    else:
        createAccount_btn.configure(state="disabled")
        messagebox.showerror("Can't login","Shoflak klba 7ad l3b fe el router")
    
def logoutMailu(): 
    global mailuer
    mailuer.logout()
    loginMailu_btn.configure(state="active")
    logoutMailu_btn.configure(state="disabled")
    createAccount_btn.configure(state="disabled")

def createAccount():
    global mailuer
    global bot
    global email
    global password
    global gender
    code = str(uuid4())
    email = code.split("-")[0]
    password = code.split("-")[1]+code.split("-")[2]
    person = Person.getUser()
    gender = int(person.gender)
    if mailuer.addUser(email,password):
        messagebox.showinfo("el email at3ml",  "no touch el browser")
        getCode_btn.configure(state="active")
        bot.signup(email+"@mahraga.com",password,person)
    else:
        getCode_btn.configure(state="disabled")
        messagebox.showerror("el email msh rady yt3ml","yorga el m7wla mn gdded")

def getCode():
    global email
    global password
    mail = FaceMailer("mail.mahraga.com",143)
    mail.login(email+"@mahraga.com",password)
    code = mail.getCode()
    if code == False:
        messagebox.showinfo("no code","no code")
    else:
        root.clipboard_clear()
        root.clipboard_append(code)
        messagebox.showinfo("El code wasal",code)

def openSaver():
    global saver
    saver = Saver("mahraga.com",3306,"facebot","-aPA@safPzWxP@9M","facebot")
    if saver.open():
        closeSaver_btn.configure(state="active")
        openSaver_btn.configure(state="disabled")
        save_btn.configure(state="active")
        messagebox.showinfo("Saver connected","el saver bymse 3lek")
    else:
        messagebox.showerror("Can't Connect to Saver","shoflak klba yala")

def closeSaver():
    global saver
    saver.close()
    closeSaver_btn.configure(state="disabled")
    openSaver_btn.configure(state="active")
    save_btn.configure(state="disabled")

def saveAccount(table):
    global email
    global password
    global gender
    global saver
    if saver.addAccount(email,password,int(gender),table):
        messagebox.showinfo("Saved account","el account ra7 m3a a5wato")
    else:
        messagebox.showerror("Can't save account","el account ra7 el teen")

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

root.mainloop()