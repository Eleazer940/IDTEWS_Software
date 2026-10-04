import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.config import BG,WHITE,NAVY,BLUE,RED,AMBER,GREEN,FONT_NORMAL
from app.gui.header import make_header
from app.gui.sidebar import Sidebar
from app.database import get_prediction_counts,get_recent_predictions

class DashboardScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg=BG); self.controller=controller; self.pack(fill="both",expand=True)
        Sidebar(self,controller,"dashboard")
        self.content=tk.Frame(self,bg=BG); self.content.pack(side="right",fill="both",expand=True)
        make_header(self.content,controller,"Professional Analytics Dashboard")
        self.build()

    def card(self,parent,title,value,sub,bg):
        f=tk.Frame(parent,bg=bg,height=100); f.pack(side="left",fill="both",expand=True,padx=5); f.pack_propagate(False)
        tk.Label(f,text=title,bg=bg,fg=WHITE,font=("Times New Roman",10,"bold")).pack(anchor="w",padx=13,pady=(13,2))
        tk.Label(f,text=str(value),bg=bg,fg=WHITE,font=("Times New Roman",23,"bold")).pack(anchor="w",padx=13)
        tk.Label(f,text=sub,bg=bg,fg=WHITE,font=("Times New Roman",9)).pack(anchor="w",padx=13)

    def build(self):
        for w in self.content.winfo_children()[1:]: w.destroy()
        counts=get_prediction_counts(); total=sum(counts.values())
        try: acc=self.controller.load_predictor().get_accuracy()*100
        except Exception: acc=0
        user=(self.controller.current_user or {}).get("username","User")
        welcome=tk.Frame(self.content,bg=WHITE); welcome.pack(fill="x",padx=18,pady=(14,5))
        tk.Label(welcome,text=f"Welcome back, {user}",bg=WHITE,fg=NAVY,font=("Times New Roman",18,"bold")).pack(anchor="w",padx=16,pady=(12,1))
        tk.Label(welcome,text="Monitor academic risk, identify students early, and support timely intervention.",bg=WHITE,fg="#7F8C8D",font=FONT_NORMAL).pack(anchor="w",padx=16,pady=(0,12))
        top=tk.Frame(self.content,bg=BG); top.pack(fill="x",padx=18,pady=6)
        self.card(top,"TOTAL STUDENTS",total,"Processed records",NAVY)
        for label,col in [("At-Risk",RED),("Average",AMBER),("High-Achiever",GREEN)]:
            n=counts.get(label,0); pct=n/total*100 if total else 0
            self.card(top,label.upper(),n,f"{pct:.1f}% of students",col)
        self.card(top,"MODEL ACCURACY",f"{acc:.2f}%","CART Decision Tree",BLUE)
        charts=tk.Frame(self.content,bg=BG); charts.pack(fill="both",expand=True,padx=18,pady=6)
        fig=Figure(figsize=(10.8,3.4),dpi=100); fig.patch.set_facecolor(WHITE)
        a1=fig.add_subplot(141); a2=fig.add_subplot(142); a3=fig.add_subplot(143); a4=fig.add_subplot(144)
        labels=["At-Risk","Average","High-Achiever"]; vals=[counts.get(x,0) for x in labels]
        if total: a1.pie(vals,labels=labels,autopct="%1.0f%%",colors=[RED,AMBER,GREEN],textprops={"fontsize":7})
        else: a1.text(.5,.5,"No predictions yet",ha="center",va="center"); a1.set_xticks([]);a1.set_yticks([])
        a1.set_title("Risk Distribution",fontsize=9)
        a2.bar(labels,vals,color=[RED,AMBER,GREEN]); a2.tick_params(axis="x",labelrotation=25,labelsize=7); a2.set_title("Class Counts",fontsize=9)
        imp={}
        try: imp=self.controller.load_predictor().get_feature_importance()
        except Exception: pass
        if imp:
            a3.barh(list(imp.keys()),list(imp.values()),color=BLUE); a3.tick_params(axis="y",labelsize=6)
        else: a3.text(.5,.5,"Model unavailable",ha="center",va="center");a3.set_xticks([]);a3.set_yticks([])
        a3.set_title("Feature Importance",fontsize=9)
        risk=(counts.get("At-Risk",0)/total*100) if total else 0
        a4.barh(["Risk"],[risk],color=RED); a4.set_xlim(0,100); a4.text(min(risk+2,95),0,f"{risk:.1f}%",va="center",fontsize=9); a4.set_title("At-Risk Indicator",fontsize=9); a4.set_xlabel("Percentage",fontsize=8)
        fig.tight_layout(); c=FigureCanvasTkAgg(fig,charts); c.draw(); c.get_tk_widget().pack(fill="both",expand=True)
        box=tk.Frame(self.content,bg=WHITE); box.pack(fill="x",padx=18,pady=(0,12))
        tk.Label(box,text="Recent Predictions",bg=WHITE,fg=NAVY,font=("Times New Roman",13,"bold")).pack(anchor="w",padx=12,pady=8)
        recent=get_recent_predictions(6)
        if recent:
            from tkinter import ttk
            cols=["student_id","predicted_class","confidence","date_generated"]; t=ttk.Treeview(box,columns=cols,show="headings",height=min(6,len(recent)))
            for ccol,label in zip(cols,["Student ID","Prediction","Confidence","Date"]): t.heading(ccol,text=label); t.column(ccol,width=170,anchor="center")
            for r in recent: t.insert("","end",values=(r["student_id"],r["predicted_class"],f'{r["confidence"]:.1f}%',r["date_generated"]))
            t.pack(fill="x",padx=12,pady=(0,10))
        else: tk.Label(box,text="No predictions yet. Create a prediction or upload a CSV to begin.",bg=WHITE,fg="#7F8C8D",font=FONT_NORMAL).pack(pady=14)
        tk.Button(self.content,text="REFRESH DASHBOARD",command=self.build,bg=BLUE,fg=WHITE,font=FONT_NORMAL,relief="flat").pack(anchor="e",padx=20,pady=(0,10))
