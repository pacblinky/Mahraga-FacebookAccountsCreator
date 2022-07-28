from tkinter import Tk, Label, Button,messagebox
from mailu import Mailu
from mailer import FaceMailer
from Facebook import Facebook
from Person import Person
from uuid import uuid4

Person.initUsers("data.json")

bot = None
mailer = None
ssh = None
email = None
password = None
gender = None

def openBrowser():
    global bot
    bot = Facebook()

def closeBrowser():
    global bot
    bot.close()

def connectSSH():
    global ssh
    ssh = Mailu("mail.mahraga.com",22,"root","mx012243543")
    if ssh.connect():
        messagebox.showinfo("Connected",  "Tam el atsaal")
    else:
        messagebox.showerror("Can't Connect","Shoflak klba 7ad l3b fe el router")
    
def closeSSH(): 
    global ssh
    ssh.disconnect()

def createAccount():
    global ssh
    global bot
    global email
    global password
    code = str(uuid4())
    email = code.split("-")[0]
    password = code.split("-")[1]+code.split("-")[2]

    if ssh.addUser(email,password):
        messagebox.showinfo("el email at3ml",  "no touch el browser")
        bot.signup(email+"@mahraga.com",password,Person.getUser())
    else:
        messagebox.showinfo("el email msh rady yt3ml","yorga el m7wla mn gdded")

def getCode():
    global email
    global password
    mail = FaceMailer("mail.mahraga.com",143)
    mail.login(email+"@mahraga.com",password)
    if mail.getCode() == False:
        messagebox.showinfo("no code","no code")
    else:
        messagebox.showinfo("El code wasal",mail.getCode())

def saveAccount():
    pass

root = Tk()
openBrowser_btn = Button(root,text="Open Browser",command=openBrowser)
closeBrowser_btn = Button(root,text="Close Browser",command=closeBrowser)
connectSSH_btn = Button(root,text="Connect SSH", command=connectSSH)
disconnectSSH_btn = Button(root,text="Close SSH",command=closeSSH)
createAccount_btn = Button(root,text="Create account",command=createAccount) 
getCode_btn = Button(root,text="Hat el Code",command=getCode)
save_btn = Button(root,text="Done",command=saveAccount)

connectSSH_btn.grid(row=1,column=0)
disconnectSSH_btn.grid(row=1,column=1)
openBrowser_btn.grid(row=2,column=0)
closeBrowser_btn.grid(row=2,column=1)
createAccount_btn.grid(row=3,column=0)
save_btn.grid(row=3,column=1)

root.mainloop()