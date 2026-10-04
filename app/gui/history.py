import tkinter as tk
from tkinter import ttk,messagebox
import pandas as pd
from app.config import BG,WHITE,NAVY,BLUE,RED,AMBER,GREEN,FONT_HEADING,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import get_all_predictions,search_predictions,clear_predictions
from app.modules.reporter import Reporter
class HistoryScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill='both',expand=True);self.controller=controller
  Sidebar(self,controller,'history'); content=tk.Frame(self,bg=BG);content.pack(side='right',fill='both',expand=True);make_header(content,controller,'Prediction History')
  bar=tk.Frame(content,bg=BG);bar.pack(fill='x',padx=22,pady=15);tk.Label(bar,text='Prediction History',bg=BG,fg=NAVY,font=("Times New Roman",18,'bold')).pack(side='left')
  self.q=tk.StringVar();tk.Entry(bar,textvariable=self.q,font=FONT_NORMAL,width=24).pack(side='right',padx=6);tk.Button(bar,text='Search',command=self.refresh,bg=BLUE,fg=WHITE,font=FONT_NORMAL).pack(side='right');tk.Button(bar,text='Export CSV',command=self.export,bg=NAVY,fg=WHITE,font=FONT_NORMAL).pack(side='right',padx=8)
  cols=['student_id','attendance_pct','assignment_score','midterm_score','participation','previous_gpa','predicted_class','confidence','date_generated'];self.tree=ttk.Treeview(content,columns=cols,show='headings')
  labels=['Student ID','Attendance','Assignment','Midterm','Participation','Prev GPA','Prediction','Confidence','Date'];
  for c,l in zip(cols,labels):self.tree.heading(c,text=l);self.tree.column(c,width=105,anchor='center')
  self.tree.pack(fill='both',expand=True,padx=22,pady=(0,10));self.tree.tag_configure('At-Risk',background='#FADBD8');self.tree.tag_configure('Average',background='#FCF3CF');self.tree.tag_configure('High-Achiever',background='#D5F5E3');self.refresh()
  tk.Button(content,text='Clear All History',command=self.clear,bg=RED,fg=WHITE,font=FONT_NORMAL).pack(anchor='e',padx=22,pady=10)
 def refresh(self):
  rows=search_predictions(self.q.get().strip()) if self.q.get().strip() else get_all_predictions();
  for i in self.tree.get_children():self.tree.delete(i)
  self.rows=rows
  for r in rows:self.tree.insert('', 'end',values=[r.get(c,'') for c in self.tree['columns']],tags=(r.get('predicted_class',''),))
 def export(self):
  if not self.rows:return messagebox.showinfo('Export','No prediction history to export.')
  p=Reporter.export_csv(pd.DataFrame(self.rows));messagebox.showinfo('Export complete',f'History exported to:\n{p}')
 def clear(self):
  if messagebox.askyesno('Confirm','Delete all prediction history?'):
   clear_predictions();self.refresh()
