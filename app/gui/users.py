import tkinter as tk
from tkinter import ttk,messagebox
from app.config import BG,WHITE,NAVY,BLUE,GREEN,RED,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import get_all_users,add_user,delete_user
class UsersScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill='both',expand=True);self.controller=controller;Sidebar(self,controller,'users');c=tk.Frame(self,bg=BG);c.pack(side='right',fill='both',expand=True);make_header(c,controller,'User Management')
  form=tk.Frame(c,bg=WHITE);form.pack(fill='x',padx=22,pady=20);self.u=tk.StringVar();self.p=tk.StringVar();self.r=tk.StringVar(value='lecturer')
  for label,var in [('Username',self.u),('Password',self.p)]:tk.Label(form,text=label,bg=WHITE,fg=NAVY,font=FONT_NORMAL).pack(side='left',padx=(15,4),pady=15);tk.Entry(form,textvariable=var,font=FONT_NORMAL,width=16,show='*' if label=='Password' else '').pack(side='left',padx=5)
  ttk.Combobox(form,textvariable=self.r,values=['admin','lecturer','adviser'],width=10,state='readonly').pack(side='left',padx=5);tk.Button(form,text='Add User',command=self.add,bg=GREEN,fg=WHITE,font=FONT_NORMAL).pack(side='left',padx=10)
  self.t=ttk.Treeview(c,columns=['username','role'],show='headings');self.t.heading('username',text='Username');self.t.heading('role',text='Role');self.t.pack(fill='both',expand=True,padx=22,pady=10);tk.Button(c,text='Delete Selected User',command=self.delete,bg=RED,fg=WHITE,font=FONT_NORMAL).pack(anchor='e',padx=22,pady=10);self.refresh()
 def refresh(self):
  for i in self.t.get_children():self.t.delete(i)
  for r in get_all_users():self.t.insert('', 'end',values=(r['username'],r['role']))
 def add(self):
  if not self.u.get().strip() or not self.p.get():return messagebox.showwarning('User','Enter username and password.')
  if add_user(self.u.get().strip(),self.p.get(),self.r.get()):self.u.set('');self.p.set('');self.refresh()
  else:messagebox.showerror('User','Username already exists.')
 def delete(self):
  s=self.t.selection()
  if not s:return
  username=self.t.item(s[0])['values'][0]
  if delete_user(username):self.refresh()
  else:messagebox.showwarning('User','The default admin account cannot be deleted.')
