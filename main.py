from tkinter import Tk, Label, Button,messagebox
from mailu import Mailu
from mailer import FaceMailer
from Facebook import Facebook
from Person import Person
from uuid import uuid4

Person.initUsers("data.json")
root = Tk()

bot = None
mailer = None
mailuer = None
email = None
password = None
gender = None

def openBrowser():
    global bot
    bot = Facebook()

def closeBrowser():
    global bot
    bot.close()

def loginMailu():
    global mailuer
    mailuer = Mailu("http://mail.mahraga.com/")
    if mailuer.login("admin@mahraga.com","Mail012243543"):
        messagebox.showinfo("Connected",  "tam tsgeel el do8al")
    else:
        messagebox.showerror("Can't login","Shoflak klba 7ad l3b fe el router")
    
def logoutMailu(): 
    global mailuer
    mailuer.logout()

def createAccount():
    global mailuer
    global bot
    global email
    global password
    code = str(uuid4())
    email = code.split("-")[0]
    password = code.split("-")[1]+code.split("-")[2]

    if mailuer.addUser(email,password):
        messagebox.showinfo("el email at3ml",  "no touch el browser")
        bot.signup(email+"@mahraga.com",password,Person.getUser())
    else:
        messagebox.showinfo("el email msh rady yt3ml","yorga el m7wla mn gdded")

def getCode():
    global email
    global password
    mail = FaceMailer("mail.mahraga.com",143)
    mail.login(email+"@mahraga.com",password)
    code = mail.getCode()
    if code == False:
        messagebox.showinfo("no code","no code")
    else:
        messagebox.showinfo("El code wasal",code)
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(code)
        root.update()
        root.destroy()
        
def saveAccount():
    pass

openBrowser_btn = Button(root,text="Open Browser",command=openBrowser)
closeBrowser_btn = Button(root,text="Close Browser",command=closeBrowser)
connectSSH_btn = Button(root,text="Login Mailu", command=loginMailu)
disconnectSSH_btn = Button(root,text="Logout Mailu",command=logoutMailu)
createAccount_btn = Button(root,text="Create account",command=createAccount) 
getCode_btn = Button(root,text="Hat el Code",command=getCode)
save_btn = Button(root,text="Done",command=saveAccount)

connectSSH_btn.grid(row=1,column=0)
disconnectSSH_btn.grid(row=1,column=1)
openBrowser_btn.grid(row=2,column=0)
closeBrowser_btn.grid(row=2,column=1)
createAccount_btn.grid(row=3,column=0)
getCode_btn.grid(row=3,column=1)
save_btn.grid(row=4,column=0)

root.mainloop()