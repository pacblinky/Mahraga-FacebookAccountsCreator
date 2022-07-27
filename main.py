from tkinter import Tk, Label, Button, Grid, Toplevel
from turtle import onclick
from mailu import Mailu
from Facebook import FaceBot

root = Tk()

title_lbl = Label(root, text="Mahraga Facebook Account Creator",font=("Arial",10))
currentAccount_lbl = Label(root, text="Current account:")

openBrowser_btn = Button(root,text="Open Browser")
closeBrowser_btn = Button(root,text="Close Browser")
connectSSH_btn = Button(root,text="Connect SSH")
disconnectSSH_btn = Button(root,text="Disconnect SSH")
createAccount_btn = Button(root,text="Create account") 
save_btn = Button(root,text="Done")

title_lbl.grid(row=0,column=0)
connectSSH_btn.grid(row=1,column=0)
disconnectSSH_btn.grid(row=1,column=1)
openBrowser_btn.grid(row=2,column=0)
closeBrowser_btn.grid(row=2,column=1)
createAccount_btn.grid(row=3,column=0)
save_btn.grid(row=3,column=1)



root.mainloop()