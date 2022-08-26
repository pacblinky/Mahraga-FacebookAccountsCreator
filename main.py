import tkinter as tk
from mailu import Mailu
from mailer import Mailer
from facebot import FaceBot
from Person import Person
import uuid
from saver import Saver
import dotenv
import easygui
import re

class App(tk.Tk):
    def __init__(self):
        self.bot = None
        self.mailuer = None
        self.email = None
        self.password = None
        self.gender = None
        self.saver = None
        self.config = dotenv.dotenv_values("config.env")
        Person.initUsers("data.json")
        super().__init__()
        self.title('Facebook accounts creator')
        self.openBrowser_btn = tk.Button(self,text="Open Browser",command=self.openBrowser)
        self.closeBrowser_btn = tk.Button(self,text="Close Browser",command=self.closeBrowser,state="disabled")
        self.loginMailu_btn = tk.Button(self,text="Login Mailu",command=self.loginMailu)
        self.logoutMailu_btn = tk.Button(self,text="Logout Mailu",command=self.logoutMailu,state="disabled")
        self.createAccount_btn = tk.Button(self,text="Create account",command=self.createAccount,state="disabled")
        self.getCode_btn = tk.Button(self,text="Hat el Code",command=self.getCode,state="disabled")
        self.openSaver_btn = tk.Button(self,text="Open Saver",command=self.openSaver)
        self.closeSaver_btn = tk.Button(self,text="Close Saver",command=self.closeSaver,state="disabled")
        self.save_btn = tk.Button(self,text="Save account",command=lambda: self.saveAccount("uncomplete_accounts"),state="disabled")
        self.saveError_Btn = tk.Button(self,text="Save account(error)",command=lambda: self.saveAccount("closed_accounts"),state="disabled")
        self.exit_btn = tk.Button(self, text="Exit", command=self.exitProgram)

        self.loginMailu_btn.grid(row=1, column=0)
        self.logoutMailu_btn.grid(row=1, column=1)
        self.openBrowser_btn.grid(row=2, column=0)
        self.closeBrowser_btn.grid(row=2, column=1)
        self.createAccount_btn.grid(row=3, column=0)
        self.getCode_btn.grid(row=3, column=1)
        self.openSaver_btn.grid(row=4, column=0)
        self.closeSaver_btn.grid(row=4, column=1)
        self.save_btn.grid(row=5, column=0)
        self.saveError_Btn.grid(row=5, column=1)
        self.exit_btn.grid(row=6, column=0)

    def openBrowser(self):
        self.bot = FaceBot()
        self.openBrowser_btn.configure(state="disabled")
        self.closeBrowser_btn.configure(state="active")
        self.createAccount_btn.configure(state="active")

    def closeBrowser(self):
        self.bot.close()
        self.openBrowser_btn.configure(state="active")
        self.closeBrowser_btn.configure(state="disabled")
        self.createAccount_btn.configure(state="disabled")
        self.bot = None

    def loginMailu(self):
        self.mailuer = Mailu(self.config["MAILU_URL"])
        if self.mailuer.login(self.config["MAILU_USERNAME"],self.config["MAILU_PASSWORD"]):
            self.loginMailu_btn.configure(state="disabled")
            self.logoutMailu_btn.configure(state="active")
            self.createAccount_btn.configure(state="active")
            tk.messagebox.showinfo("Mailu logged in","tam tsgeel el do8al 3la mailu")
        else:
            self.createAccount_btn.configure(state="disabled")
            self.mailuer = None
            tk.messagebox.showerror("Can't login to Mailu","Shoflak klba 7ad l3b fe el router")

    def logoutMailu(self):
        self.mailuer.logout()
        self.loginMailu_btn.configure(state="active")
        self.logoutMailu_btn.configure(state="disabled")
        self.createAccount_btn.configure(state="disabled")
        self.mailuer = None

    def createAccount(self):
        customMail = False
        code = str(uuid.uuid4())
        self.password = code.split("-")[1] + code.split("-")[2]
        signup = True
        if not self.bot:
            tk.messagebox.showwarning("Can't create account","Please open the browser first")
            self.getCode_btn.configure(state="disabled")
            return
        while True:
            reply = easygui.enterbox("Do you want to use a custom email?","Custom email")
            if reply:
                if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',reply):
                    customMail = True
                    self.email = reply
                    break
                else:
                    tk.messagebox.showwarning("Invalid self.email","Please enter a valid self.email")
            else:
                self.email = code.split("-")[0] + "@mahraga.com"
                break
        if customMail:
            self.getCode_btn.configure(state="disabled")
        else:
            if self.mailuer is not None:
                if self.mailuer.addUser(
                        self.email.split("@")[0], self.password):
                    self.getCode_btn.configure(state="active")
                else:
                    signup = False
                    tk.messagebox.showerror("Can't create account","yorga el m7wla mn gdded")
            else:
                signup = False
                tk.messagebox.showwarning("Can't create account","Please login to mailu first")
        if signup:
            person = Person.getUser()
            self.gender = int(person.gender)
            self.bot.signup(self.email, self.password, person)
            tk.messagebox.showinfo("Creating account", "no touch el browser")

    def getCode(self):
        mail = Mailer(self.config["MAIL_HOST"], int(self.config["MAIL_PORT"]))
        if mail.login(self.email, self.password):
            code = mail.getCode()
            if code == False:
                tk.messagebox.showinfo("No code yet", "el code lsa mwaslash")
            else:
                self.clipboard_clear()
                self.clipboard_append(code)
                tk.messagebox.showinfo("Got the code", code)
        else:
            tk.messagebox.showerror("Can't login to get code","msh 3raf aft7 el email ageeb el code yasta")
        mail.logout()

    def openSaver(self):
        self.saver = Saver(self.config["SAVER_DBHOST"],int(self.config["SAVER_DBPORT"]),self.config["SAVER_DBUSER"],self.config["SAVER_DBPASS"],self.config["SAVER_DBNAME"])
        if self.saver.open():
            self.closeSaver_btn.configure(state="active")
            self.openSaver_btn.configure(state="disabled")
            self.save_btn.configure(state="active")
            tk.messagebox.showinfo("Saver opened successfully","el saver bymse 3lek")
        else:
            tk.messagebox.showerror("Can't open the saver","shoflak klba yala")
            self.saver = None

    def closeSaver(self):
        self.saver.close()
        self.closeSaver_btn.configure(state="disabled")
        self.openSaver_btn.configure(state="active")
        self.save_btn.configure(state="disabled")
        self.saver = None

    def saveAccount(self, table):
        if self.saver.addAccount(self.email, self.password, int(self.gender),table):
            tk.messagebox.showinfo("Saved account","el account ra7 m3a a5wato")
            self.bot.logout()
        else:
            tk.messagebox.showerror("Can't save account","el account ra7 el teen")

    def exitProgram(self):
        confirm = tk.messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
        if confirm:
            if self.bot:
                self.bot.close()
            if self.mailuer:
                self.mailuer.logout()
            if self.saver:
                self.saver.close()
            self.destroy()
            
if __name__ == "__main__":
  app = App()
  app.mainloop()