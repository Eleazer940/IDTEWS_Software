import tkinter as tk
from tkinter import messagebox
from app.database import verify_user
from app.config import NAVY,WHITE,FONT_NORMAL,FONT_HEADING,APP_FULL
class LoginScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=NAVY);self.pack(fill="both",expand=True);self.controller=controller;c=tk.Frame(self,bg=WHITE,padx=40,pady=30);c.place(relx=.5,rely=.5,anchor="center")
  tk.Label(c,text="IDTEWS",bg=WHITE,fg=NAVY,font=("Times New Roman",22,"bold")).pack();tk.Label(c,text=APP_FULL,bg=WHITE,font=FONT_NORMAL).pack(pady=10)
  tk.Label(c,text="Username",bg=WHITE,font=FONT_NORMAL).pack(anchor="w");self.u=tk.Entry(c,font=FONT_NORMAL,width=28);self.u.pack(pady=5)
  tk.Label(c,text="Password",bg=WHITE,font=FONT_NORMAL).pack(anchor="w");self.p=tk.Entry(c,show="*",font=FONT_NORMAL,width=28);self.p.pack(pady=5)
  tk.Button(c,text="LOGIN",command=self.login,bg=NAVY,fg=WHITE,font=FONT_HEADING,width=20).pack(pady=15)
 def login(self):
  x=verify_user(self.u.get().strip(),self.p.get())
  if not x:messagebox.showerror("Login Failed","Invalid username or password.");return
  try:self.controller.load_predictor()
  except Exception as e:messagebox.showerror("Model Error",str(e));return
  self.controller.current_user=x;self.controller.show_dashboard() if x["role"]=="admin" else self.controller.show_data_entry()
