import tkinter as tk
from tkinter import messagebox
from app.config import BG, WHITE, NAVY, BLUE, GREEN, RED, AMBER, FONT_NORMAL, FONT_BOLD, FONT_HEADING, CAT_COLORS
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import search_predictions

class StudentProfileScreen(tk.Frame):
    """Professional student performance profile with latest saved prediction."""
    def __init__(self,parent,controller):
        super().__init__(parent,bg=BG); self.controller=controller; self.pack(fill='both',expand=True)
        body=tk.Frame(self,bg=BG); body.pack(fill='both',expand=True)
        Sidebar(body,controller,active='profile')
        content=tk.Frame(body,bg=BG); content.pack(side='right',fill='both',expand=True)
        make_header(content,controller,'Student Performance Profile')
        search=tk.Frame(content,bg=WHITE); search.pack(fill='x',padx=22,pady=18)
        tk.Label(search,text='Student ID:',bg=WHITE,font=FONT_BOLD).pack(side='left',padx=12,pady=12)
        self.var=tk.StringVar(); tk.Entry(search,textvariable=self.var,font=FONT_NORMAL,width=30).pack(side='left',padx=8)
        tk.Button(search,text='VIEW PROFILE',command=self.load,bg=BLUE,fg=WHITE,font=FONT_BOLD,relief='flat',padx=16).pack(side='left',padx=8)
        self.card=tk.Frame(content,bg=WHITE); self.card.pack(fill='both',expand=True,padx=22,pady=(0,22))
        tk.Label(self.card,text='Search for a student to view the latest academic performance profile.',bg=WHITE,fg='#7F8C8D',font=FONT_HEADING).pack(pady=80)
    def load(self):
        sid=self.var.get().strip()
        if not sid: messagebox.showwarning('Student ID','Enter a Student ID.'); return
        rows=search_predictions(sid)
        if not rows: messagebox.showinfo('Not found','No prediction was found for this Student ID.'); return
        r=rows[0]
        for w in self.card.winfo_children(): w.destroy()
        top=tk.Frame(self.card,bg=WHITE); top.pack(fill='x',padx=28,pady=24)
        cls=r['predicted_class']; color=CAT_COLORS.get(cls,NAVY)
        tk.Label(top,text=f'Student: {r["student_id"]}',bg=WHITE,fg=NAVY,font=('Times New Roman',20,'bold')).pack(anchor='w')
        tk.Label(top,text=f'Latest prediction • {r["date_generated"]}',bg=WHITE,fg='#7F8C8D',font=FONT_NORMAL).pack(anchor='w',pady=(4,12))
        tk.Label(top,text=cls,bg=color,fg=WHITE,font=('Times New Roman',18,'bold'),padx=18,pady=10).pack(anchor='w')
        grid=tk.Frame(self.card,bg=WHITE); grid.pack(fill='x',padx=28,pady=10)
        vals=[('Attendance',f'{r["attendance_pct"]:.1f}%'),('Assignment',f'{r["assignment_score"]:.1f}%'),('Midterm',f'{r["midterm_score"]:.1f}%'),('Participation',f'{r["participation"]:.1f}/10'),('Previous GPA',f'{r["previous_gpa"]:.2f}'),('Confidence',f'{r["confidence"]:.1f}%')]
        for i,(a,b) in enumerate(vals):
            box=tk.Frame(grid,bg=BG,highlightbackground='#BDC3C7',highlightthickness=1)
            box.grid(row=i//3,column=i%3,sticky='nsew',padx=8,pady=8)
            tk.Label(box,text=a,bg=BG,fg='#7F8C8D',font=FONT_NORMAL).pack(pady=(12,2))
            tk.Label(box,text=b,bg=BG,fg=NAVY,font=('Times New Roman',16,'bold')).pack(pady=(0,12))
        for i in range(3): grid.grid_columnconfigure(i,weight=1)
        msg='Immediate academic intervention and close monitoring are recommended.' if cls=='At-Risk' else ('Continue monitoring and provide targeted improvement support.' if cls=='Average' else 'Excellent performance. Encourage advanced learning and leadership opportunities.')
        tk.Label(self.card,text='IDTEWS Recommendation',bg=WHITE,fg=NAVY,font=FONT_HEADING).pack(anchor='w',padx=28,pady=(20,4))
        tk.Label(self.card,text=msg,bg=WHITE,fg='#34495E',font=FONT_NORMAL,wraplength=800,justify='left').pack(anchor='w',padx=28,pady=(0,20))
