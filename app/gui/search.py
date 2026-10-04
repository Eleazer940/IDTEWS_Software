import tkinter as tk
from app.config import BG,WHITE,NAVY,BLUE,RED,AMBER,GREEN,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import search_predictions
class SearchScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill='both',expand=True);self.controller=controller;Sidebar(self,controller,'search');c=tk.Frame(self,bg=BG);c.pack(side='right',fill='both',expand=True);make_header(c,controller,'Student Search')
  card=tk.Frame(c,bg=WHITE,highlightbackground='#BDC3C7',highlightthickness=1);card.pack(fill='x',padx=60,pady=35);tk.Label(card,text='Find Student Performance Record',bg=WHITE,fg=NAVY,font=("Times New Roman",18,'bold')).pack(pady=(25,12));self.q=tk.StringVar();tk.Entry(card,textvariable=self.q,font=("Times New Roman",13),width=30).pack(pady=8);tk.Button(card,text='SEARCH STUDENT',command=self.search,bg=BLUE,fg=WHITE,font=FONT_NORMAL,padx=18,pady=8).pack(pady=(5,25));self.result=tk.Frame(c,bg=BG);self.result.pack(fill='both',expand=True,padx=60,pady=10)
 def search(self):
  for w in self.result.winfo_children():w.destroy()
  rows=search_predictions(self.q.get().strip())
  if not rows:tk.Label(self.result,text='No student record found.',bg=BG,fg='#7F8C8D',font=("Times New Roman",14)).pack(pady=30);return
  r=rows[0];color={'At-Risk':RED,'Average':AMBER,'High-Achiever':GREEN}.get(r['predicted_class'],BLUE)
  box=tk.Frame(self.result,bg=WHITE);box.pack(fill='x');tk.Label(box,text=f"Student: {r['student_id']}",bg=WHITE,fg=NAVY,font=("Times New Roman",18,'bold')).pack(anchor='w',padx=25,pady=15)
  tk.Label(box,text=r['predicted_class'],bg=color,fg=WHITE,font=("Times New Roman",18,'bold'),padx=15,pady=8).pack(anchor='w',padx=25,pady=5)
  text=f"Attendance: {r['attendance_pct']}%\nAssignment Score: {r['assignment_score']}%\nMidterm Score: {r['midterm_score']}%\nParticipation: {r['participation']}\nPrevious GPA: {r['previous_gpa']}\nConfidence: {r['confidence']:.2f}%\nDate: {r['date_generated']}"
  tk.Label(box,text=text,bg=WHITE,fg=NAVY,font=FONT_NORMAL,justify='left').pack(anchor='w',padx=25,pady=20)
