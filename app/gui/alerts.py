import tkinter as tk
from tkinter import ttk
from app.config import BG,WHITE,NAVY,RED,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import get_at_risk_predictions
class AlertsScreen(tk.Frame):
 def __init__(self,parent,controller):
  super().__init__(parent,bg=BG);self.pack(fill='both',expand=True);Sidebar(self,controller,'alerts');c=tk.Frame(self,bg=BG);c.pack(side='right',fill='both',expand=True);make_header(c,controller,'Early Warning Alerts')
  rows=get_at_risk_predictions(100);banner=tk.Label(c,text=f'EARLY WARNING: {len(rows)} At-Risk student(s) require attention',bg=RED,fg=WHITE,font=("Times New Roman",15,'bold'),pady=12);banner.pack(fill='x',padx=22,pady=20)
  tk.Label(c,text='Recommended action: review attendance and academic performance, then initiate personalised intervention.',bg=BG,fg=NAVY,font=FONT_NORMAL).pack(anchor='w',padx=22,pady=5)
  cols=['student_id','attendance_pct','assignment_score','midterm_score','confidence','date_generated'];t=ttk.Treeview(c,columns=cols,show='headings');
  for x,l in zip(cols,['Student ID','Attendance','Assignment','Midterm','Confidence','Date']):t.heading(x,text=l);t.column(x,width=140,anchor='center')
  for r in rows:t.insert('', 'end',values=[r.get(x,'') for x in cols])
  t.pack(fill='both',expand=True,padx=22,pady=20)
